import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import mysql.connector
load_dotenv()

host = os.getenv('HOST')
database = os.getenv('DATABASE')
user = os.getenv('USER')
port = os.getenv('PORT')
password = os.getenv('PASSWORD')

db = mysql.connector.connect(
    host=host,
    user=user,
    port=port,
    password=password,
    database=database
)
cursor = db.cursor()

query = "SELECT * FROM products WHERE title LIKE '%apple%' LIMIT 10"
cursor.execute(query)

results = cursor.fetchall()
print(results)