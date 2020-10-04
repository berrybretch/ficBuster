import asyncio

def decor(fetch, retries=10):
    async def wrapper(*args, **kwargs):
        while retries > 0:
            response = await fetch(*args, **kwargs)
            async with response:
                if response.status == 200:
                    return response
                elif response.status == 429:
                    asyncio.sleep(10)
                    print(response.status, '...waiting')
                    retries -= 1
                    continue
                elif response.status in range(500, 599):
                    print(f'Bad status, see {response.status}')
                    break
    return wrapper
