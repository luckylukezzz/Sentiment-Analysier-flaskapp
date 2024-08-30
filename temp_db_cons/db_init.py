import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

# Get the values from environment variables
host = os.getenv('HOST')
port = os.getenv('PORT')
database = os.getenv('DATABASE')
user = os.getenv('USER')
password = os.getenv('PASSWORD')


# Establish the connection
conn = mysql.connector.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database,
    ssl_disabled=False,
)

# Create a cursor object
cursor = conn.cursor()
print("connection success")