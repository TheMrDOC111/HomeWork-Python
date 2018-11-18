import requests
import json
from datetime import datetime
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime
from homework04.model import User
from homework04.model import Message
from homework04.plotly_config import config_ploty
import plotly

import time
from homework04.vk_config import config


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    delay = timeout
    for i in range(max_retries):
        try:
            return requests.get(url, params=params).json()["response"]
        except requests.RequestException:
            time.sleep(delay)
            delay *= delay + backoff_factor


def get_friends(user_id: int, fields) -> dict:
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


def age_predict(user_id):
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
    return ages[len(ages) // 2]


def messages_get_history(user_id, offset=0, count=20):
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

    messages = []
    while count > 0:
        query = "{domain}/messages.getHistory?access_token={access_token}&user_id={user_id}&offset={offset}&count={count}&v={v}".format(
            **query_params)
        response = get(query)
        messages.extend(response["items"])
        count -= min(count, 200)
        query_params['offset'] += 200
        query_params['count'] = min(count, 200)
        time.sleep(0.4)

    count_dates_from_messages(messages)

    pass


def count_dates_from_messages(messages):
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


def plotly_messages_freq(freq_list):
    """ Построение графика с помощью Plot.ly

    :param freq_list: список дат и их частот
    """

    print(freq_list[0], freq_list[1])

    plotly.tools.set_credentials_file(username=config_ploty["username"], api_key=config_ploty["api_key"])

    data = [go.Scatter(x=freq_list[0], y=freq_list[1])]
    py.plot(data)


def get_network(users_ids, as_edgelist=True):
    # PUT YOUR CODE HERE
    pass


def plot_graph(graph):
    # PUT YOUR CODE HERE
    pass


if __name__ == '__main__':
    print(age_predict(164416858))
    print(messages_get_history(221450385))

# user = User(**user_date)
