################ Establishing the database connection and database updates ################

import mysql.connector
from dotenv import load_dotenv
import os
import json
import re
import ast

load_dotenv()


class DBConnection:
    # Establish the database connection       
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
        print("Connection established successfully.")

    def clear_negative_keywords(self):
        # Execute the update query to set all negative_keywords to NULL
        self.cursor.execute("UPDATE products SET negative_keywords = NULL;")
        
        # Commit the transaction to save changes
        self.conn.commit()
        print("All negative keywords have been set to NULL.")

    def fetch_reviews(self):
        self.cursor.execute("SELECT review_id, parent_asin, text FROM reviews WHERE is_predicted IS NULL LIMIT 10")
        print("Fetching reviews...")
        return self.cursor.fetchall()

    #def fetch_keywords(self, review_ids):
    #   query = "SELECT keywords FROM reviews WHERE parent_asin = %s"
    #   #self.cursor.execute(query, (parent_asin,))
    #   print("Fetching keywords...")
    #   return self.cursor.fetchall()
    
    def fetch_product_details(self, parent_asins):
        parent_asins_tuple = tuple(set(parent_asins))  # Remove duplicates

        # Construct and execute the query
        placeholders = ','.join(['%s'] * len(parent_asins_tuple))
        query = f"SELECT parent_asin, details FROM products WHERE parent_asin IN ({placeholders})"
        self.cursor.execute(query, parent_asins_tuple)
        results = self.cursor.fetchall()

        details_dict = {}
        for result in results:
            parent_asin = result[0]
            details_json = result[1]
            
            # Attempt to decode JSON, handle if it's already a string
            try:
                details_dict[parent_asin] = json.loads(details_json)
            except json.JSONDecodeError:
                details_dict[parent_asin] = details_json  # Assume it's a string if not JSON

        return details_dict

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
        print("Results:", results)
        negative_aspects = {result[0]: result[1].split(',') if result[1] else [] for result in results}
        print("neg aspects", negative_aspects)
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
        query = "UPDATE products SET negative_keywords = CONCAT(IFNULL(negative_keywords, ''), %s) WHERE parent_asin = %s"
        self.cursor.execute(query, (formatted_output, parent_asin))
        print("Updating improvements...")
        self.conn.commit()

    def close(self):
        self.conn.close()
        print("Connection closed.")

    def extract_aspects(data):
        """
        Extracts and cleans the aspects from a list of tuples.
        """
        aspects = []

        for _, aspect_string in data:
            if aspect_string:
                # Remove unnecessary escape characters
                cleaned_string = re.sub(r'\\+', '', aspect_string)
                try:
                    # Safely convert the cleaned string back to a Python list
                    aspects.append(ast.literal_eval(cleaned_string))
                except (SyntaxError, ValueError):
                    # Skip if the cleaned string cannot be parsed
                    continue

        return aspects