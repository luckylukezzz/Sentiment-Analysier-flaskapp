# Description: This file contains the ReviewProcessor class which is responsible for processing the reviews and generating suggestions for improvements.

from db_connection import DBConnection
from aspect_extraction import AspectExtractor, SentimentAspectAnalyzer
from llama_integration import LLaMAIntegration
from collections import Counter
import json

class ReviewProcessor:
    def __init__(self, api_token):
        self.api_token = api_token

    def process(self):
        # Establish DB connection
        db = DBConnection()
        print("connected")

        #db.clear_negative_keywords()
        #return

        try:
            # Fetch product titles
            # product_titles = db.fetch_product_titles()
            # print(product_titles)

            # Update the database with product names
            # db.update_product_names(product_titles)
            # print("Product names updated successfully.")

            # Fetch unprocessed reviews from database
            review_data = db.fetch_reviews()
            print(review_data)

            # Extract review IDs and texts
            review_ids, parent_asins, texts, timestamps = zip(*review_data)
            review_ids = list(review_ids)
            parent_asins = list(parent_asins)
            texts = list(texts)
            timestamps = list(timestamps)
            print("Data fetched successfully.")
            print("Texts: ",texts)

            # Initialize aspect extractor and sentiment analyzer
            aspect_extractor = AspectExtractor()
            sentiment_analyzer = SentimentAspectAnalyzer()

            # Extract aspects from reviews
            aspects = aspect_extractor.process_aspects(texts)
            print("Aspects: ",aspects)

            # Analyze sentiment of aspects and overall sentiment
            aspect_sentiments, overall_sentiments = sentiment_analyzer.analyze(texts, aspects)
            print("Aspect sentiments: ",aspect_sentiments)
            print("Overall sentiments: ",overall_sentiments)

            # Update the database with sentiment analysis results
            db.update_keywords(review_ids, aspect_sentiments)
            db.update_sentiment_scores(review_ids, overall_sentiments)

            # Update timestamp column in the reviews table
            db.update_timestamps(review_ids, timestamps)
            db.update_review_count(review_ids)

            # Filter out negative and positive aspects
            negative_aspects, positive_aspects = self.filter_aspects(aspect_sentiments)
            print("Negative aspects",negative_aspects)
            print("Positive aspects", positive_aspects)
            
            # Categorize positive, negative aspects by parent_asin and merge with existing aspects
            merged_negative_aspects, merged_positive_aspects, unique_parent_asins, new_changes = self.categorize_and_merge_aspects(negative_aspects, positive_aspects, parent_asins, db)

            # Update negative and positive keywords in the database
            print("back to main...")
            db.update_aspects(merged_negative_aspects, merged_positive_aspects, unique_parent_asins)
            print("Negative and positive aspects updated successfully.")
            print("New changes1", new_changes)

            # Filter out non-null new_changes and respective product details
            new_changes = {key: value for key, value in new_changes.items() if value}

            if not new_changes:
                print("No new changes to process.")
                return
            
            product_details = db.fetch_product_details(list(new_changes.keys()))  # Fetch for unique parent_asins
            print("Product Details:", product_details)
            print("New Changes2:", new_changes)


            # Integrate LLAMA for suggestions
            llama = LLaMAIntegration(self.api_token)

            # Merge the negative_aspects with the parent_asins
            # new_negative_aspects = dict(zip(unique_parent_asins, negative_aspects))

            # Get the differences between the new and old negative aspects
            # diff = {key: list(set(value) - set(old_aspects[key])) for key, value in new_negative_aspects.items()}
            # print("Differences:", diff)
            # print("New Negative Aspects:", new_negative_aspects)

            
            # Fetch product features
            # product_details = db.fetch_product_details(changed_parent_asins)  # Fetch for unique parent_asins
            # print("Product Details:", product_details)

            # Filter out non null differences and respective product details
            # diff = {key: value for key, value in diff.items() if value}
            # product_details = {key: value for key, value in product_details.items() if key in diff}

            # print(len(diff), len(product_details))
            # print("Filtered Differences:", diff)
            # print("Filtered Product Details:", product_details)

            # Generate suggestions using LLAMA
            for parent_asin, aspects in new_changes.items():
                suggestions = llama.generate_suggestions(aspects, product_details[parent_asin])
                print("suggestions:", suggestions)
                
                # formatted_suggestions = llama.format_suggestions(suggestions)
                # print("Formatted Suggestions:", formatted_suggestions)
                
                # Update the database with the formatted output
                db.update_improvements(parent_asin, suggestions)
                print(parent_asin, "Data updated successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            db.close()
            print("Connection closed.")

    def filter_aspects(self, aspect_sentiments):
        negative_aspects = []
        positive_aspects = []
        for i in range (len(aspect_sentiments)):
            review_aspects = aspect_sentiments[i]
            neg_aspects = []
            pos_aspects = []
            for aspect in review_aspects:
                if aspect[1] == "Negative":
                    neg_aspects.append(aspect[0])
                elif aspect[1] == "Positive":    
                    pos_aspects.append(aspect[0])
            negative_aspects.append(neg_aspects)
            positive_aspects.append(pos_aspects)
        return negative_aspects, positive_aspects
    

    def categorize_and_merge_aspects(self, negative_aspects, parent_asins, db):
        # Fetch existing negative aspects from the products table
        existing_negatives = db.fetch_negative_aspects(list(set(parent_asins)))  # Fetch for unique parent_asins
        already_existing_aspects = existing_negatives

        # Make a list of negative aspects for each parent_asin
        new_negative_aspects = dict(zip(parent_asins, negative_aspects))

        # Merge new negative aspects with existing ones
        for parent_asin, aspects in new_negative_aspects.items():
            if parent_asin in existing_negatives:
                merged_aspects = self.merge_aspects(aspects, existing_negatives[parent_asin])
            else:
                merged_aspects = aspects  # If no existing aspects, use new aspects directly
            existing_negatives[parent_asin] = merged_aspects

        print("Merged Negatives:", existing_negatives)

        return existing_negatives, already_existing_aspects
   

    def categorize_and_merge_aspects(self, negative_aspects, positive_aspects, parent_asins, db):
        unique_parent_asins = list(set(parent_asins))  # Get unique parent_asins
        # Fetch existing negative aspects (keyword: frequency) from the products table
        existing_negatives, existing_positives = db.fetch_aspects(unique_parent_asins)  # Fetch for unique parent_asins
        print("Existing Negatives:", existing_negatives)
        print("Existing Positives:", existing_positives)
        new_changes = {}

        # old_negative_aspects = existing_negatives.copy()  # Keep a copy of already existing aspects
        # old_positive_aspects = existing_positives.copy()

        # Make a dictionary of negative aspects for each parent_asin (new aspects in keyword: frequency format)
        new_negative_aspects = dict(zip(unique_parent_asins, negative_aspects))
        new_positive_aspects = dict(zip(unique_parent_asins, positive_aspects))

        print("New Negatives:", new_negative_aspects)
        print("New Positives:", new_positive_aspects)
        print("Passed here :)")

        
        # Merge new negative aspects with existing ones
        for parent_asin, aspects in new_negative_aspects.items():
            newly_added_aspects = []
            parent_asin_index = unique_parent_asins.index(parent_asin)  # Get the index of parent_asin in parent_asins
            print(parent_asin_index)

            if aspects is not None:
                print("hi")
                merged_aspects = existing_negatives[parent_asin_index]
                if merged_aspects is None:
                    merged_aspects = dict()  # Initialize as an empty dictionary if None
                print(aspects)
                for aspect in aspects:
                    if aspect in merged_aspects:
                        merged_aspects[aspect] += 1  # Increase frequency if keyword exists
                    else:
                        merged_aspects[aspect] = 1  # Add new keyword with frequency 1
                        newly_added_aspects.append(aspect)

                print("Merged Aspects:", merged_aspects)
                existing_negatives[parent_asin_index] = merged_aspects  # Update the existing_negatives
                new_changes[parent_asin] = newly_added_aspects
            
            else:
                existing_negatives[parent_asin_index] = existing_negatives[parent_asin_index]  # If no new aspects, keep the existing ones

        print("Merged Negatives:", existing_negatives)

                # Merge new negative aspects with existing ones
        for parent_asin, aspects in new_positive_aspects.items():
            parent_asin_index = unique_parent_asins.index(parent_asin)  # Get the index of parent_asin in parent_asins
            print(parent_asin_index)

            if aspects is not None:
                merged_aspects = existing_positives[parent_asin_index]
                if merged_aspects is None:
                    merged_aspects = {}  # Initialize as an empty dictionary if None

                for aspect in aspects:
                    if aspect in merged_aspects:
                        merged_aspects[aspect] += 1  # Increase frequency if keyword exists
                    else:
                        merged_aspects[aspect] = 1  # Add new keyword with frequency 1

                print("Merged Aspects:", merged_aspects)
                existing_positives[parent_asin_index] = merged_aspects  # Update the existing_negatives
            
            else:
                existing_positives[parent_asin_index] = existing_positives[parent_asin_index]  # If no new aspects, keep the existing ones

        print("Merged Positives:", existing_positives)
        return existing_negatives, existing_positives, unique_parent_asins, new_changes  # Return the updated dictionary

    

    # def categorize_and_merge_aspects(self, negative_aspects, positive_aspects, parent_asins, db):
    #     # Step 1: Get unique parent_asins
    #     unique_parent_asins = list(set(parent_asins))

    #     # Step 2: Fetch existing negative and positive aspects from the products table
    #     existing_negatives, existing_positives = db.fetch_aspects(unique_parent_asins)

    #     # Initialize dictionaries to hold new aspects, with default values being empty lists
    #     new_negative_aspects = {asin: [] for asin in unique_parent_asins}
    #     new_positive_aspects = {asin: [] for asin in unique_parent_asins}

    #     # Step 3: Map the new aspects to the corresponding parent_asins
    #     for i, parent_asin in enumerate(parent_asins):
    #         if negative_aspects[i]:  # Check if there are any negative aspects for this `parent_asin`
    #             new_negative_aspects[parent_asin].append(negative_aspects[i])  # Add the negative aspects
                
    #         if positive_aspects[i]:  # Check if there are any positive aspects for this `parent_asin`
    #             new_positive_aspects[parent_asin].append(positive_aspects[i])  # Add the positive aspects

    #     # Step 4: Merge new negative aspects with existing ones
    #     for parent_asin, aspects in new_negative_aspects.items():
    #         parent_asin_index = unique_parent_asins.index(parent_asin)  # Get the index of `parent_asin`
            
    #         # Fetch the existing negative aspects and check if it's a string
    #         merged_aspects = existing_negatives[parent_asin_index]

    #         if isinstance(merged_aspects, str):
    #             try:
    #                 # Parse the string into a dictionary
    #                 merged_aspects = json.loads(merged_aspects)
    #             except json.JSONDecodeError:
    #                 merged_aspects = {}  # Fallback to an empty dictionary if parsing fails
            
    #         if merged_aspects is None:
    #             merged_aspects = {}  # Initialize as an empty dictionary if None

    #         # Merge new negative aspects with their frequencies
    #         for aspect in aspects:
    #             if aspect in merged_aspects:
    #                 merged_aspects[aspect] += 1  # Increase frequency if keyword exists
    #             else:
    #                 merged_aspects[aspect] = 1  # Add new keyword with frequency 1

    #         # Update the existing negatives list
    #         existing_negatives[parent_asin_index] = merged_aspects

    #     # Step 5: Merge new positive aspects with existing ones (since positive aspects are lists)
    #     for parent_asin, new_aspects in new_positive_aspects.items():
    #         parent_asin_index = unique_parent_asins.index(parent_asin)  # Get the index of `parent_asin`
    #         existing_positive = existing_positives[parent_asin_index]

    #         if isinstance(existing_positive, str):
    #             try:
    #                 existing_positive = json.loads(existing_positive)
    #             except json.JSONDecodeError:
    #                 existing_positive = []  # Fallback to an empty list if parsing fails

    #         if existing_positive is None:
    #             existing_positive = []

    #         # Add new positive aspects and remove duplicates
    #         existing_positive.extend(new_aspects)
    #         existing_positive = list(set(existing_positive))  # Remove duplicates

    #         # Update the existing positives list
    #         existing_positives[parent_asin_index] = existing_positive

    #     print("Merged Negatives:", existing_negatives)
    #     print("Merged Positives:", existing_positives)

    #     # Return the updated aspects
    #     return existing_negatives, existing_positives, unique_parent_asins

    def merge_aspects(self, negative_aspects, existing_negatives):
        # Combine new and existing aspects, removing duplicates
        merged_aspects = list(set(existing_negatives + negative_aspects))
        return merged_aspects



#-------main.py--------------------------
#from process_reviews import ReviewProcessor

#if __name__ == "__main__":
#   parent_asin = 'B07CQNF813'  # Example ASIN; replace with actual value
#   api_token = os.getenv("GROQ_API_KEY")

#   processor = ReviewProcessor(parent_asin, api_token)
#   processor.process()

