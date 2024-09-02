from playwright.sync_api import sync_playwright
import time
import re
import logging

# Set up logging
logging.basicConfig(filename='asin_fetch.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_product_links(url):
    with sync_playwright() as p:
        browser = None
        try:
            browser = p.firefox.launch(headless=False, slow_mo=100)
            page = browser.new_page()
            
            logging.info(f"Navigating to {url}")
            page.goto(url, timeout=60000)  # Increased timeout to 60 seconds
            time.sleep(5)  # Wait for page to load
            
            # Find all the links with the specified class
            links = page.query_selector_all('a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')
            
            product_links = []
            for link in links:
                href = link.get_attribute('href')
                if href:
                    # Construct the full URL
                    full_url = "https://www.amazon.com" + href
                    # Use regex to clean the URL
                    clean_url = re.sub(r'(/dp/[A-Z0-9]+).*', r'\1/', full_url)
                    product_links.append(clean_url)
            
            logging.info(f"Found {len(product_links)} product links")
            return product_links
        
        except Exception as e:
            logging.error(f"An error occurred while getting product links: {e}")
            return []
        
        finally:
            if browser:
                browser.close()

def get_asin_list(searchTerm):
    try:
        searchTermProcessed = "+".join(searchTerm.split())
        url = f"https://www.amazon.com/s?k={searchTermProcessed}"

        product_links = get_product_links(url)
        product_links = list(set(product_links))

        if not product_links:
            logging.warning("No product links were found. There might be an issue with the scraping process.")
            return []
        else:
            asin_list = []
            asin_pattern = re.compile(r'/dp/([A-Z0-9]{10})')
        
            for link in product_links:
                match = asin_pattern.search(link)
                if match:
                    asin_list.append(match.group(1))

            logging.info(f"Found {len(asin_list)} unique ASINs")
            return asin_list
    except Exception as e:
        logging.error(f"An error occurred in get_asin_list: {e}")
        return []

# def main():
#     try:
#         search_term = "ps4"
#         logging.info(f"Searching for: {search_term}")
#         result = get_asin_list(search_term)
#         if result:
#             print(f"ASINs found for '{search_term}':")
#             for asin in result:
#                 print(asin)
#         else:
#             print(f"No ASINs found for '{search_term}'")
#     except Exception as e:
#         logging.error(f"An error occurred in main: {e}")

# if __name__ == "__main__":
#     main()