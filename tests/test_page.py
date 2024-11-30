
import pytest
import asyncio
from aiohttp import ClientSession
from src.async_http.page import get_page_all, get_page_details, QnaData
from datetime import datetime

@pytest.mark.asyncio
async def test_get_page_all():
    html_text_list = ["<html><body><table><tr><td>1</td><td>Type</td><td>Title</td><td>Writer</td><td><a href='/file'>File</a></td><td>10</td><td>2023-10-10</td></tr></table></body></html>"]
    datas = get_page_all(html_text_list)
    assert len(datas) == 1
    assert datas[0].id == 1
    assert datas[0].type == "Type"
    assert datas[0].title == "Title"
    assert datas[0].writer == "Writer"
    assert datas[0].file_link == ["https://ksae.org/file"]
    assert datas[0].view == 10
    assert datas[0].upload_date == datetime.strptime("2023-10-10", "%Y-%m-%d")
