import requests
from bs4 import BeautifulSoup
import random
import mysql.connector
import csv
from bs4 import BeautifulSoup
from datetime import datetime
import os
from components.scrape_ops_headers import get_headers
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('HOST')
database = os.getenv('DATABASE')
user = os.getenv('USER')
password = os.getenv('PASSWORD')


conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
)
cursor = conn.cursor()
print("db con okay")

#get reviews -----------------------------------------------------------------------------------------
def reviews_into_sql(asin):
    scrape_headers= get_headers()
    print(scrape_headers["result"][0])
    url =f"http://www.amazon.com/dp/product-reviews/{asin}?pageNumber=1"
    response = requests.get(url, headers=scrape_headers["result"][0]  )

    # , proxies= {'http': 'http://124.6.155.170:3131'}

    print(response.status_code)

    soup = BeautifulSoup(response.text, 'html.parser')
    reviews = []
    parent_asin = asin

    # Find all review blocks
    review_blocks = soup.find_all('div', class_='a-row a-spacing-none')

    for review_block in review_blocks:
        try:
            rating = float(review_block.find('span', class_='a-icon-alt').text.split(' ')[0])  # Extract star rating
            review_title = review_block.find('span', class_=None).text  # Extract review title

            review_date_full_str = review_block.find('span', {'data-hook': 'review-date'}).text
            review_date_str = review_date_full_str.split('on ')[-1]  # Remove prefix 'Reviewed in the United States on'
            review_date = datetime.strptime(review_date_str, '%B %d, %Y') # Extract review date
            review_date_ms = int(review_date.timestamp() * 1000)

            review_body = review_block.find('span', {'data-hook': 'review-body'}).text  # Extract review body
            review_text = f"{review_title}. {review_body}"

            user_id = review_block.find('a', class_='a-profile')['href'].split('.')[2].split('/')[0]  # Extract user ID
            review = {
                'rating': rating,
                'text': review_text,
                'parent_asin': parent_asin,
                'user_id': user_id,
                'timestamp': review_date_ms,
            }

            reviews.append(review)
           
            insert_stmt = """
            INSERT INTO reviews (rating, text, parent_asin, user_id, timestamp)
            VALUES (%s, %s, %s, %s, %s)
            """
            data = (rating, review_text, parent_asin, user_id, review_date_ms)

            cursor.execute(insert_stmt, data)
            conn.commit()

        except AttributeError:
            # Skip review blocks that don't match the expected structure
            continue

    cursor.close()
    conn.close()

    csv_file = 'reviews.csv'

    csv_headers = ['rating', 'text', 'parent_asin', 'user_id', 'timestamp']

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=csv_headers)
        writer.writeheader()
        writer.writerows(reviews)

    print(f'Reviews extracted and saved to {csv_file}')

reviews_into_sql('B098V9PT4N')