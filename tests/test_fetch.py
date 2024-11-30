
import pytest
import aiohttp
from src.async_http.fetch import fetcher

@pytest.mark.asyncio
async def test_fetcher():
    async with aiohttp.ClientSession() as session:
        result = await fetcher(session, "https://example.com")
        assert result is not None