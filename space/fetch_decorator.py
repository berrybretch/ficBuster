import asyncio
import aiohttp
from tenacity import *


@retry(stop=stop_after_attempt(2))
async def fetch():
    print("running fetch")
    async with aiohttp.ClientSession() as session:
        res = await session.get("http://0.0.0.0:8000/")
    if res.status == 200:
        asyncio.sleep(5)
        raise TryAgain
    else:
        return res


if __name__ == "__main__":
    asyncio.run(fetch())
