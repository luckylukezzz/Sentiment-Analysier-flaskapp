################ Establishing the database connection ################

import mysql.connector
import os


class DBConnection:
    def __init__(self, port=os.getenv('PORT'), host=os.getenv('HOST'), user=os.getenv('USER'),
                 password=os.getenv('PASSWORD'), database=os.getenv('DATABASE')):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            ssl_disabled=False,
            database=database
        )
        self.cursor = self.conn.cursor()

    def fetch_reviews(self):
        self.cursor.execute("SELECT review_id, text FROM reviews")
        return self.cursor.fetchall()

    def fetch_keywords(self, parent_asin):
        query = "SELECT keywords FROM reviews WHERE parent_asin = %s"
        self.cursor.execute(query, (parent_asin,))
        return self.cursor.fetchall()

    def fetch_features(self, parent_asin):
        query = "SELECT features FROM products WHERE parent_asin = %s"
        self.cursor.execute(query, (parent_asin,))
        return self.cursor.fetchall()

    def update_improvements(self, parent_asin, formatted_output):
        query = "UPDATE products SET improvements = %s WHERE parent_asin = %s"
        self.cursor.execute(query, (formatted_output, parent_asin))
        self.conn.commit()

    def close(self):
        self.conn.close()
