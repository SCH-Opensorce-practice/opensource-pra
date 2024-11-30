
from src.db.conn import create_connection_pool

def test_create_connection_pool():
    pool = create_connection_pool("127.0.0.1", "attendance", "root", "1234")
    assert pool is not None
    assert pool.pool_name == "mypool"
    assert pool.pool_size == 4