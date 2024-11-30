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


class QnaDataDB(QnaData):
    def __init__(self, connection_pool):
        self.connection_pool = connection_pool

    def get_create_query(self):
        return """
        INSERT INTO QnaData (id, type, title, writer, file_link, view, upload_date, detail_link, details)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

    def create(self):
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        insert_query = self.get_create_query()
        cursor.execute(
            insert_query,
            (
                self.id,
                self.type,
                self.title,
                self.writer,
                self.file_link,
                self.view,
                self.upload_date,
                self.detail_link,
                self.details,
            ),
        )
        connection.commit()
        cursor.close()
        connection.close()

    def read(self, qna_id):
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        select_query = "SELECT * FROM QnaData WHERE id = %s"
        cursor.execute(select_query, (qna_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result:
            (
                self.id,
                self.type,
                self.title,
                self.writer,
                self.file_link,
                self.view,
                self.upload_date,
                self.detail_link,
                self.details,
            ) = result
            return self
        return None

    def update(self):
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        update_query = """
        UPDATE QnaData SET type = %s, title = %s, writer = %s, file_link = %s, view = %s, upload_date = %s, detail_link = %s, details = %s
        WHERE id = %s
        """
        cursor.execute(
            update_query,
            (
                self.type,
                self.title,
                self.writer,
                self.file_link,
                self.view,
                self.upload_date,
                self.detail_link,
                self.details,
                self.id,
            ),
        )
        connection.commit()
        cursor.close()
        connection.close()

    def delete(self, qna_id):
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        delete_query = "DELETE FROM QnaData WHERE id = %s"
        cursor.execute(delete_query, (qna_id,))
        connection.commit()
        cursor.close()
        connection.close()


def get_page_all(html_text_list: List[str], connection_pool) -> List[QnaDataDB]:
    datas: List[QnaDataDB] = []
    for html_text in html_text_list:
        soup = BeautifulSoup(html_text, "html.parser")
        tr_list = soup.find_all("tr")[1:]
        for tr in tr_list:
            qna = QnaDataDB(connection_pool)
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
            qna.create()
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
