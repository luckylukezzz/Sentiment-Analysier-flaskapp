from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

host = os.getenv('HOST')
database = os.getenv('DATABASE')
user = os.getenv('USER')
password = os.getenv('PASSWORD')

db = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    connection_timeout=60,
)
cursor = db.cursor(dictionary=True)


@app.route('/search')
def search_products():
    search_term = request.args.get('term', '')
    search_term = search_term.strip()
    print(search_term)  # Prepare for SQL LIKE search
    query = f"SELECT * FROM products WHERE title LIKE '%{search_term}%' LIMIT 10"
    print(query)
    try:

        cursor.execute(query)
        results = cursor.fetchall()
        return jsonify(results)
    except Error as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)