from datetime import datetime as dt

import feedparser
import requests
from bs4 import BeautifulSoup


class Grabber:
    """Получение последних новостей из запрошенного RSS канала"""

    def news(self, limit=None):
        """
        Получение новостей из RSS канала
            limit: количество последних новостей
        """
        news = []
        url = self.urls[0]
        fp = feedparser.parse(url)
        all_feed = fp["items"]

        for feed in all_feed:
            if limit is not None and limit > 0:
                piece_news = {}
                pub_date = dt.strptime(
                    feed['published'], '%a, %d %b %Y %H:%M:%S %z'
                )
                piece_news['title'] = feed['title']
                piece_news['link'] = feed['link']
                piece_news['desc'] = feed['description']
                piece_news['pub_date'] = pub_date.strftime('%d.%m.%Y %H:%M')
                news.append(piece_news)
                limit -= 1
        return news

    def grub(self, link):
        """
        Получаем данные статьи по ссылке
        """
        raise NotImplementedError


class Lenta(Grabber):
    def __init__(self):
        self.urls = [
            'http://lenta.ru/rss'
        ]
        self.tmp_news = []

    def grub(self, link) -> dict:
        article_dict = {}
        r = requests.get(link).text
        soup = BeautifulSoup(r, 'html.parser')
        article = soup.find('div', class_='b-topic__content')
        article_dict['title'] = article.find(
            'h1', class_='b-topic__title'
        ).text.replace('\xa0', ' ')

        img = soup.find('div', class_='b-topic__title-image')
        img = img.find('img', src=True)
        article_dict['image'] = img.get('src') if img is not None else None

        contents = article.find('div', itemprop='articleBody')
        for content in contents.find_all('p'):
            article_dict['content'] = article_dict.get(
                'content', []) + [content.text]

        return article_dict


if __name__ == '__main__':
    grabber = Lenta()
    news = grabber.news(limit=3)
    data = [grabber.grub(news[i]['link']) for i in range(len(news))]

    print(data)
