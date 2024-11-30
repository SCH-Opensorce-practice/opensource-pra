import mysql.connector
from mysql.connector import Error
from .conn import create_connection_pool


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


# Example usage:
# pool = create_connection_pool('your_host', 'your_database', 'your_user', 'your_password')
# connection = pool.get_connection()
# create_table(connection)
