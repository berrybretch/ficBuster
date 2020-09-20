import requests
from bs4 import SoupStrainer, BeautifulSoup
import re
import asyncio
import aiohttp
import uuid

class Space:
    def __init__(self, url=None):
        self.url = self._validate_url(url)
        self.data = {}
        self.data['uid'] = str(uuid.uuid4())
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

        self.data = dict(
            self.data, **{"lang": "en", "docAuthor": author, "docTitle": title,}
        )
        self.links = [self.url + "/page-{}".format(i + 1) for i in range(pages)]

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
                raise ValueError("Spacebattles only pls")
        else:
            raise ValueError("I need a link")





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
            print(f'page-{index}')
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
        #_get_pages
        # run all coroutines
        #_parse_soup to populate obj
        self._get_pages()
        async with aiohttp.ClientSession() as session:
            futures = [self._fetch_url(url, session) for url in self.links]
            content = await asyncio.gather(*futures)
            text = [await i.text() for i in content]
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
        self._parse_soups(all_content)
        print('self.data has been populated')
