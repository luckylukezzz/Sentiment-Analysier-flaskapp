################ Establishing the database connection ################

import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

class DBConnection:
    def __init__(self, host=os.getenv('HOST'), user=os.getenv('USER'), password=os.getenv('PASSWORD'), database=os.getenv('DATABASE'), port=os.getenv('PORT')):
        self.conn = mysql.connector.connect(
           host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        ssl_disabled=False,
        )
        self.cursor = self.conn.cursor()
        print("Connection established successfully.")

    def clear_negative_keywords(self):
        # Execute the update query to set all negative_keywords to NULL
        self.cursor.execute("UPDATE products SET negative_keywords = NULL;")
        
        # Commit the transaction to save changes
        self.conn.commit()
        print("All negative keywords have been set to NULL.")

    def fetch_reviews(self):
        self.cursor.execute("SELECT review_id, parent_asin, text FROM reviews LIMIT 10")
        print("Fetching reviews...")
        return self.cursor.fetchall()

    #def fetch_keywords(self, review_ids):
    #   query = "SELECT keywords FROM reviews WHERE parent_asin = %s"
    #   #self.cursor.execute(query, (parent_asin,))
    #   print("Fetching keywords...")
    #   return self.cursor.fetchall()

    def fetch_features(self, parent_asin):
        query = "SELECT features FROM products WHERE parent_asin = %s"
        self.cursor.execute(query, (parent_asin,))
        print("Fetching features...")
        return self.cursor.fetchall()
    
    def update_keywords(self, review_ids, sentiment_aspects):
        for i in range(len(review_ids)):
            self.cursor.execute(
                "UPDATE reviews SET keywords = %s WHERE review_id = %s",
                (str(sentiment_aspects[i]), review_ids[i])
            )
        self.conn.commit()
        print("Keywords updated successfully.")

    def update_sentiment_scores(self, review_ids, overall_sentiments):
        for i in range(len(review_ids)):
            self.cursor.execute(
                "UPDATE reviews SET pos_score = %s, neu_score = %s, neg_score = %s, is_predicted = TRUE WHERE review_id = %s",
                (overall_sentiments[i][0], overall_sentiments[i][1], overall_sentiments[i][2], review_ids[i])
            )
        self.conn.commit()
        print("Sentiment scores updated successfully.")

    def fetch_negative_aspects(self, unique_parent_asins):    
        # Create the query with the appropriate number of placeholders
        query = "SELECT parent_asin, negative_keywords FROM products WHERE parent_asin IN ({})".format(
            ','.join(['%s'] * len(unique_parent_asins))
        )
        
        # Execute the query with the unique parent_asins
        self.cursor.execute(query, unique_parent_asins)
        print("Fetching negative aspects...")
        
        # Fetch results and organize them as a list of lists
        results = self.cursor.fetchall()
        negative_aspects = {result[0]: result[1].split(',') if result[1] else [] for result in results}
        
        return negative_aspects
    
    def update_negative_keywords(self, merged_aspects):
        for parent_asin, negative_keywords in merged_aspects.items():
            # Convert the list of negative keywords to a string in the format ['battery', 'screen']
            keywords_string = str(negative_keywords)
            
            # Execute the update query
            self.cursor.execute(
                "UPDATE products SET negative_keywords = %s WHERE parent_asin = %s",
                (keywords_string, parent_asin)
        )
        self.conn.commit()
        print("Negative keywords updated successfully.")


    def update_improvements(self, parent_asin, formatted_output):
        query = "UPDATE products SET improvements = %s WHERE parent_asin = %s"
        self.cursor.execute(query, (formatted_output, parent_asin))
        print("Updating improvements...")
        self.conn.commit()

    def close(self):
        self.conn.close()
        print("Connection closed.")
