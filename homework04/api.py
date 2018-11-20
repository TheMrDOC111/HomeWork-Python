import requests
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime
from homework04.model import User
from homework04.model import Message
from homework04.plotly_config import config_ploty
import plotly
import time
import igraph
from homework04.vk_config import config
from igraph import Graph, plot
import numpy as np


def get(url: str, params={}, timeout=5, max_retries=5, backoff_factor=0.3) -> dict:
    for i in range(max_retries):
        try:
            res = requests.get(url, params=params).json()
            try:
                return res["response"]
            except KeyError:
                return {'error': 'response error'}
        except requests.RequestException:
            time.sleep(timeout)
            timeout *= backoff_factor * (2 ** i)


def get_friends(user_id: int, fields="") -> dict:
    """ Вернуть данных о друзьях пользователя
    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    query_params = {
        'domain': config['domain'],
        'access_token': config["VK_ACCESS_TOKEN"],
        'user_id': user_id,
        'fields': fields,
        'v': config['v']
    }

    query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}".format(
        **query_params)
    response = get(query)
    return response


def age_predict(user_id: int) -> int:
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: идентификатор пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    friends = get_friends(user_id, "bdate")
    friends = friends["items"]
    new_friend = []
    for friend in friends:
        new_friend.append(User(**friend))
    friends = new_friend
    friends_date = []
    for friend in friends:
        if friend.bdate is not None:
            data = friend.bdate.split(".")
            if len(data) == 3:
                friends_date.append(friend.bdate)

    ages = []
    for year in friends_date:
        age = datetime.now().year - int(year.split(".")[2])
        if datetime.now().month - int(year.split(".")[1]) < 0 and datetime.now().day - int(year.split(".")[0]) < 0:
            ages.append(age - 1)
        else:
            ages.append(age)
    ages.sort()

    if len(ages) % 2 == 0:
        return (ages[len(ages) // 2] + ages[len(ages) // 2 + 1]) // 2

    return ages[len(ages) // 2]


def messages_get_history(user_id: int, offset=0, count=200) -> None:
    """ Получить историю переписки с указанным пользователем
    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"

    query_params = {
        'domain': config['domain'],
        'access_token': config["VK_ACCESS_TOKEN"],
        'user_id': user_id,
        'offset': offset,
        'count': count,
        'v': config['v']
    }
    query = "{domain}/messages.getHistory?access_token={access_token}&user_id={user_id}&v={v}".format(
        **query_params)
    response = get(query)
    count = response['count']
    messages = []
    while count > 0:
        query = "{domain}/messages.getHistory?access_token={access_token}&user_id={user_id}&offset={offset}&count={count}&v={v}".format(
            **query_params)
        response = get(query)
        messages.extend(response["items"])
        count -= min(count, 200)
        query_params['offset'] += 200
        query_params['count'] = min(count, 200)
        time.sleep(0.3334)

    count_dates_from_messages(messages)


def count_dates_from_messages(messages: list) -> None:
    """ Получить список дат и их частот
    :param messages: список сообщений
    """
    date = []
    count = []
    new_messages = []
    for message in messages:
        new_messages.append(Message(**message))
    messages = new_messages

    for message in messages:
        message.date = datetime.utcfromtimestamp(message.date).strftime("%Y-%m-%d")
        date.append(message.date)
        k = 0
        for mes in messages:
            if message.date == mes.date:
                k += 1
        count.append(k)

    plotly_messages_freq([date, count])


def plotly_messages_freq(freq_list: list) -> None:
    """ Построение графика с помощью Plot.ly
    :param freq_list: список дат и их частот
    """
    plotly.tools.set_credentials_file(username=config_ploty["username"], api_key=config_ploty["api_key"])
    data = [go.Scatter(x=freq_list[0], y=freq_list[1])]
    py.plot(data)


def get_network(user_id: int, as_edgelist=True) -> list:
    users_ids = get_friends(user_id)['items']
    edges = []
    for user1 in range(len(users_ids)):
        response = get_friends(users_ids[user1])
        if response.get('error'):
            continue
        friends = response['items']
        for user2 in range(user1 + 1, len(users_ids)):
            if users_ids[user2] in friends:
                edges.append((user1, user2))
        time.sleep(0.33333334)
    return edges


def plot_graph(user_id: int) -> None:
    surnames = get_friends(user_id, 'last_name')
    vertices = [i['last_name'] for i in surnames['items']]
    edges = get_network(user_id)
    g = Graph(vertex_attrs={"shape": "circle",
                            "label": vertices,
                            "size": 10},
              edges=edges, directed=False)

    n = len(vertices)
    visual_style = {
        "vertex_size": 20,
        "edge_color": "gray",
        "layout": g.layout_fruchterman_reingold(
            maxiter=100000,
            area=n ** 2,
            repulserad=n ** 2)
    }

    clusters = g.community_multilevel()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)
    plot(g, **visual_style)


if __name__ == '__main__':
    user_id = 164416858
    print("Примерный возраст", age_predict(user_id))
    messages_get_history(user_id)
    plot_graph(user_id)
