import requests
from bs4 import SoupStrainer, BeautifulSoup
import re
import asyncio
import aiohttp
from functools import reduce


class Space:
    def __init__(self, url=None):
        self.url = self._validate_url(url)
        self.meta = {}
        self.meta["threadmarks"] = []

    def _get_pages(self):
        """
        Find out how many pages are available in the story
        return metadata for lang, author and title. 
        params:
            none
        returns:
            pages:int
        """
        print("Getting pages...")
        page = requests.get(self.url).text
        smol_filter = re.compile("pageNav-page")
        soup = BeautifulSoup(page, "lxml")
        pages = int(soup.findAll("li", class_=smol_filter)[-1].text)
        articles = soup.select("article.message")
        author = articles[0]["data-author"]
        title = soup.select("title")[0].text

        self.meta = dict(
            self.meta, **{"lang": "en", "docAuthor": author, "docTitle": title,}
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

    @staticmethod
    def _parse_soup(html):
        """
        Parses soup, returns thread content in dictionary format

        params:   
            html_file
        returns:
            dictionary(post_id:content) 
        """
        print("Straining...")
        soup = BeautifulSoup(html, "lxml")
        articles = soup.select("article.message")
        post_id = [i["data-content"] for i in articles]
        threadmarks = [i.select("span.threadmarkLabel")[0].text for i in articles]
        content = [i.select("div.bbWrapper")[0].text for i in articles]
        print("Done Straining, zipping it up...")
        story = dict(zip(post_id, content))
        return story, threadmarks

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
            Populate object variables so i can shove entire object into epub class instead
        """
        all_content = asyncio.run(self.build())
        # all content is already in order, returns text
        parsed_content = [self._parse_soup(i) for i in all_content]
        # returns tuple of story dictionary and threadmarks

        self.meta["story"] = reduce(self.dict_merge, parsed_content[0])
        for i in parsed_content[1]:
            self.meta["threadmarks"].append(i)

    @staticmethod
    def dict_merge(dict1, dict2):
        """
        Im going to use this for merging all posts together into one large dictionary
        """
        return dict(dict1, **dict2)
