import requests
from bs4 import BeautifulSoup
import db


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    news_table = parser.find_all("tr", {"class": "athing"})
    info = parser.find_all("td", {"class": "subtext"})
    for i in range(len(news_table)):
        comments = "0"
        links = info[i].find_all("a")
        title = news_table[i].find(class_="storylink")
        points = info[i].span.text.split()[0]
        try:
            if links[3].text != "discuss":
                comments = links[3].text.split()[0]
        except Exception as ex:
            pass

        news = {
            'author': links[0].text,
            'comments': comments,
            'points': points,
            'title': title.text,
            'url': title['href']
        }
        news_list.append(news)

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    return parser.table.find_all('table')[1].find_all('a')[-1]['href']
    pass


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html5lib")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news


news = get_news("https://news.ycombinator.com/", 1)
for i in news:
    print(i)

s = db.session()
for i in range(len(news)):
    obj = db.News(title=news[i]['title'],
                  author=news[i]['author'],
                  url=news[i]['author'],
                  comments=news[i]['comments'],
                  points=news[i]['points'])

    s.add(obj)


s.commit()
