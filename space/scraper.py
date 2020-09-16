import requests
from bs4 import SoupStrainer, BeautifulSoup
import re
import asyncio
import aiohttp


class Space:
    def __init__(self, url=None):
        self.url = self._validate_url(url)
        self.data = {}
        self.data["threadmarks"] = []
        self.data["story"] = {}

    def _get_pages(self):
        """
        Find out how many pages are available in the story
        populate self.data for lang, author and title.
        returns number of pages available for scraping 
        params:
            none
        returns:
            pages:int
        """
        print("Getting pages...")
        page = requests.get(self.url).text
        smol_filter = re.compile("pageNav-page")
        soup = BeautifulSoup(page, "lxml")
        pages_tag = soup.findAll("li", class_=smol_filter)
        if pages_tag:
            pages = int(pages_tag.text)
        else:
            pages = 1

        articles = soup.select("article.message")
        author = articles[0]["data-author"]
        title = soup.select("title")[0].text

        self.data = dict(
            self.data, **{"lang": "en", "docAuthor": author, "docTitle": title,}
        )

        return pages

    @staticmethod
    def _validate_url(url=None):
        """
        Check if the url is good.
        WIP
        """
        print(f"Validating {url}...")
        if url:
            reg = re.compile("https://forums.spacebattles.com/threads/(.*?)")
            url = url.rstrip("/")
            if reg.match(url):
                if "/reader" in url:
                    print("Url seems fine")
                    return url
                else:
                    print("Url seems fine")
                    return url + "/reader"
            else:
                raise ValueError("Give Me spacebattles link")

    async def _fetch_url(self, url, session):
        """
        Async Request
        params:
            session
            url:str
        returns:
            coroutine to be executed in async
        """
        print(f"Fetching {url}...")
        return await session.get(url)

    def _parse_soup(self, html):
        """
        Turns html into soup, parses it for text i need, then populates self.data.
        params:
            html:str
        returns:
            none
        """
        print("Straining...")
        soup = BeautifulSoup(html, "lxml")
        articles = soup.select("article.message")
        post_id = [i["data-content"] for i in articles]
        threadmarks = [i.select("span.threadmarkLabel")[0].text for i in articles]
        content = [i.select("div.bbWrapper")[0].text for i in articles]

        print("Done Straining, populating object...")

        self.data["story"] = dict(self.data["story"], **dict(zip(post_id, content)))
        for i in threadmarks:
            self.data["threadmarks"].append(i)

    async def build(self):
        """
        Setup all requests, await them, return the response.text
        """
        print("Building...")
        if not self.url:
            raise (ValueError)
        num = self._get_pages()
        urls = [self.url + "/page-{}".format(i + 1) for i in range(num)]
        async with aiohttp.ClientSession() as session:
            futures = [self._fetch_url(url, session) for url in urls]
            content = await asyncio.gather(*futures)
            text = [await i.text() for i in content]
        return text

    def wrap(self):
        """
            Runs blocking async code, then runs function to parse response for each
            params:
                none
            returns:
                none
        """
        all_content = asyncio.run(self.build())
        for i in all_content:
            self._parse_soup(i)
