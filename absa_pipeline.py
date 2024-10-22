import os
import process_reviews
from scraper.scrape_with_asin import scrape_reviews_final
import logging

logging.basicConfig(filename='pipeline.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')
api_token = os.getenv("GROQ_API_KEY")


def ABSA_pipeline(asin, api_token):
    #scrape_reviews_final(asin)

    processor = process_reviews.ReviewProcessor(api_token)
    processor.process()


#asin = 'B0CGTD5KVT'
asin = input("Enter asin: ")
logging.info("got asin" + str(asin))
logging.info("Starting ABSA pipeline")
ABSA_pipeline(asin, api_token)
logging.info("Finished ABSA pipeline")