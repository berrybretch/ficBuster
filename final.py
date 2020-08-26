import requests
from bs4 import BeautifulSoup as bs
import asyncio
import aiohttp
import re

test_link = '''https://forums.spacebattles.com/threads/compulsion-worm-prototype.821228/'''
test_link2 = 'https://forums.spacebattles.com/threads/the-blacks-the-greens-and-the-reds-asoiaf-si-au.792052/reader/'

def validator(link):
    '''
    wanted to use regex but realized i am not insane
    '''
    if 'https://forums.spacebattles.com' in link:
        print("Link seems ok...I'll trust you")
        if 'reader' in link:
            return link
        else:
            return link + '/reader'
    else:
        raise ValueError("We want link from spacebattles")    


def page_links(link) ->list:
    '''
    returns list of links to other pages
    '''
    page_one = requests.get(link)
    soup = bs(page_one.text, 'lxml')
    pages = [ i for i in soup.find_all('li', class_='pageNav-page')]
    num = pages[-1].text
    page_links = ["{}page-{}".format(link, i+1) for i in range(int(num))]
    return page_links

async def grab_content(specific_page, session):
    print(f"Getting link={specific_page}")
    return await session.get(specific_page) 

async def executor(pages):
    conn= aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=conn) as client:
        content = [grab_content(i, client) for i in pages]
        return await asyncio.gather(*content)

if __name__ == "__main__":
    pages = page_links(test_link2)
    loop = asyncio.get_event_loop()
    all_the_content = loop.run_until_complete(executor(pages))

