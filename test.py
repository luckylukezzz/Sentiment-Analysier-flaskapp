import os
import process_reviews
 
#parent_asin = 'B07CQNF813'   # Example ASIN; replace with actual value

api_token = os.getenv("GROQ_API_KEY")

#enter ASIN
ASIN = input()

processor = process_reviews.ReviewProcessor(api_token)
processor.process(ASIN)