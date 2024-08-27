# Description: This file contains the ReviewProcessor class which is responsible for processing the reviews and generating suggestions for improvements.

from db_connection import DBConnection
from aspect_extraction import AspectExtractor, SentimentAspectAnalyzer
from llama_integration import LLaMAIntegration

class ReviewProcessor:
    def __init__(self, parent_asin, api_token):
        self.parent_asin = parent_asin
        self.api_token = api_token

    def process(self):
        print("running process")
        # Establish DB connection
        db = DBConnection()
        print("connected")

        try:
            # Fetch reviews and keywords
            review_data = db.fetch_reviews()
            print("fetch complete")
            keywords_data = db.fetch_keywords(self.parent_asin)
            features_data = db.fetch_features(self.parent_asin)

            # Extract review IDs and texts
            review_ids, texts = zip(*review_data)
            review_ids = list(review_ids)
            texts = list(texts)

            # Initialize aspect extractor and sentiment analyzer
            aspect_extractor = AspectExtractor()
            sentiment_analyzer = SentimentAspectAnalyzer()

            # Extract aspects and analyze sentiment
            aspects = aspect_extractor.process_aspects(texts)
            sentiment_aspect = sentiment_analyzer.analyze(texts, aspects)

            # Prepare the negative keywords list
            negative_keywords = []
            for item in keywords_data:
                if item[0] is not None:
                    lists = eval(f'[{item[0]}]')
                    for keyword in lists:
                        if keyword[1] == 'negative':
                            negative_keywords.append(keyword[0])

            # Integrate LLAMA for suggestions
            llama = LLaMAIntegration(self.api_token)
            suggestions = llama.generate_suggestions(negative_keywords, features_data)
            formatted_suggestions = llama.format_suggestions(suggestions)

            # Update the database with the formatted output
            db.update_improvements(self.parent_asin, formatted_suggestions)
            print("Data updated successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            db.close()


#-------main.py--------------------------
#from process_reviews import ReviewProcessor

#if __name__ == "__main__":
#   parent_asin = 'B07CQNF813'  # Example ASIN; replace with actual value
#   api_token = os.getenv("GROQ_API_KEY")

#   processor = ReviewProcessor(parent_asin, api_token)
#   processor.process()

