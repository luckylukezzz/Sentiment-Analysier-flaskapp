################ Establishing the database connection and database updates ################

import mysql.connector
from dotenv import load_dotenv
from datetime import datetime
import os
import json

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

    def fetch_product_titles(self):
        self.cursor.execute("SELECT parent_asin, title FROM products")
        print("Fetching product titles...")
        return self.cursor.fetchall()
    
    def update_product_names(self, product_titles):
        for parent_asin, title in product_titles:
            # Extract the text up to the first comma
            name_up_to_comma = title.split(',')[0].strip()
            self.cursor.execute(
                "UPDATE products SET product_name = %s WHERE parent_asin = %s",
                (name_up_to_comma, parent_asin)
            )
        self.conn.commit()

    def fetch_reviews(self):
        self.cursor.execute("SELECT review_id, parent_asin, text, timestamp FROM reviews WHERE is_predicted IS NOT NULL LIMIT 20")
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

    def update_timestamps(self, review_ids, timestamps):
        for i in range (len(review_ids)):
            # # Convert the Unix timestamp (in milliseconds) to a datetime object
            # review_datetime = datetime.fromtimestamp(timestamps[i] / 1000.0)
            # # Format it to "Month, Year"
            # review_date_str = review_datetime.strftime("%B, %Y")
            # self.cursor.execute(
            #     "UPDATE reviews SET review_date = %s WHERE review_id = %s",
            # (review_date_str, review_ids[i])
            # )
            # Convert the Unix timestamp (in milliseconds) to a datetime object
            review_datetime = datetime.fromtimestamp(timestamps[i] / 1000.0)
            # Format it to "YYYY-MM-DD"
            review_date_str = review_datetime.strftime("%Y-%m-%d")
            self.cursor.execute(
                 "UPDATE reviews SET review_date = %s WHERE review_id = %s",
             (review_date_str, review_ids[i])
             )
            
        self.conn.commit()
        print("Review_dates updated successfully.")

    # def fetch_negative_aspects(self, unique_parent_asins):    
    #     # Create the query with the appropriate number of placeholders
    #     query = "SELECT parent_asin, negative_keywords FROM products WHERE parent_asin IN ({})".format(
    #         ','.join(['%s'] * len(unique_parent_asins))
    #     )
        
    #     # Execute the query with the unique parent_asins
    #     self.cursor.execute(query, unique_parent_asins)
    #     print("Fetching negative aspects...")
        
    #     # Fetch results and organize them as a list of lists
    #     results = self.cursor.fetchall()
    #     print("Results:", results)
    #     negative_aspects = {result[0]: result[1].split(',') if result[1] else [] for result in results}
        
    #     return negative_aspects
    
    def fetch_aspects(self, unique_parent_asins):    
        # Create the query with the appropriate number of placeholders
        query = "SELECT parent_asin, negative_keywords, positive_keywords FROM products WHERE parent_asin IN ({})".format(
            ','.join(['%s'] * len(unique_parent_asins))
        )
        
        # Execute the query with the unique parent_asins
        self.cursor.execute(query, unique_parent_asins)
        print("Fetching negative and positive aspects...")
        
        # Fetch results and organize them as a list of lists
        results = self.cursor.fetchall()
        print("Results:", results)

        existing_negatives = []
        existing_positives = []
        for result in results:
            existing_negatives.append(result[1])
            existing_positives.append(result[2])

        #negative_aspects = {result[0]: result[1].split(',') if result[1] else [] for result in results}
        print("Positive aspects:", existing_positives)
        print("Negative aspects:", existing_negatives)
        
        return existing_negatives, existing_positives # These are lists of dictionaries
    
    # def fetch_positive_aspects(self, unique_parent_asins):
    #     # Create the query with the appropriate number of placeholders
    #     query = "SELECT parent_asin, positive_keywords FROM products WHERE parent_asin IN ({})".format(
    #         ','.join(['%s'] * len(unique_parent_asins))
    #     )
        
    #     # Execute the query with the unique parent_asins
    #     self.cursor.execute(query, unique_parent_asins)
    #     print("Fetching positive aspects...")
        
    #     # Fetch results and organize them as a list of lists
    #     results = self.cursor.fetchall()
    #     positive_aspects = {result[0]: result[1].split(',') if result[1] else [] for result in results}
        
    #     return positive_aspects
    
    def update_aspects(self, merged_negative_aspects, merged_positive_aspects, unique_parent_asins):
        for i in range (len(unique_parent_asins)):
            parent_asin = unique_parent_asins[i]
            negative_keywords = merged_negative_aspects[i]
            positive_keywords = merged_positive_aspects[i]
            # Convert the list of negative keywords to a string in the format ['battery', 'screen']
            negative_keywords_string = str(negative_keywords)
            positive_keywords_string = str(positive_keywords)
            # Execute the update query
            self.cursor.execute(
                "UPDATE products SET negative_keywords = %s, positive_keywords = %s WHERE parent_asin = %s",
                (negative_keywords_string, positive_keywords_string, parent_asin)
            )
        # for parent_asin, negative_keywords in merged_negative_aspects.items():
        #     # Convert the list of negative keywords to a string in the format ['battery', 'screen']
        #     keywords_string = str(negative_keywords)
            
        #     # Execute the update query
        #     self.cursor.execute(
        #         "UPDATE products SET negative_keywords = %s WHERE parent_asin = %s",
        #         (str(keywords_string), parent_asin)
        # )
        self.conn.commit()
        print("Negative and positive keywords updated successfully.")

        # for parent_asin, positive_keywords in merged_positive_aspects.items():
        #     # Convert the list of positive keywords to a string in the format ['battery', 'screen']
        #     keywords_string = str(positive_keywords)
            
        #     # Execute the update query
        #     self.cursor.execute(
        #         "UPDATE products SET positive_keywords = %s WHERE parent_asin = %s",
        #         (keywords_string, parent_asin)
        #     )
        # self.conn.commit()
        # print("Positive keywords updated successfully.")

    def update_improvements(self, parent_asin, formatted_output):
        query = "UPDATE products SET negative_keywords = CONCAT(IFNULL(negative_keywords, ''), %s) WHERE parent_asin = %s"
        self.cursor.execute(query, (formatted_output, parent_asin))
        print("Updating improvements...")
        self.conn.commit()

    def close(self):
        self.conn.close()
        print("Connection closed.")
