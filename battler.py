
#class should only download content, nothing else.
import requests
#for grabbing the content from the internet
from bs4 import BeautifulSoup
#for parsing the content
from concurrent.futures import ThreadPoolExecutor
#for doing the above asynchronously
import asyncio
import aiohttp


#each chapter should be of the form
#date{thread:chapter}, date2{thread:chapter}


class SpaceBattler:
    def __init__(self, link):
        self.session = requests.session()
        self.client = aiohttp.ClientSession()
        if 'forums.spacebattles.com' in link:
            if 'reader' in link:
                self.link = link
            else:
                self.link = link +'/reader'
        else:
            raise ValueError('Need a link from Spacebattles')
        
    
    def page_links(self):
        '''
        Returns list of pages for entire story using pagination.
        '''
        page_one = self.session.get(self.link)
        soup = BeautifulSoup(page_one.text, 'lxml')
        pages = [ i for i in soup.find_all('li', class_='pageNav-page')]
        num = pages[-1].text
        page_links = ["{}/page-{}".format(self.link, i+1) for i in range(int(num))]
        return page_links

    async def grab_content(self, specific_page):
        '''
        get all the responses. better?
        '''
        print(f"Runnning link ->{specific_page}")
        await self.client.get(specific_page)

    def executor(self, links):
        loop = asyncio.get_event_loop()
        futures = asyncio.gather(*[self.grab_content(i) for i in links])
        content = loop.run_until_complete()
        return content       

        

    def parse_content(self):
        pass


if __name__ == "__main__":
    link_here = "https://forums.spacebattles.com/threads/the-blacks-the-greens-and-the-reds-asoiaf-si-au.792052/reader/"
    x = SpaceBattler(link_here)
    test = x.page_links()
    content = x.executor(test)