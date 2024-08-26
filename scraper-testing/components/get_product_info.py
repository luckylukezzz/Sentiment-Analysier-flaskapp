from playwright.sync_api import sync_playwright
import time
import json
import csv
from bs4 import BeautifulSoup

def get_product_html(asin):
    url = f"https://www.amazon.com/dp/{asin}/"
    
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False, slow_mo=100)
        page = browser.new_page()
        
        try:
            page.goto(url)
            time.sleep(5)  # Wait for the page to load
            
            # Get the page content (HTML)
            page_content = page.content()
            
            return page_content
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
        finally:
            browser.close()

def extract_product_info(html_content, asin):
    
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the product title
    product_title = soup.find('span', id='productTitle').get_text(strip=True)

    # Extract the main category and list of categories
    categories = [a.get_text(strip=True) for a in soup.find_all('a', class_='a-link-normal a-color-tertiary')]
    main_category = categories[0] if categories else None
    all_categories = ', '.join(categories)

    # Extract the features list items
    features = [li.get_text(strip=True) for li in soup.select('ul.a-unordered-list.a-vertical.a-spacing-mini li')]

    # Extract the image source link
    image_link = soup.find('div', id='imgTagWrapperId').find('img')['src']

    # Extract product details as key-value pairs
    details = {}
    for row in soup.select('#productDetails_detailBullets_sections1 tr'):
        th = row.find('th').get_text(strip=True)
        td = row.find('td').get_text(strip=True)
        details[th] = td

    # Serialize the details dictionary as a string without escaping quotes
    details_str = json.dumps(details, ensure_ascii=False).replace('"', '')

    # Prepare CSV data
    csv_data = {
        'parent_asin': asin,
        'main_category': main_category,
        'title': product_title,
        'features': '; '.join(features),
        'image': image_link,
        'categories': all_categories,
        'details': details_str  # Details without extra quotes
    }

    # Write to CSV
    with open('product_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=csv_data.keys())
        writer.writeheader()
        writer.writerow(csv_data)

    print("Data written to product_data.csv")

# Example usage
extract_product_info(get_product_html('B079FPFV3X'), 'B079FPFV3X')
