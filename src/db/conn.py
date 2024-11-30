import mysql.connector
from mysql.connector import pooling


def create_connection_pool(
    host: str, database: str, user: str, password: str
) -> pooling.MySQLConnectionPool:
    pool = pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=4,
        pool_reset_session=True,
        host=host,
        database=database,
        user=user,
        password=password,
    )
    return pool
