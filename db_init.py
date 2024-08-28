import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

# Get the values from environment variables
host = os.getenv('HOST')
database = os.getenv('DATABASE')
user = os.getenv('USER')
password = os.getenv('PASSWORD')


# Establish the connection
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

# Create a cursor object
cursor = conn.cursor()
print("connection success")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS productsmmmm (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        age INT
    )
""")
# Insert dummy data
dummy_data = [
    ("Alice", 30),
    ("Bob", 25),
    ("Charlie", 35)
]

insert_query = "INSERT INTO productsmmmm (name, age) VALUES (%s, %s)"
cursor.executemany(insert_query, dummy_data)
# Commit the changes
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print("Schema and table created successfully.")
