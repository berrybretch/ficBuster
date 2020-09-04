import requests
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer
import re
import asyncio
import aiohttp


class Space:
    def __init__(self, sesh, url=None):
        self.tasks = []
        self.session = sesh
        self.url = self._validate_url(url)

    def _set_tasks(self):
        page = requests.get(self.url).text
        smol_filter = re.compile("pageNav-page")
        soup = bs(
            page, "lxml", parse_only=SoupStrainer("li", attrs={"class": smol_filter})
        )
        pages = int(soup.findAll("li", class_=smol_filter)[-1].text)
        for page in range(pages):
            x = self._fetch_url(f"{self.url}+/page-{page+1}")
            self.tasks.append(x)
        return True

    def _get_tasks(self):
        return self.tasks

    @staticmethod
    def _validate_url(url=None):
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

    async def _fetch_url(self, url):
        """
        Should be asynchronous task
        """
        print(f"Fetching {url}...")
        async with self.session.get(url) as response:
            return response

    @staticmethod
    def _parse_soup(html):
        print("Straining")
        strainer = SoupStrainer(
            attrs={
                "class": lambda l: "bbWrapper" in l.split(),
                "class": lambda l: "threadmarkLabel" in l.split(),
            }
        )
        soup = bs(html, "lxml", parse_only=strainer)
        threads = [i.text for i in soup.findAll("span", class_="threadmarkLabel")]
        content = [i.text for i in soup.findAll("div", class_="bbWrapper")]
        return {k: v for k in threads for v in content}

    async def build(self):
        self._set_tasks()
        futures = await asyncio.gather(*self.tasks)
        await self.session.close()
        return futures


test_link = (
    """https://forums.spacebattles.com/threads/compulsion-worm-prototype.821228/"""
)
test_link2 = "https://forums.spacebattles.com/threads/the-blacks-the-greens-and-the-reds-asoiaf-si-au.792052/reader/"


if __name__ == "__main__":
    obj = Space(test_link2)
    fish = asyncio.run(obj.build())
