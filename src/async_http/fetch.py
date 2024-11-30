import aiohttp


async def fetcher(session: aiohttp.ClientSession, URL: str):
    async with session.get(URL) as res:
        return await res.text()
