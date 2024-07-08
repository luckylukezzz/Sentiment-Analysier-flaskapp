import mysql.connector


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    port=3306,
    password="2001"
)

# Create a cursor object
cursor = conn.cursor()

# Create a new schema
cursor.execute("CREATE SCHEMA IF NOT EXISTS analytica")

# Select the schema
cursor.execute("USE analytica")

# Create a new table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
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

insert_query = "INSERT INTO products (name, age) VALUES (%s, %s)"
cursor.executemany(insert_query, dummy_data)
# Commit the changes
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print("Schema and table created successfully.")
