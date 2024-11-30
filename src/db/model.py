import mysql.connector
from mysql.connector import Error
from .conn import create_connection_pool
from ..async_http.page import QnaData


def create_table(connection: mysql.connector.connection.MySQLConnection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS QnaData (
            id INT PRIMARY KEY,
            type VARCHAR(255),
            title VARCHAR(255),
            writer VARCHAR(255),
            file_link TEXT,
            view INT,
            upload_date DATE,
            detail_link TEXT,
            details TEXT,
            INDEX (type),
            INDEX (title),
            INDEX (writer),
            INDEX (file_link),
            INDEX (view),
            INDEX (upload_date),
            INDEX (detail_link),
            INDEX (details)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


class QnaDataModel:
    def __init__(self, qna_data):
        self.qna_data = qna_data

    def get_insert_query(self):
        return """
        INSERT INTO QnaData (id, type, title, writer, file_link, view, upload_date, detail_link, details)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """.format(
            self.qna_data.id,
            self.qna_data.type,
            self.qna_data.title,
            self.qna_data.writer,
            self.qna_data.file_link,
            self.qna_data.view,
            self.qna_data.upload_date,
            self.qna_data.detail_link,
            self.qna_data.details,
        )

    def create(self, connection):
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO QnaData (id, type, title, writer, file_link, view, upload_date, detail_link, details)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            insert_query,
            (
                self.qna_data.id,
                self.qna_data.type,
                self.qna_data.title,
                self.qna_data.writer,
                self.qna_data.file_link,
                self.qna_data.view,
                self.qna_data.upload_date,
                self.qna_data.detail_link,
                self.qna_data.details,
            ),
        )
        connection.commit()
        cursor.close()

    def read(self, connection, qna_id):
        cursor = connection.cursor()
        select_query = "SELECT * FROM QnaData WHERE id = %s"
        cursor.execute(select_query, (qna_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            (
                self.qna_data.id,
                self.qna_data.type,
                self.qna_data.title,
                self.qna_data.writer,
                self.qna_data.file_link,
                self.qna_data.view,
                self.qna_data.upload_date,
                self.qna_data.detail_link,
                self.qna_data.details,
            ) = result
            return self.qna_data
        return None

    def update(self, connection):
        cursor = connection.cursor()
        update_query = """
        UPDATE QnaData SET type = %s, title = %s, writer = %s, file_link = %s, view = %s, upload_date = %s, detail_link = %s, details = %s
        WHERE id = %s
        """
        cursor.execute(
            update_query,
            (
                self.qna_data.type,
                self.qna_data.title,
                self.qna_data.writer,
                self.qna_data.file_link,
                self.qna_data.view,
                self.qna_data.upload_date,
                self.qna_data.detail_link,
                self.qna_data.details,
                self.qna_data.id,
            ),
        )
        connection.commit()
        cursor.close()

    def delete(self, connection, qna_id):
        cursor = connection.cursor()
        delete_query = "DELETE FROM QnaData WHERE id = %s"
        cursor.execute(delete_query, (qna_id,))
        connection.commit()
        cursor.close()
