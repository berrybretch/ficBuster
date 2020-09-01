import asyncio
import aiohttp


from bs4 import BeautifulSoup as BS 

class Space:
    def __init__(self, link:str):
        if 'forums.spacebattles.com' not in link:
            raise ValueError("Expected spacebattles link")
        if '/reader' not in link:
            self.link = link.rstrip('/')+'/reader'
        else:
            self.link = link
        self.sesh = aiohttp.ClientSession()

    async def fetch_links(self):
        reader = await self.fetch(self.sesh, self.link)
        soup = BS(reader, 'lxml')
        all_list_items = soup.findAll('li', class_='pageNav-page')
        last_item_text = all_list_items[-1].text
        return int(last_item_text)

    
    def tasks(self,num_of_links:int): 
        links = [self.link+'page-{i+1}' for i in range(num_of_links)]
        futures = [self.fetch(self.sesh,i) for i in links]
        return futures

    async def fetch(self, sesh, link:str): 
        with sesh.get(link) as response:
            return response.text()

    def parse_html(self, html_page):
        soup = BS(html_page, 'lxml')
        #threadmarks, bbwrappers, join together
        threads = soup.findAll("span",class_="threadmarkLabel")
        articles = soup.findAll("div", class_='bbWrapper')
        return {thread.text:article.text for thread in threads for article in articles}

    async def main(self):
        t = await self.fetch_links()
        routines = self.tasks(t)
        futures = await asyncio.gather(*routines)
        self.sesh.close()
        return futures






if __name__ == "__main__":
    link_here = "https://forums.spacebattles.com/threads/the-blacks-the-greens-and-the-reds-asoiaf-si-au.792052/reader"
    space = Space(link_here)
    
