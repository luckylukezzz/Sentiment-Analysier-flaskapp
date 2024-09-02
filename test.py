from db_connection import DBConnection
from aspect_extraction import AspectExtractor, SentimentAspectAnalyzer
from llama_integration import LLaMAIntegration
import os
import process_reviews


parent_asin = 'B075NVNBCW'  # Example ASIN; replace with actual value
api_token = os.getenv("GROQ_API_KEY")

processor = process_reviews.ReviewProcessor(parent_asin, api_token)
processor.process()

