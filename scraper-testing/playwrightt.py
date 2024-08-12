from playwright.sync_api import sync_playwright
import time
import re

def get_product_links(url):
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False, slow_mo=100)
        page = browser.new_page()
        
        try:
            page.goto(url)
            time.sleep(5)  # Wait for page to load
            
            # Find all the links with the specified class
            links = page.query_selector_all('a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')
            
            product_links = []
            for link in links:
                href = link.get_attribute('href')
                # Construct the full URL
                full_url = "http://www.amazon.com" + href
                # Use regex to clean the URL
                clean_url = re.sub(r'(/dp/[A-Z0-9]+).*', r'\1/', full_url)
                product_links.append(clean_url)
            
            return product_links
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
        
        finally:
            browser.close()

# URL of the Amazon search results page
url = "https://www.amazon.com/s?k=playstation+4&crid=5YWS6IRECKWQ&sprefix=%2Caps%2C308&ref=nb_sb_ss_recent_1_0_recent"

product_links = get_product_links(url)
product_links = list(set(product_links))

if not product_links:
    print("No product links were found. There might be an issue with the scraping process.")
else:
    print(len(product_links))
    for href in product_links:
        print(href)
        print("---")
