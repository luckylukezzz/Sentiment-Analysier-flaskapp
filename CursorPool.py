from queue import Queue
from threading import Lock
import mysql.connector

class CursorPool:
    def __init__(self, db_path, pool_size=5):
        self.db_path = db_path
        self.pool_size = pool_size
        self.connection = mysql.connect(db_path, check_same_thread=False)
        self.cursor_pool = Queue(maxsize=pool_size)
        self.lock = Lock()

        # Initialize the pool with cursors
        for _ in range(pool_size):
            cursor = self.connection.cursor()
            self.cursor_pool.put(cursor)

    def get_cursor(self):
        return self.cursor_pool.get()

    def release_cursor(self, cursor):
        self.cursor_pool.put(cursor)

    def execute_query(self, query, params=None):
        cursor = self.get_cursor()
        try:
            with self.lock:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                result = cursor.fetchall()
            return result
        finally:
            self.release_cursor(cursor)

    def close(self):
        while not self.cursor_pool.empty():
            cursor = self.cursor_pool.get()
            cursor.close()
        self.connection.close()

#example usage

#  pool = CursorPool(db_path)   // initialize
#  results = pool.execute_query("SELECT * FROM users")
#  pool.execute_query("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")