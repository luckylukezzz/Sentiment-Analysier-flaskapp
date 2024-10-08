from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app)

host = os.getenv('HOST')
port= os.getenv('PORT')
database = os.getenv('DATABASE')
user = os.getenv('USER')
password = os.getenv('PASSWORD')

db = mysql.connector.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database,
    ssl_disabled=False,
    connection_timeout=1000,
)

cursor = db.cursor(dictionary=True)

@app.route('/search')
def search_products():
    search_term = request.args.get('term', '')
    search_term = search_term.strip()
    print(search_term)  # Prepare for SQL LIKE search
    #query = f"SELECT * FROM products WHERE title LIKE '%{search_term}%' LIMIT 10"

    try:
        if search_term:
            query = f"SELECT * FROM products WHERE title LIKE '%{search_term}%' LIMIT 10"
        else:
            query = "SELECT * FROM products LIMIT 10"
        cursor.execute(query)
        results = cursor.fetchall()
        return jsonify(results)
    except Error as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run()