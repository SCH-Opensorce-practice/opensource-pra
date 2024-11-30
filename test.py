import aiohttp
import asyncio

URL = "https://httpbin.org/uuid"


async def fetch(session, url):
    async with session.get(url) as response:
        json_repsonse = await response.json()
        print(json_repsonse["uuid"])


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, URL) for _ in range(100)]
        await asyncio.gather(*tasks)


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
