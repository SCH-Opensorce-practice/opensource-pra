import pytest
from datetime import datetime
from src.db.conn import create_connection_pool
from src.db.model import create_table, QnaDataModel
from src.async_http.page import QnaData

@pytest.fixture
def connection():
    pool = create_connection_pool("127.0.0.1", "attendance", "root", "1234")
    connection = pool.get_connection()
    create_table(connection)
    yield connection
    connection.close()

def test_qna_data_model_create(connection):
    qna_data = QnaData()
    qna_data.id = 1
    qna_data.type = "Type"
    qna_data.title = "Title"
    qna_data.writer = "Writer"
    qna_data.file_link = "https://example.com/file"
    qna_data.view = 10
    qna_data.upload_date = datetime.strptime("2023-10-10", "%Y-%m-%d")
    qna_data.detail_link = "https://example.com"
    qna_data.details = "Details"

    model = QnaDataModel(qna_data)
    model.create(connection)
    fetched_data = model.read(connection, 1)
    assert fetched_data is not None
    assert fetched_data.id == 1
    assert fetched_data.type == "Type"
    assert fetched_data.title == "Title"
    assert fetched_data.writer == "Writer"
    assert fetched_data.file_link == "https://example.com/file"
    assert fetched_data.view == 10
    assert fetched_data.upload_date == datetime.strptime("2023-10-10", "%Y-%m-%d")
    assert fetched_data.detail_link == "https://example.com"
    assert fetched_data.details == "Details"
    model.delete(connection, 1)

def test_create_table(connection):
    create_table(connection)
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES LIKE 'QnaData'")
    result = cursor.fetchone()
    assert result is not None, "Table QnaData was not created"
    cursor.close()