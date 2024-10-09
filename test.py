import os
import process_reviews
#from scraper.reviews_scrape_final import scrape_reviews

#parent_asin = 'B07CQNF813'   # Example ASIN; replace with actual value

api_token = os.getenv("GROQ_API_KEY")

#enter ASIN
#ASIN = input("Enter ASIN")
#scrape_reviews(ASIN)

processor = process_reviews.ReviewProcessor(api_token)
processor.process()
