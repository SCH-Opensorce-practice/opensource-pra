import aiohttp
import asyncio

async def fetcher(session: aiohttp.ClientSession, URL: str):
    async with session.get(URL) as res:
        return await res.text()

async def test_fetcher():
    async with aiohttp.ClientSession() as session:
        result = await fetcher(session, "https://example.com")
        print(result)
