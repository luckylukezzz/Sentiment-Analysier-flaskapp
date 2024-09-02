# Description: This file contains the ReviewProcessor class which is responsible for processing the reviews and generating suggestions for improvements.

from db_connection import DBConnection
from aspect_extraction import AspectExtractor, SentimentAspectAnalyzer
from llama_integration import LLaMAIntegration

class ReviewProcessor:
    def __init__(self, parent_asin, api_token):
        self.parent_asin = parent_asin
        self.api_token = api_token

    def process(self):
        # Establish DB connection
        db = DBConnection()

        #db.clear_negative_keywords()
        #return

        try:
            # Fetch reviews and keywords
            review_data = db.fetch_reviews()

            # Extract review IDs and texts
            print(review_data)
            review_ids, parent_asins, texts = zip(*review_data)
            review_ids = list(review_ids)
            parent_asins = list(parent_asins)
            texts = list(texts)
            print("Data fetched successfully.")
            print(texts)

            # Initialize aspect extractor and sentiment analyzer
            aspect_extractor = AspectExtractor()
            sentiment_analyzer = SentimentAspectAnalyzer()

            # Extract aspects and analyze sentiment
            aspects = aspect_extractor.process_aspects(texts)
            print(aspects)

            aspect_sentiments, overall_sentiments = sentiment_analyzer.analyze(texts, aspects)
            print(aspect_sentiments, overall_sentiments)
            db.update_keywords(review_ids, aspect_sentiments)
            db.update_sentiment_scores(review_ids, overall_sentiments)

            # Filter out negative aspects
            negative_aspects = self.filter_negative_aspects(aspect_sentiments)
            print(negative_aspects)
            
            # Categorize negative aspects by parent_asin and merge with existing aspects
            merged_aspects, old_aspects = self.categorize_and_merge_aspects(negative_aspects, parent_asins, db)
            print("Merged Aspects:", merged_aspects)

            # Update negative keywords in the database
            db.update_negative_keywords(merged_aspects)

            # Integrate LLAMA for suggestions
            llama = LLaMAIntegration(self.api_token)

            # Merge the negative_aspects with the parent_asins
            parent_asins = list(set(parent_asins))  # Get unique parent_asins
            new_negative_aspects = dict(zip(parent_asins, negative_aspects))

            # Get the differences between the new and old negative aspects
            diff = {key: list(set(value) - set(old_aspects[key])) for key, value in new_negative_aspects.items()}
            print("Differences:", diff)
            print("New Negative Aspects:", new_negative_aspects)
            
            # Fetch product features
            product_details = db.fetch_product_details(list(set(parent_asins)))  # Fetch for unique parent_asins
            print("Product Details:", product_details)

            # Filter out non null differences and respective product details
            diff = {key: value for key, value in diff.items() if value}
            product_details = {key: value for key, value in product_details.items() if key in diff}

            # Generate suggestions using LLAMA
            for parent_asin, aspects in diff.items():
                suggestions = llama.generate_suggestions(aspects, product_details[parent_asin])
                formatted_suggestions = llama.format_suggestions(suggestions)

                # Update the database with the formatted output
                db.update_improvements(self.parent_asin, formatted_suggestions)
                print(parent_asin, "Data updated successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            db.close()
            print("Connection closed.")

    def filter_negative_aspects(self, aspect_sentiments):
        negative_aspects = []
        for i in range (len(aspect_sentiments)):
            review_aspects = aspect_sentiments[i]
            neg_aspects = []
            neg_aspects = [aspect[0] for aspect in review_aspects if aspect[1] == "Negative"]
            negative_aspects.append(neg_aspects)
        return negative_aspects

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

