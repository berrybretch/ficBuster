import requests
import asyncio
import aiohttp
links = [f"https://forums.spacebattles.com/threads/the-blacks-the-greens-and-the-reds-asoiaf-si-au.792052/reader/page-{i+1}" for i in range(10)]

async def fetch(session, url):
    print(f"Running {url}")
    return await session.get(url)

loop = asyncio.get_event_loop()
client = aiohttp.ClientSession()
futures = [fetch(client, i) for i in links]
x = asyncio.gather(*futures)

content = loop.run_until_complete(x)

