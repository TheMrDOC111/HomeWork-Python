from bottle import (
    route, run, template, request, redirect
)
import bottle
import string
import os
from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    news = s.query(News).filter(News.id == request.query.id).one()
    news.label = request.query.label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    news_list = get_news("https://news.ycombinator.com/newest", n_pages=5)
    news_list_bd = s.query(News).all()
    if len(news_list_bd) > 0:
        for new_news in news_list:
            f = False
            for old_news_bd in news_list_bd:
                if new_news['author'] == old_news_bd.author and new_news['title'] == old_news_bd.title:
                    f = True
                    break
            if not f:
                s.add(News(**new_news))

    else:
        for new_news in news_list:
            s.add(News(**new_news))
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    labeled_news = s.query(News).filter(News.label != None).all()
    x_train = [clean(news.title) for news in labeled_news]
    y_train = [news.label for news in labeled_news]
    classifier.fit(x_train, y_train)

    rows = s.query(News).filter(News.label == None).all()
    good, maybe, never = [], [], []
    for row in rows:
        prediction = classifier.predict([clean(row.title)])
        print(prediction)
        if prediction == 'good':
            good.append(row)
        elif prediction == 'maybe':
            maybe.append(row)
        else:
            never.append(row)

    return template('news_recommendations', good=good, maybe=maybe, never=never)


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator).lower()


if __name__ == "__main__":
    abs_app_dir_path = os.path.dirname(os.path.realpath(__file__))
    abs_views_path = os.path.join(abs_app_dir_path, 'templates')
    bottle.TEMPLATE_PATH.insert(0, abs_views_path)
    classifier = NaiveBayesClassifier()
    run(host="localhost", port=8080)
