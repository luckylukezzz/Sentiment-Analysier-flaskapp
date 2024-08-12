import requests
from bs4 import BeautifulSoup
import random
import mysql.connector
import csv
from bs4 import BeautifulSoup
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


#get headers -------------------------------------------------------------------
response = requests.get(
  url='https://headers.scrapeops.io/v1/browser-headers',
  params={
      'api_key': 'ef359c6c-468c-4004-8869-da304cbb68dc',
      'num_results': '1'}
)

scrape_headers = response.json()
# print(scrape_headers)


# Retrieve and prepare the list of proxies
# proxies = []
# response = requests.get("http://sslproxies.org/")
# soup = BeautifulSoup(response.content, 'html.parser')
# proxies_table = soup.find('table', class_='table table-striped table-bordered')
# for row in proxies_table.tbody.find_all('tr'):
#     proxies.append({
#         'ip': row.find_all('td')[0].string,
#         'port': row.find_all('td')[1].string
#     })

# # Create a list of proxy dictionaries
# proxies_lst = [{'http': 'http://' + proxy['ip'] + ':' + proxy['port']} for proxy in proxies]
# proxies_lst

# proxy = random.choice(proxies_lst)


#get reviews -----------------------------------------------------------------------------------------
url ="http://www.amazon.com/dp/product-reviews/B00NLZUM36?pageNumber=1"
response = requests.get(url, headers=scrape_headers["result"][0]  )

# , proxies= {'http': 'http://124.6.155.170:3131'}

print(response.status_code)



host = os.getenv('HOST')
database = os.getenv('DATABASE')
user = os.getenv('USER')
password = os.getenv('PASSWORD')


conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    connection_timeout=1000,
)
cursor = conn.cursor()

# Scraping and insertion logic
soup = BeautifulSoup(response.text, 'html.parser')
reviews = []
parent_asin = "B00NLZUM36"
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

        # Prepare SQL insert statement
        insert_stmt = """
        INSERT INTO reviews (rating, text, parent_asin, user_id, timestamp)
        VALUES (%s, %s, %s, %s, %s)
        """
        data = (rating, review_text, parent_asin, user_id, review_date_ms)

        # Execute the SQL statement
        cursor.execute(insert_stmt, data)
        conn.commit()

    except AttributeError:
        # Skip review blocks that don't match the expected structure
        continue

# Close the cursor and connection
cursor.close()
conn.close()


csv_file = 'reviews.csv'

csv_headers = ['rating', 'text', 'parent_asin', 'user_id', 'timestamp']

# Write reviews to CSV
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=csv_headers)
    writer.writeheader()
    writer.writerows(reviews)

print(f'Reviews extracted and saved to {csv_file}')

