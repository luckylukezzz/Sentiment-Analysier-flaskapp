import mysql.connector
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import random
import csv
from datetime import datetime
import os
from dotenv import load_dotenv
import logging
import re
import time

# Set up logging
logging.basicConfig(filename='review_scrape.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

load_dotenv()

host = os.getenv('HOST')
database = os.getenv('DATABASE')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
port = os.getenv('PORT')

def clean_text(text):
    # Remove emojis and other problematic characters
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            ssl_disabled=False,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )
        logging.info("Database connection established successfully")
        return conn
    except mysql.connector.Error as err:
        logging.error(f"Database connection failed: {err}")
        return None

def reviews_into_sql(asin, max_pages=15, delay=5):
    conn = get_db_connection()
    if not conn:
        return

    cursor = conn.cursor()
    
    try:
        page = 1
        total_reviews = 0
        duplicate_count = 0
        reviews = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080}
            )
            page_instance = context.new_page()
            
            while page <= max_pages:
                url = f"http://www.amazon.com/dp/product-reviews/{asin}?pageNumber={page}"
                
                try:
                    # Navigate to the page and wait for content to load
                    page_instance.goto(url)
                    page_instance.wait_for_load_state('networkidle')
                    
                    # Get the page content
                    content = page_instance.content()
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    parent_asin = asin
                    review_blocks = soup.find_all('div', class_='a-row a-spacing-none')

                    if not review_blocks:
                        logging.info(f"No reviews found on page {page}. Ending scraping.")
                        break

                    page_reviews = 0

                    for review_block in review_blocks:
                        try:
                            rating = float(review_block.find('span', class_='a-icon-alt').text.split(' ')[0])
                            review_title = review_block.find('span', class_=None).text

                            review_date_full_str = review_block.find('span', {'data-hook': 'review-date'}).text
                            review_date_str = review_date_full_str.split('on ')[-1]
                            review_date = datetime.strptime(review_date_str, '%B %d, %Y')
                            review_date_ms = int(review_date.timestamp() * 1000)

                            review_body = review_block.find('span', {'data-hook': 'review-body'}).text
                            review_text = clean_text(f"{review_title}. {review_body}")

                            user_id = review_block.find('a', class_='a-profile')['href'].split('.')[2].split('/')[0]

                            review = {
                                'rating': rating,
                                'text': review_text,
                                'parent_asin': parent_asin,
                                'user_id': user_id,
                                'timestamp': review_date_ms,
                            }

                            check_stmt = """
                            SELECT COUNT(*) FROM reviews 
                            WHERE user_id = %s AND timestamp = %s
                            """
                            cursor.execute(check_stmt, (user_id, review_date_ms))
                            if cursor.fetchone()[0] > 0:
                                logging.info(f"Skipped duplicate review: user_id={user_id}, timestamp={review_date_ms}")
                                duplicate_count += 1
                                continue

                            reviews.append(review)
                            # Insert the review if it's not a duplicate
                            insert_stmt = """
                            INSERT INTO reviews (rating, text, parent_asin, user_id, timestamp)
                            VALUES (%s, %s, %s, %s, %s)
                            """
                            data = (rating, review_text, parent_asin, user_id, review_date_ms)

                            cursor.execute(insert_stmt, data)
                            conn.commit()
                            logging.info(f"Inserted new review: user_id={user_id}, timestamp={review_date_ms}")
                            page_reviews += 1
                            total_reviews += 1

                        except AttributeError as e:
                            logging.warning(f"Skipped a review due to AttributeError: {e}")
                            continue
                        except mysql.connector.Error as err:
                            logging.error(f"MySQL error: {err}")
                            conn.rollback()
                        except Exception as e:
                            logging.error(f"Unexpected error: {e}")
                            conn.rollback()

                    logging.info(f"Page {page}: {page_reviews} reviews added, {duplicate_count} duplicates skipped")
                    
                    if page_reviews == 0:
                        logging.info("No new reviews found on this page. Ending scraping.")
                        break
                    
                    page += 1
                    # Add some randomization to the delay
                    time.sleep(delay + random.uniform(1, 3))
                    
                except Exception as e:
                    logging.error(f"Error processing page {page}: {e}")
                    break
            
            browser.close()

        # Write to CSV
        try:
            csv_file = 'reviews.csv'
            csv_headers = ['rating', 'text', 'parent_asin', 'user_id', 'timestamp']
            with open(csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=csv_headers)
                writer.writeheader()
                writer.writerows(reviews)
            logging.info(f'Reviews extracted and saved to {csv_file}')
        except IOError as e:
            logging.error(f"Error writing to CSV: {e}")

        logging.info(f"Scraping completed. Total reviews added: {total_reviews}")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        cursor.close()
        conn.close()
        logging.info("Database connection closed")

def scrape_reviews(asin):
    try:
        reviews_into_sql(asin, max_pages=15, delay=5)
        return True
    except Exception as e:
        logging.error(f"scrape reviews function error: {e}")
        return False
    
scrape_reviews("B08V51YBKG")