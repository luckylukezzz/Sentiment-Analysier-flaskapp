import os
import process_reviews
from scraper.scrape_with_asin import scrape_reviews_final

api_token = os.getenv("GROQ_API_KEY")


def ABSA_pipeline(asin, api_token):
    scrape_reviews_final(asin)

    processor = process_reviews.ReviewProcessor(api_token)
    processor.process()


asin = 'B0CGTD5KVT'

ABSA_pipeline(asin, api_token)
