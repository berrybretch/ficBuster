import requests
from bs4 import SoupStrainer, BeautifulSoup
import re
import asyncio
import aiohttp
import uuid
from validator import validate_url
from decorators import decor


# how do i handle multiple requests?
# how do i handle timeouts? i dont
# all requests need to retry after certain amount of time


class Space:
    def __init__(self, url):
        self.url = validate_url(url)
        self.data = {}
        self.data["uid"] = str(uuid.uuid4())
        self.data["threadmarks"] = []
        self.data["story"] = {}
        self.links = []

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
            pages = int(pages_tag[-1].text)
        else:
            pages = 1
        articles = soup.select("article.message")
        author = articles[0]["data-author"]
        title = soup.select("title")[0].text

        # appends author, language and title information to self.data
        self.data = dict(
            self.data, **{"lang": "en", "docAuthor": author, "docTitle": title,}
        )
        self.links = [self.url + "/page-{}".format(i + 1) for i in range(pages)]

    @staticmethod
    async def _fetch_url(url, session):
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

    def _parse_soups(self, all_content):
        """
        Turns html into soup, parses it for text i need, then populates self.data.
        params:
            list_of_htmls
        returns:
            none
        """
        print("Straining...")
        for index, html in enumerate(all_content):
            print(f"page-{index}")
            soup = BeautifulSoup(html, "lxml")
            articles = soup.select("article.message")
            post_id = [i["data-content"] for i in articles]
            threadmarks = [i.select("span.threadmarkLabel")[0].text for i in articles]
            content = [i.select("div.bbWrapper")[0].text for i in articles]
            self.data["story"] = dict(self.data["story"], **dict(zip(post_id, content)))
            for i in threadmarks:
                self.data["threadmarks"].append(i)

    async def build(self):
        """
        Setup all requests, await them, return the response.text
        """
        print("Building...")
        self._get_pages()
        # returns all relevant links to self.links for reference
        # populates self.data with author, title and language
        async with aiohttp.ClientSession() as session:
            futures = [_fetch_url(url, session) for url in self.links]
            content = await asyncio.gather(*futures)
            text = [await i.text() for i in content]
        # text contains all the html of all the relevant pages
        return text

    def run(self):
        """
            Runs blocking async code, then runs function to parse response for each
            params:
                none
            returns:
                none
        """
        print("Running blocking function pls wait")
        all_content = asyncio.run(self.build())

        # reads all the html returned from the awaited content
        # grabs all relevant data and populates self.data with it.
        self._parse_soups(all_content)
        print("self.data has been populated")
