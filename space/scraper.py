import requests
from bs4 import SoupStrainer, BeautifulSoup
import re
import asyncio
import aiohttp
import pickle


class Space:
    def __init__(self, url=None):
        self.tasks = []
        self.url = self._validate_url(url)
        self.meta = {}


    def _get_pages(self):
        """
        Find out how many pages are available in the story
        return metadata for lang, author and title. 
        """
        print("Getting pages...")
        page = requests.get(self.url).text
        smol_filter = re.compile("pageNav-page")
        soup = BeautifulSoup( page, "lxml")
        pages = int(soup.findAll("li", class_=smol_filter)[-1].text)
        articles = soup.select('article.message')
        author = articles[0]['data-author']
        title = soup.select('title')[0].text

        self.meta = {
            "lang":"en",
            "docAuthor":author,
            "docTitle":title,
        } 
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
            good_stuff is text.
            parses a single page.
            """
        print("Straining...")
        strainer = SoupStrainer(attrs={"class": "message",})
        soup = BeautifulSoup(html, "lxml")
        articles = soup.select("article.message")
        post_id = [i["data-content"] for i in articles]
        threadmarks = [i.select("span.threadmarkLabel")[0].text for i in articles]
        content = [i.select("div.bbWrapper")[0].text for i in articles]
        print("Done Straining, zipping it up...")
        
        document = dict(zip(post_id, content)) 
        
        return content

    async def build(self):
        """
        Setup all requests, await them, return the response.text
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
        Need to combine all the pages into one dictionary, with all pertinent material.
        each page returns a dictionary
        lang, author and title are consistent
        depth,threadmarks,content, post_id keys need to accumulate in order.
        """
        all_content = asyncio.run(self.build())
        parsed_content = [self._parse_soup(i) for i in all_content]
        ##parsed content returns a tuple of dicks for every single page. how do i combine these?
        return all_content
