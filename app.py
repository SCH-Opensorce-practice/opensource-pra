import aiohttp
import asyncio

from src.async_http.page import get_page_all, get_page_details
from src.async_http.fetch import fetcher

PAGE_URL = "https://ksae.org/jajak/bbs/index.php?page={}&code=J_qna"


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetcher(session, PAGE_URL.format(i)) for i in range(1, 2)]
        results = await asyncio.gather(*tasks)
        datas = get_page_all(results)
        await get_page_details(session, datas)
        # TOOD:Database async insert


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
