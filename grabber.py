from datetime import datetime as dt

import feedparser
import requests
from bs4 import BeautifulSoup


class Grabber:
    """Получение последних новостей из запрошенного RSS канала"""
    rss_channels = {}

    def __init__(self, link: str = None):
        if link is not None:
            self.rss_channels[type(self).__name__.lower()] = link

    @classmethod
    def register(cls, collector: 'Grabber'):
        """Регистрируем сборщика как атрибут класса"""
        name_collector = type(collector).__name__.lower()
        if name_collector not in cls.__dict__:
            setattr(cls, name_collector, collector)

    def news(self, limit=None):
        """
        Получение новостей из RSS канала
            limit: количество последних новостей
        """
        news = []
        if type(self).__name__.lower() == 'grabber':
            for url in self.rss_channels.values():
                news += self.__get_news(url, limit)
        else:
            url = self.rss_channels.get(type(self).__name__.lower())
            news += self.__get_news(url, limit)
        return news

    def __get_news(self, url, limit):
        news = []
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
                # .strftime('%d.%m.%Y %H:%M')
                piece_news['published'] = pub_date
                news.append(piece_news)
                limit -= 1
        return news

    def grub(self, link):
        """Получаем данные статьи по ссылке"""
        raise NotImplementedError


class Lenta(Grabber):
    def grub(self, link) -> dict:
        article_dict = {}
        article_dict['link'] = link
        r = requests.get(link).text
        soup = BeautifulSoup(r, 'html.parser')
        article = soup.find('div', class_='b-topic__content')
        article_dict['title'] = article.find(
            'h1', class_='b-topic__title'
        ).text.replace('\xa0', ' ')

        img = soup.find('div', class_='b-topic__title-image')
        if img:
            img = img.find('img', src=True)
        article_dict['image'] = img.get('src') if img is not None else None

        contents = article.find('div', itemprop='articleBody')
        for content in contents.find_all('p'):
            article_dict['content'] = article_dict.get(
                'content', []) + [content.text]

        return article_dict


class Interfax(Grabber):
    pass


class Kommersant(Grabber):
    pass


class M24(Grabber):
    pass


Grabber.register(Lenta('http://lenta.ru/rss'))
Grabber.register(Interfax('http://www.interfax.ru/rss.asp'))
Grabber.register(Kommersant('http://www.kommersant.ru/RSS/news.xml'))
Grabber.register(M24('http://www.m24.ru/rss.xml'))


if __name__ == '__main__':
    grabber = Grabber()
    print(grabber.news(limit=1))

    news = grabber.lenta.news(limit=2)

    data = [grabber.lenta.grub(news[i]['link']) for i in range(len(news))]
    print(data)
