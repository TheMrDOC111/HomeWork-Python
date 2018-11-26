import requests
import time
import config
from api_models import Message


def get(url, params={}, timeout=1, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос
    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    for i in range(max_retries):
        try:
            res = requests.get(url, params=params, timeout=timeout)
            return res
        except requests.exceptions.RequestException:
            if i == max_retries - 1:
                raise
            backoff_value = backoff_factor * (2 ** i)
            time.sleep(backoff_value)


def get_friends(user_id: int, fields="") -> dict:
    """ Вернуть данных о друзьях пользователя
    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    query_params = {
        'domain': config.VK_CONFIG['domain'],
        'access_token': config.VK_CONFIG['access_token'],
        'user_id': user_id,
        'fields': fields,
        'v': config.VK_CONFIG['version']
    }

    query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}".format(
        **query_params)
    response = get(query, query_params)
    json_doc = response.json()
    fail = json_doc.get('error')
    if fail:
        raise Exception(json_doc['error']['error_msg'])
    return json_doc['response']['items']


def messages_get_history(user_id, offset=0, count=200) -> list:
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
        'domain': config.VK_CONFIG['domain'],
        'access_token': config.VK_CONFIG['access_token'],
        'user_id': user_id,
        'offset': offset,
        'count': count,
        'v': config.VK_CONFIG['version']
    }

    messages = []
    try:

        query = "{domain}/messages.getHistory?access_token={access_token}&user_id={user_id}&v={v}".format(
            **query_params)
        response = get(query)
        json_doc = response.json()
        fail = json_doc.get('error')
        if fail:
            raise Exception(json_doc['error']['error_msg'])
        count = json_doc['response']['count']
        while count > 0:
            query = "{domain}/messages.getHistory?access_token={access_token}&user_id={user_id}&offset={offset}&count={count}&v={v}".format(
                **query_params)
            response = get(query)
            json_doc = response.json()
            fail = json_doc.get('error')
            if fail:
                raise Exception(json_doc['error']['error_msg'])
            messages.extend(json_doc['response']["items"])
            count -= min(count, 200)
            query_params['offset'] += 200
            query_params['count'] = min(count, 200)
            time.sleep(0.4)
    finally:
        return messages
