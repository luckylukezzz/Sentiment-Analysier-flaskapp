from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import mysql.connector
import os
from scraper.scrape_with_asin import scrape_reviews_final
from threading import Thread
import process_reviews

load_dotenv()

app = Flask(__name__)
CORS(app)

# Load environment variables
host = os.getenv('HOST')
port = os.getenv('PORT')
database = os.getenv('DATABASE')
user = os.getenv('USER')
password = os.getenv('PASSWORD')

# Database connection
db = mysql.connector.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database,
    ssl_disabled=False,
    connection_timeout=1000,
)
cursor = db.cursor(dictionary=True)

api_token = os.getenv("GROQ_API_KEY")
import subprocess
from multiprocessing import Process

def run_scraper(asin):
    try:
        scrape_reviews_final(asin)
        processor_review = process_reviews.ReviewProcessor(api_token)
        processor_review.process()
        print(f"Task completed for ASIN: {asin}")
    except Exception as e:
        print(f"Error occurred while processing ASIN {asin}: {str(e)}")

@app.route('/run_task', methods=['POST'])
def run_task():
    data = request.json
    asin = data.get('asin')
    
    if not asin:
        return jsonify({"error": "ASIN is required"}), 400
    
    # Run the scraper in a separate process
    process = Process(target=run_scraper, args=(asin,))
    process.start()

    return jsonify({"message": f"Task started for ASIN: {asin}"}), 202

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the ASIN Task Runner API"}), 200

if __name__ == '__main__':
    app.run(debug=True,port=8080)

