import asyncio
import aiohttp
from validator import validate_url
from decorators import decor
from bs4 import BeautifulSoup
from tenacity import retry



class Mine:
    def __init__(self, url):
        self.url = validate_url(url)

    @retry
    async def fetch(self, url:str,session=None):
        '''
        Returns awaitable response
        params: 
            url:str   
        '''
        return await session.get(url)

  
    async def collect(self):
        '''
        Awaits first page of spacebattles, parses it for the page numbers
        makes list of urls to set up consecutive requests
        awaits all these requests asynchronously
        returns coroutine?
        '''
        async with aiohttp.ClientSession() as session:
            response = await self.fetch(self.url, session=session)
            #parse response for number of pages
            text = await response.text() 
            soup = BeautifulSoup(text, 'lxml')
            tags = soup.findAll('li', class_='pageNav-page')
            if not tags:
                number_of_links = 1
            else:
                number_of_links = int(tags[-1].text)
                print(f'Pages=={number_of_links}')
            urls = [
                f'{self.url}/page-{i+1}' for i in range(number_of_links)
            ]
            tasks = [self.fetch(url, session=session) for url in urls]
            future = await asyncio.gather(*tasks)
            return future

    def start(self):
        '''
        Runs the coroutine to generate the responses.
        '''
        return asyncio.run(self.collect())

    