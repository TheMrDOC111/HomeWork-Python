from datetime import datetime
from statistics import median
from typing import Optional
from api import get_friends
from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    friends = get_friends(user_id, "bdate")

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
        bornMonth = int(year.split(".")[1])
        bornDay = int(year.split(".")[0])
        if (datetime.now().month < bornMonth) or (datetime.now().month == bornMonth and datetime.now().day < bornDay):
            ages.append(age - 1)
        else:
            ages.append(age)
    ages.sort()

    if len(ages) > 0:
        return median(ages)
    else:
        return None
