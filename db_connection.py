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
        self.cursor.execute("SELECT review_id, parent_asin, text, timestamp FROM reviews WHERE is_predicted IS NULL LIMIT 5")
        print("Fetching reviews...")
        return self.cursor.fetchall()

    def fetch_keywords(self, parent_asin):
       query = "SELECT keywords FROM reviews WHERE parent_asin = %s"
       self.cursor.execute(query, (parent_asin,))
       print("Fetching keywords...")
       return self.cursor.fetchall()
    
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
                details_dict[parent_asin] = details_json  

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

    def update_emotions(self, review_ids, emotions, scores):
        for i in range(len(review_ids)):
            # Ensure that score is a float, and emotion is a string
            self.cursor.execute(
                "UPDATE reviews SET emotion = %s, emo_score = %s WHERE review_id = %s",
                (emotions[i], float(scores[i]), review_ids[i])  # Ensure score is converted to float
            )
        self.conn.commit()
        print("Emotions updated successfully.")

    def update_aspect_scores(self, review_ids, aspect_results):
        for i in range(len(review_ids)):
            self.cursor.execute(
                "UPDATE reviews SET aspect_quality = %s, quality_score = %s, aspect_price = %s, price_score = %s, aspect_shipping = %s, shipping_score = %s, aspect_customer_service = %s, customer_service_score = %s, aspect_warranty = %s, warranty_score = %s WHERE review_id = %s",
                (
                    aspect_results[i]['aspect_quality'], aspect_results[i]['quality_score'],
                    aspect_results[i]['aspect_price'], aspect_results[i]['price_score'],
                    aspect_results[i]['aspect_shipping'], aspect_results[i]['shipping_score'],
                    aspect_results[i]['aspect_customer_service'], aspect_results[i]['customer_service_score'],
                    aspect_results[i]['aspect_warranty'], aspect_results[i]['warranty_score'],
                    review_ids[i]
                )
            )
        self.conn.commit()
        print("Aspect scores updated successfully.")

    def update_lime_explanations(self, review_ids, lime_explanations):
        for i in range(len(review_ids)):
            self.cursor.execute(
                "UPDATE reviews SET lime = %s WHERE review_id = %s",
                (json.dumps(lime_explanations[i]), review_ids[i])
            )
        self.conn.commit()
        print("LIME explanations updated successfully.")

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

    def update_review_count(self, review_ids):
        # Get parent_asin of each review and increase the review_count of each parent_asin in products table by one
        for review_id in review_ids:
            self.cursor.execute(
                "SELECT parent_asin FROM reviews WHERE review_id = %s",
                (review_id,)
            )
            parent_asin = self.cursor.fetchone()[0]
            self.cursor.execute(    
                "UPDATE products SET review_count = review_count + 1 WHERE parent_asin = %s",
                (parent_asin,)
            )
        self.conn.commit()
        print("Review count updated successfully.")

    def fetch_aspects(self, unique_parent_asins):
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

        # Iterate over the results and deserialize the negative and positive keywords from JSON
        for result in results:
            try:
                # Deserialize the negative_keywords field
                negative_keywords = json.loads(result[1]) if result[1] else {}
            except json.JSONDecodeError:
                negative_keywords = {}  

            try:
                positive_keywords = json.loads(result[2]) if result[2] else {}
            except json.JSONDecodeError:
                positive_keywords = {}  

            # Append the deserialized dictionaries to the respective lists
            existing_negatives.append(negative_keywords)
            existing_positives.append(positive_keywords)

        print("Positive aspects (dictionaries):", existing_positives)
        print("Negative aspects (dictionaries):", existing_negatives)

        # Return the lists of dictionaries for negative and positive aspects
        return existing_negatives, existing_positives
    

    def update_aspects(self, merged_negative_aspects, merged_positive_aspects, unique_parent_asins):
        for i in range(len(unique_parent_asins)):
            parent_asin = unique_parent_asins[i]
            negative_keywords = merged_negative_aspects[i]
            positive_keywords = merged_positive_aspects[i]
            
            # Convert the dictionaries of negative and positive keywords to JSON strings
            negative_keywords_json = json.dumps(negative_keywords)
            positive_keywords_json = json.dumps(positive_keywords)
            
            # Execute the update query with the JSON strings
            self.cursor.execute(
                "UPDATE products SET negative_keywords = %s, positive_keywords = %s WHERE parent_asin = %s",
                (negative_keywords_json, positive_keywords_json, parent_asin)
            )
        
        # Commit the transaction to apply the changes
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

    def update_improvements(self, parent_asin, suggestions_list):
        # Fetch the current improvements for the given parent_asin
        query = "SELECT improvements FROM products WHERE parent_asin = %s"
        self.cursor.execute(query, (parent_asin,))
        result = self.cursor.fetchone()
        print(result)
        
        # Check if the improvements column is NULL or empty
        current_improvements = result[0]
        print(current_improvements)
        
        if current_improvements is None:
            # Initialize as an empty list if NULL
            current_improvements_list = []
        else:
            # Parse the existing improvements as a list from the stored JSON string
            current_improvements_list = json.loads(current_improvements)
        
        print(current_improvements_list)
        # Append new suggestions to the existing improvements list
        current_improvements_list.extend(suggestions_list)
        
        # Convert the list back to a JSON string
        updated_improvements = json.dumps(current_improvements_list)
        print(updated_improvements)
        # Update the improvements column with the new suggestions list
        update_query = "UPDATE products SET improvements = %s WHERE parent_asin = %s"
        self.cursor.execute(update_query, (updated_improvements, parent_asin))
        
        # Commit the changes
        self.conn.commit()
        
        print("Improvements updated successfully.")

    def close(self):
        self.conn.close()
        print("Connection closed.")
