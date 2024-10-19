import mysql.connector
from ABSA_model import AspectExtractor, SentimentAspectAnalyzer
import os

def establish_db_connection(host, user, password, database):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        print("Connected to MySQL")
        cursor.execute("SELECT review_id, text FROM reviews")
        data = cursor.fetchall()
        return data, conn, cursor
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None, None, None

def store_results(cursor, conn, sentiment_aspect, review_ids):
    for i in range(len(review_ids)):
        aspect_lst = []
        for j in range(0, len(sentiment_aspect[i]), 2):
            aspect_lst.append(list((sentiment_aspect[i][j], sentiment_aspect[i][j+1][0])))
        cursor.execute(
            "UPDATE reviews SET keywords = %s WHERE review_id = %s",
            (str(aspect_lst), review_ids[i])
        )
    conn.commit()
    print("Data updated successfully.")

def main():
    data, conn, cursor = establish_db_connection(user=os.getenv('USER'), password=os.getenv('PASSWORD'), host=os.getenv('HOST'), database=os.getenv('DATABASE'))
    if not data:
        return

    # Separate into two lists
    review_ids, texts = zip(*data)

    # Convert the zip object into lists
    review_ids = list(review_ids)
    texts = list(texts)

    # Establishing the pipeline
    aspect_extractor = AspectExtractor()
    sentiment_aspect_analyzer = SentimentAspectAnalyzer()

    # Extracting aspects
    aspects = aspect_extractor.process_aspects(texts)

    # Analyzing sentiment
    sentiment_aspect = sentiment_aspect_analyzer.analyze(texts, aspects)

    # Storing the results
    store_results(cursor, conn, sentiment_aspect, review_ids)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
