from collections import Counter
from datetime import datetime
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from typing import List, Tuple
from api import messages_get_history
from api_models import Message
import config

Dates = List[datetime.date]
Frequencies = List[int]

plotly.tools.set_credentials_file(
    username=config.PLOTLY_CONFIG['username'],
    api_key=config.PLOTLY_CONFIG['api_key']
)


def fromtimestamp(ts: int) -> datetime.date:
    return datetime.fromtimestamp(ts).date()


def count_dates_from_messages(messages: List[Message]) -> Tuple[Dates, Frequencies]:
    """ Получить список дат и их частот
    :param messages: список сообщений
    """
    date = []
    frequencies = []
    for message in messages:
        message.date = datetime.utcfromtimestamp(message.date).strftime("%Y-%m-%d")
        date.append(message.date)
        k = 0
        for mes in messages:
            if message.date == mes.date:
                k += 1
        frequencies.append(k)
    return date, frequencies


def plotly_messages_freq(dates: Dates, freq: Frequencies) -> None:
    """ Построение графика с помощью Plot.ly
    :param date: список дат
    :param freq: число сообщений в соответствующую дату
    """
    data = [go.Scatter(x=dates, y=freq)]
    py.plot(data)

# if __name__ == '__main__':
#   user_id = 164416858
#  data, freq = count_dates_from_messages(messages_get_history(user_id))
# plotly_messages_freq(data, freq)
