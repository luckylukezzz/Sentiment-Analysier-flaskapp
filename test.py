import os
import process_reviews
 
parent_asin = 'B0B5FLX9WS'   # Example ASIN; replace with actual value

api_token = os.getenv("GROQ_API_KEY")

processor = process_reviews.ReviewProcessor(parent_asin, api_token)
processor.process()

