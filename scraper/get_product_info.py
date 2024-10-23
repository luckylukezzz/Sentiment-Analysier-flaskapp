from playwright.sync_api import sync_playwright
import time
import json
import csv
import os
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(filename='product_info.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

host = os.getenv('HOST')
database = os.getenv('DATABASE')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
port = os.getenv('PORT')


def get_product_html(asin):
    url = f"https://www.amazon.com/dp/{asin}/"
    
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True, slow_mo=100)
        page = browser.new_page()
        
        try:
            page.goto(url, timeout=60000)  # Increased timeout to 60 seconds
            time.sleep(5)  # Wait for the page to load
            
            # Get the page content (HTML)
            page_content = page.content()
            
            return page_content
        
        except Exception as e:
            logging.error(f"An error occurred while fetching the page: {e}")
            return None
        
        finally:
            browser.close()

def extract_product_info(html_content, asin):
    if not html_content:
        logging.warning(f"No HTML content to parse for ASIN: {asin}")
        return None

    soup = BeautifulSoup(html_content, 'html.parser')

    try:
        product_title = soup.find('span', id='productTitle').get_text(strip=True)
    except AttributeError:
        product_title = "N/A"
        logging.warning(f"Could not find product title for ASIN: {asin}")

    categories = [a.get_text(strip=True) for a in soup.find_all('a', class_='a-link-normal a-color-tertiary')]
    main_category = categories[0] if categories else "N/A"
    all_categories = ', '.join(categories) if categories else "N/A"

    features = [li.get_text(strip=True) for li in soup.select('ul.a-unordered-list.a-vertical.a-spacing-mini li')]
    features_str = '; '.join(features) if features else "N/A"

    try:
        image_link = soup.find('div', id='imgTagWrapperId').find('img')['src']
    except AttributeError:
        image_link = "N/A"
        logging.warning(f"Could not find image link for ASIN: {asin}")

    try:
        store = soup.find('a', id='bylineInfo').get_text(strip=True)
        if store.startswith("Visit the"):
            store = store.replace("Visit the", "").strip()
    except AttributeError:
        store = "N/A"
        logging.warning(f"Could not find store name for ASIN: {asin}")

    details = {}
    for row in soup.select('#productDetails_detailBullets_sections1 tr'):
        try:
            th = row.find('th').get_text(strip=True)
            td = row.find('td').get_text(strip=True)
            details[th] = td
        except AttributeError:
            continue

    details_str = json.dumps(details, ensure_ascii=False).replace('"', '')

    return {
        'parent_asin': asin,
        'main_category': main_category,
        'title': product_title,
        'features': features_str,
        'image': image_link,
        'categories': all_categories,
        'store': store,
        'details': details_str
    }

def asin_exists_in_db(cursor, asin):
    query = "SELECT COUNT(*) FROM products WHERE parent_asin = %s"
    cursor.execute(query, (asin,))
    count = cursor.fetchone()[0]
    return count > 0

def asin_exists_in_csv(asin, filename='product_data.csv'):
    if not os.path.exists(filename):
        return False
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return any(row['parent_asin'] == asin for row in reader)

def insert_into_mysql(data):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            port=port,
            password=password,
            database=database,
            ssl_disabled=False,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            if asin_exists_in_db(cursor, data['parent_asin']):
                logging.info(f"ASIN {data['parent_asin']} already exists in the database. Skipping insertion.")
                return True

            query = """INSERT INTO products 
                       (parent_asin, main_category, title, features, image, categories, store, details) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            
            values = (
                data['parent_asin'],
                data['main_category'],
                data['title'],
                data['features'],
                data['image'],
                data['categories'],
                data['store'],
                data['details']
            )

            cursor.execute(query, values)
            connection.commit()
            logging.info(f"Data inserted successfully for ASIN: {data['parent_asin']}")
            return True

    except Error as e:
        logging.error(f"Error while connecting to MySQL or inserting data: {e}")
        return False

    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()

def write_to_csv(data, filename='product_data.csv'):
    file_exists = os.path.exists(filename)
    
    if file_exists and asin_exists_in_csv(data['parent_asin'], filename):
        logging.info(f"ASIN {data['parent_asin']} already exists in the CSV. Skipping writing.")
        return

    mode = 'a' if file_exists else 'w'
    with open(filename, mode=mode, newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)
    logging.info(f"Data written to {filename} for ASIN: {data['parent_asin']}")

def product_info(asin):
    html_content = get_product_html(asin)
    if html_content:
        product_data = extract_product_info(html_content, asin)
        if product_data:
            isTrue = insert_into_mysql(product_data)
            write_to_csv(product_data)
            return isTrue
        else:
            logging.error(f"Failed to extract product info for ASIN: {asin}")
            return False
    else:
        logging.error(f"Failed to get HTML content for ASIN: {asin}")
        return False

# Example usage
#result = product_info('B079FPFV3X')
#logging.info(f"Product info result: {result}")