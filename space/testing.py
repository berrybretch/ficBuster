import asyncio
import aiohttp

local = "http://0.0.0.0:8000"


async def fetch(url, client):
    return await client.get(url)


async def gatherer():
    async with aiohttp.ClientSession() as client:
        futures = [fetch(local, client) for i in range(10)]
        return await asyncio.gather(*futures)


if __name__ == "__main__":
    asyncio.run(gatherer())
