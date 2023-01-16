from abc import ABC, abstractmethod
from sqlite3 import IntegrityError
import requests
from bs4 import BeautifulSoup
import json
import sqlite


class Article:

    def __init__(self, page, title, href) -> None:
        self.page = page
        self.title = title
        self.href = href


class ArticleList(list[Article]):

    def _to_json(self):
        return json.dumps(
            [article.__dict__ for article in self],
            indent=4,
            ensure_ascii=False
        )

    def write_to_json(self, file):
        with open(file, "a", encoding='utf-8') as f:
            f.write(self._to_json())

    def write_to_db(self, file):
        with sqlite.SQLite(file) as curr:
            for article in self:
                try:
                    curr.execute(
                        "INSERT INTO articles (page, title, href) VALUES(?,?,?)",
                        [article.page, article.title, article.href]
                    )
                except IntegrityError:
                    print(f'Article already exists. {article.title}', flush=True)


class Scraper(ABC):

    results: ArticleList
    url: str

    @abstractmethod
    def get_results(self):
        pass


class VZScraper(Scraper):

    url = "https://www.vz.lt/visos-naujienos?pageno=0"
    results = ArticleList()

    def get_results(self):
        r = requests.get(url=self.url)

        soup = BeautifulSoup(r.text, 'html.parser')
        result_set = soup.select('div.one-article div.txt-wr > a')

        for html_tag in result_set:
            article = Article(
                page="vz",
                title=str(html_tag.get('title')),
                href=str(html_tag.get('href'))
            )
            self.results.append(article)
        return self.results


class DelfiScraper(Scraper):

    url = "https://www.delfi.lt/archive/latest.php"
    results = ArticleList()

    def get_results(self):
        r = requests.get(url=self.url)

        soup = BeautifulSoup(r.text, 'html.parser')
        result_set = soup.select('a.CBarticleTitle')

        for html_tag in result_set:
            article = Article(
                page="delfi",
                title=html_tag.text,
                href=str(html_tag.get('href'))
            )
            self.results.append(article)
        return self.results


class MinutesScraper(Scraper):

    url = "https://www.15min.lt/naujienos"
    results = ArticleList()

    def get_results(self):
        r = requests.get(url=self.url)

        soup = BeautifulSoup(r.text, 'html.parser')
        result_set = soup.select('div.visual-list a.vl-img-container')

        for html_tag in result_set:
            article = Article(
                page="15min",
                title=str(html_tag.get('title')),
                href=str(html_tag.get('href'))
            )
            self.results.append(article)
        return self.results
