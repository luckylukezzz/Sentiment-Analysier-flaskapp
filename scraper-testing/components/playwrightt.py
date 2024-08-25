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


def get_asin_list(searchTerm):
    searchTermProcessed = "+".join(searchTerm.split())
    url = f"https://www.amazon.com/s?k={searchTermProcessed}"

    product_links = get_product_links(url)
    product_links = list(set(product_links))

    if not product_links:
        return("No product links were found. There might be an issue with the scraping process.")
    else:
        asin_list = []

        asin_pattern = re.compile(r'/dp/([A-Z0-9]{10})')

    
        for link in product_links:
            match = asin_pattern.search(link)
            if match:
                asin_list.append(match.group(1))

        return(asin_list)


print(get_asin_list("ps4"))
asins= ['B07HHW8C4V', 'B079FPFV3X', 'B01M0RU6LY', 'B00BGA9WK2', 'B07PQPFHKN', 'B098V9PT4N', 'B00HUXPZPK', 'B0B4X5QWQB', 'B0CZLB3S83', 'B0BP3ZK9K9', 'B0C48HN4Z9', 'B012CZ41ZA', 'B075YBBQMM', 'B07JMNNPXC', 'B09772FZTX', 'B07K14XKZH', 'B0716XFVBP']
