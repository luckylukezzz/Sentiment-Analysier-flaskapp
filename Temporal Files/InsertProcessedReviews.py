import mysql.connector

def create_review_sentiments_table(host, user, password, database):
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # SQL statement to create the table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS review_sentiments (
            ReviewNo INT AUTO_INCREMENT PRIMARY KEY,
            aspect VARCHAR(255),
            sentiment VARCHAR(50)
        )
        """

        # Execute the CREATE TABLE query
        cursor.execute(create_table_query)

        print("Table 'review_sentiments' created successfully.")

    except mysql.connector.Error as error:
        print(f"Error creating table: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def insert_review_sentiments(host, user, password, database, data):
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # SQL statement to insert data
        insert_query = """
        INSERT INTO review_sentiments (aspect, sentiment)
        VALUES (%s, %s)
        """

        # Process and insert the data
        for review in data:
            for item in review:
                if isinstance(item, tuple) and len(item) == 2:
                    aspect = item[0]
                    sentiment = item[1][0]  # We're using the sentiment label, not the score
                    cursor.execute(insert_query, (aspect, sentiment))

        # Commit the changes
        connection.commit()

        print(f"Successfully inserted {cursor.rowcount} rows.")

    except mysql.connector.Error as error:
        print(f"Error inserting data: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")