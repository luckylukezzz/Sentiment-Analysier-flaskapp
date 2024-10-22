# from flask import Flask, request, jsonify
# import mysql.connector
# from mysql.connector import Error
# from dotenv import load_dotenv
# from flask_cors import CORS
# import os
# import process_reviews
# from scraper.scrape_with_asin import scrape_reviews_final
# from celery import Celery
#
# load_dotenv()
#
# app = Flask(__name__)
# CORS(app)
#
# # Load environment variables
# host = os.getenv('HOST')
# port = os.getenv('PORT')
# database = os.getenv('DATABASE')
# user = os.getenv('USER')
# password = os.getenv('PASSWORD')
#
# # Database connection
# db = mysql.connector.connect(
#     host=host,
#     port=port,
#     user=user,
#     password=password,
#     database=database,
#     ssl_disabled=False,
#     connection_timeout=1000,
# )
# cursor = db.cursor(dictionary=True)
#
# api_token = os.getenv("GROQ_API_KEY")
#
# # Celery configuration
# celery = Celery(
#     app.name,
#     broker='redis://localhost:6379/0',
#     backend='redis://localhost:6379/0'
# )
# celery.conf.update(app.config)
#
#
# @celery.task
# def async_scrape_reviews(asin):
#     scrape_reviews_final(asin)
#     return f"Scraping completed for ASIN: {asin}"
#
#
# @app.route('/scrape', methods=['POST'])
# def start_scrape():
#     data = request.json
#     if not data or 'asin' not in data:
#         return jsonify({"error": "ASIN is required"}), 400
#
#     asin = data['asin']
#     task = async_scrape_reviews.delay(asin)
#     return jsonify({"message": "Scraping task started", "task_id": str(task.id)}), 202
#
#
# @app.route('/task/<task_id>', methods=['GET'])
# def get_task_status(task_id):
#     task = async_scrape_reviews.AsyncResult(task_id)
#     if task.state == 'PENDING':
#         response = {
#             'state': task.state,
#             'status': 'Task is waiting for execution'
#         }
#     elif task.state != 'FAILURE':
#         response = {
#             'state': task.state,
#             'status': str(task.info)
#         }
#     else:
#         response = {
#             'state': task.state,
#             'status': str(task.info)
#         }
#     return jsonify(response)
#
#
# if __name__ == '__main__':
#     app.run(debug=True)