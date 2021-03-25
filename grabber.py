import re
from datetime import datetime as dt
from typing import List, Union

import feedparser
import requests
from bs4 import BeautifulSoup

from core.utils import logger


class Grabber:
    """Получение последних новостей из запрошенного RSS канала"""
    rss_channels = {}

    def __init__(self, link: str = None):
        self._link = link
        if link is not None:
            name = self.__get_channel_name(link).lower()
            self.rss_channels[name] = link

    @classmethod
    def register(cls, collector: 'Grabber'):
        """Регистрация новостного источника"""
        name_collector = collector.__get_channel_name(collector._link).lower()
        if name_collector not in cls.__dict__:
            setattr(cls, name_collector, collector)

    def news(self, limit=None) -> List[dict]:
        """
        Получение новостей из RSS канала
            limit: количество последних новостей из канала
        """
        news = []
        if type(self).__name__.lower() == 'grabber':
            for url in self.rss_channels.values():
                news += self.__get_news(url, limit)
        else:
            url = self.rss_channels.get(type(self).__name__.lower())
            news += self.__get_news(url, limit)
        return news

    @staticmethod
    def __get_channel_name(link) -> str:
        pattern = r'https?:\/\/(?:[-\w]+\.)?([-\w]+)\.\w+(?:\.\w+)?\/?.*'
        match = re.search(pattern, link)
        return match.groups()[0]

    @logger.catch
    def __get_news(self, url, limit) -> Union[List[dict], list]:
        news = []
        try:
            fp = feedparser.parse(url)
        except Exception:
            logger.info(f'Temporary failure in name resolution {url}')
            return []

        all_feed = fp["items"]

        if limit is None:
            limit = len(all_feed)

        for feed in all_feed:
            if limit is not None and limit > 0:
                piece_news = {}
                pub_date = dt.strptime(
                    feed['published'], '%a, %d %b %Y %H:%M:%S %z'
                )
                piece_news['title'] = feed['title']
                piece_news['link'] = feed['link']
                piece_news['desc'] = feed['description']
                piece_news['published'] = pub_date.strftime('%d.%m.%Y %H:%M')
                news.append(piece_news)
                limit -= 1
        return news

    @logger.catch
    def get_news_page(self, link) -> Union[requests.Request, None]:
        try:
            r = requests.get(link)
            return r
        except requests.exceptions.RequestException:
            logger.info(f'Connection error by {link}.')
            return None

    @logger.catch
    def grub(self, link) -> Union[dict, None]:
        """Получаем данные статьи по ссылке"""
        channel_name = self.__get_channel_name(link).lower()
        try:
            reader = getattr(self, channel_name)
            return reader.grub(link)
        except AttributeError:
            logger.error(f'Not found grabber for link: {link}')
            return None


class Lenta(Grabber):
    def grub(self, link) -> dict:
        article_dict = {}
        article_dict['link'] = link
        page = self.get_news_page(link)

        if page is None:
            return {}

        soup = BeautifulSoup(page.text, 'html.parser')
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
    def grub(self, link) -> dict:
        article_dict = {}
        article_dict['link'] = link

        page = self.get_news_page(link)

        if page is None:
            return {}

        page = page.text.encode(page.encoding).decode('windows-1251')

        soup = BeautifulSoup(page, 'html.parser')
        article = soup.find('article', itemprop='articleBody')

        article_dict['title'] = article.find(
            'h1', itemprop='headline'
        ).text.replace('\xa0', ' ')

        img = soup.find('figure', class_='inner')
        if img:
            img = img.find('img', src=True)
        article_dict['image'] = img.get('src') if img is not None else None

        for content in article.find_all('p'):
            article_dict['content'] = article_dict.get(
                'content', []) + [content.text]

        return article_dict


class Kommersant(Grabber):
    def grub(self, link) -> dict:
        article_dict = {}
        article_dict['link'] = link

        page = self.get_news_page(link)

        if page is None:
            return {}

        soup = BeautifulSoup(page.text, 'html.parser')
        article = soup.find('article', class_='b-article')
        article_dict['title'] = article.find(
            'h1', itemprop='headline'
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


class M24(Grabber):
    def grub(self, link) -> dict:
        article_dict = {}
        article_dict['link'] = link
        page = self.get_news_page(link)

        if page is None:
            return {}

        soup = BeautifulSoup(page.text, 'html.parser')
        article = soup.find('div', class_='b-material_news')
        article_dict['title'] = article.find(
            'h1'
        ).text.replace('\xa0', ' ')

        img = soup.find('div', class_='b-material-incut-m-image')
        if img:
            img = img.find('img', src=True)
        article_dict['image'] = img.get('src') if img is not None else None

        contents = article.find('div', class_='b-material-body')
        for content in contents.find_all('p'):
            article_dict['content'] = article_dict.get(
                'content', []) + [content.text]

        return article_dict


Grabber.register(Lenta('http://lenta.ru/rss'))
Grabber.register(Interfax('http://www.interfax.ru/rss.asp'))
Grabber.register(Kommersant('http://www.kommersant.ru/RSS/news.xml'))
Grabber.register(M24('http://www.m24.ru/rss.xml'))


if __name__ == '__main__':
    grabber = Grabber()
    print(grabber.rss_channels)

    news = grabber.news(limit=1)
    print(news)

    data = [grabber.grub(news[i]['link']) for i in range(len(news))]
    print(data)
