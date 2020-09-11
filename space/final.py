import requests
from bs4 import SoupStrainer, BeautifulSoup
import re
import asyncio
import aiohttp
import pickle

BeautifulSoup


class Space:
    def __init__(self, url=None):
        self.tasks = []
        self.url = self._validate_url(url)

    def _get_pages(self):
        """
        Find out how many pages are available in the story
        """
        print("Getting pages...")
        page = requests.get(self.url).text
        smol_filter = re.compile("pageNav-page")
        soup = BeautifulSoup(
            page, "lxml", parse_only=SoupStrainer("li", attrs={"class": smol_filter})
        )
        pages = int(soup.findAll("li", class_=smol_filter)[-1].text)
        return pages

    @staticmethod
    def _validate_url(url=None):
        """
        Check if the url is good .
        """
        print(f"Validating {url}...")
        if url:
            reg = re.compile("https://forums.spacebattles.com/threads/(.*?)")
            url = url.rstrip("/")
            if reg.match(url):
                if "/reader" in url:
                    return url
                else:
                    return url + "/reader"
            else:
                raise ValueError("Give Me spacebattles link")

    async def _fetch_url(self, url, session):
        """
        Should be asynchronous task
        """
        print(f"Fetching {url}...")
        return await session.get(url)

    @staticmethod
    def _parse_soup(html):
        """
            Grab all the good stuff from the response.
            good_stuff is 
            """
        print("Straining")
        strainer = SoupStrainer(attrs={"class": "message",})
        soup = BeautifulSoup(html, "lxml")
        articles = soup.select("article.message")
        title = soup.select("title")[0].text
        lang = soup.find("html")["lang"]

        document = {
            "lang": lang,
            "uid": 1010101,  # todo generate uuid
            "docAuthor": articles[0]["data-author"],
            "docTitle": title,
            "index": [
                i for i, _ in enumerate(articles)
            ],  # temporary fix just to get it to work
            "depth": len(articles),
            "post_id": [i["data-content"] for i in articles],
            "threadmarks": [i.select("span.threadmarkLabel")[0].text for i in articles],
            "content": [i.select("div.bbWrapper")[0].text for i in articles],
        }
        return soup

    async def build(self):
        """
        Setup all requests, await them, process the responses that return
        """
        print("Building...")
        num = self._get_pages()
        urls = [self.url + "/page-{}".format(i + 1) for i in range(num)]
        async with aiohttp.ClientSession() as session:
            futures = [self._fetch_url(url, session) for url in urls]
            content = await asyncio.gather(*futures)
            text = [await i.text() for i in content]
        return text

    def wrap(self):
        """
        This is where i throw it all into an ebook ideally.
        """
        all_content = asyncio.run(self.build())
        parsed_content = [self._parse_soup(i) for i in all_content]
        return all_content
