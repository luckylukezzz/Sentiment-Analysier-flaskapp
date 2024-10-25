# Description: This file contains the ReviewProcessor class which is responsible for processing the reviews and generating suggestions for improvements.

from db_connection import DBConnection
from aspect_extraction import AspectExtractor, SentimentAspectAnalyzer
from llama_integration import LLaMAIntegration
from emotion_db_fill import EmotionExtractor
from aspect_score_generator import AspectScoreGenerator
from lime_explainer import LimeExplainer
from emotion_db_fill import EmotionExtractor
from aspect_score_generator import AspectScoreGenerator
from lime_explainer import LimeExplainer
from collections import Counter
from collections import defaultdict
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
            emotion_analyzer = EmotionExtractor()
            aspect_score_generator = AspectScoreGenerator()
            lime_explainer = LimeExplainer()
            emotion_analyzer = EmotionExtractor()
            aspect_score_generator = AspectScoreGenerator()
            lime_explainer = LimeExplainer()

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

            # Update emotions in the database
            emotion, score = emotion_analyzer.extract_emotions(texts)
            print("Emotion:", emotion)
            print("Score:", score)
            db.update_emotions(review_ids, emotion, score)

            # Update the aspect scores in the database
            aspects = ['quality', 'price', 'shipping', 'Customer Service', 'Warranty']
            aspect_results = aspect_score_generator.extract_aspect_scores(texts, aspects)
            print("Aspect Results:", aspect_results)
            db.update_aspect_scores(review_ids, aspect_results)

            # Update the lime explanations in the database
            # lime_results = lime_explainer.explain_review(texts, aspect_results)
            # print("Lime Results:", lime_results)
            # db.update_lime_explanations(review_ids, lime_results)
    
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
        for i in range (len(aspect_sentiments)):  # No. of reviews
            review_aspects = aspect_sentiments[i] # Aspect sentiments for a single review
            neg_aspects = []
            pos_aspects = []
            for aspect in review_aspects:
                if aspect[1] == "Negative":
                    neg_aspects.append(aspect[0])
                elif aspect[1] == "Positive":    
                    pos_aspects.append(aspect[0])
            negative_aspects.append(neg_aspects) # Appending a list of negative aspects for each review
            positive_aspects.append(pos_aspects) # Appending a list of positive aspects for each review
        return negative_aspects, positive_aspects
    

    def categorize_and_merge_aspects(self, negative_aspects, positive_aspects, parent_asins, db):
        unique_parent_asins = list(set(parent_asins))  # Get unique parent_asins
        print("*Unique Parent ASINs:", unique_parent_asins)
        print(negative_aspects)
        print(positive_aspects)
        # Fetch existing negative aspects (keyword: frequency) from the products table
        existing_negatives, existing_positives = db.fetch_aspects(unique_parent_asins)  # Fetch for unique parent_asins
        print("Existing Negatives:", existing_negatives)
        print("Existing Positives:", existing_positives)
        new_changes = {}

        # Make a dictionary of negative aspects for each parent_asin (new aspects in keyword: frequency format)
        new_positive_aspects, new_negative_aspects = self.merge_lists(unique_parent_asins, positive_aspects, negative_aspects)

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

    
    def merge_lists(self, parent_asins, pos_lst, neg_lst):
        positive_asin_aspects = defaultdict(list)
        negative_asin_aspects = defaultdict(list)

        print("pos_lst:", pos_lst)
        print("neg_lst:", neg_lst)

        # Iterate over the parent_asins, positive and negative aspects
        for asin, pos_aspects, neg_aspects in zip(parent_asins, pos_lst, neg_lst):
            # Only add to dictionaries if the lists are not empty
            if pos_aspects:
                positive_asin_aspects[asin].extend(pos_aspects)
            if neg_aspects:
                negative_asin_aspects[asin].extend(neg_aspects)

        
        positive_asin_aspects = dict(positive_asin_aspects)
        negative_asin_aspects = dict(negative_asin_aspects)
        return positive_asin_aspects, negative_asin_aspects
    

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

