import asyncio
import time
from datetime import datetime
from typing import List
from aiohttp import ClientSession
from .fetch import fetcher
from bs4 import BeautifulSoup


class QnaData:
    detail_link = None
    details = None
    file_link = None

    def insert_data(self, idx: int, text: str):
        text = text.replace("\n", "")
        if idx == 0:
            self.id = int(text)
        elif idx == 1:
            self.type = text
        elif idx == 2:
            self.title = text
        elif idx == 3:
            self.writer = text
        elif idx == 5:
            self.view = int(text)
        else:
            self.upload_date = datetime.strptime(text, "%Y-%m-%d")

    def show_all(self):
        print(f"ID: {self.id}")
        print(f"Type: {self.type}")
        print(f"Title: {self.title}")
        print(f"Writer: {self.writer}")
        print(f"File Link: {self.file_link}")
        print(f"View: {self.view}")
        print(f"Upload Date: {self.upload_date}")
        print(f"Detail Link: {self.detail_link}")
        print(f"Details: {self.details}")


def get_page_all(html_text_list: List[str]) -> List[QnaData]:
    datas: List[QnaData] = []
    for html_text in html_text_list:
        soup = BeautifulSoup(html_text, "html.parser")
        tr_list = soup.find_all("tr")[1:]
        for tr in tr_list:
            qna = QnaData()
            tds = tr.find_all("td")
            for idx, td in enumerate(tds):
                if idx == 2:
                    qna.insert_data(idx, td.text)
                    qna.detail_link = "https://ksae.org" + td.find("a")["href"]
                elif idx == 4:
                    qna.file_link = []
                    for a in td.find_all("a"):
                        qna.file_link.append("https://ksae.org" + a["href"])
                else:
                    qna.insert_data(idx, td.text)
            datas.append(qna)
        return datas


async def get_page_details(session: ClientSession, datas: List[QnaData]):
    tasks = [fetcher(session, data.detail_link) for data in datas]
    results = await asyncio.gather(*tasks)
    for idx, page in enumerate(results):
        result = ""
        soup = BeautifulSoup(page, "html.parser")
        spans = soup.find_all("span")
        for span in spans:
            result += span.text
        datas[idx].details = result
