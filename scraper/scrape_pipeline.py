import logging
from reviews_scrape_final import scrape_reviews
from get_asin_lists import get_asin_list
from get_product_info import product_info

# Set up logging to write to a file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='amazon_scraping.log',  # Specify the log file name
    filemode='w'  # 'w' mode overwrites the file, 'a' would append
)


def pipeline(search_term):
    try:
        
        logging.info(f"Searching for: {search_term}")
        
        asins = get_asin_list(search_term)
        logging.info(f"Found {len(asins)} ASINs for '{search_term}'")
        
        for asin in asins:
            logging.info(f"Processing ASIN: {asin}")
            
            product_okay = product_info(asin)
            if product_okay:
                logging.info(f"Product info retrieved successfully for ASIN: {asin}")
                logging.info(f"Scraping reviews for ASIN: {asin}")
                scrape_reviews(asin)
            else:
                logging.warning(f"Failed to retrieve product info for ASIN: {asin}")
        
        logging.info("Processing complete")
    
    except Exception as e:
        logging.error(f"An error occurred in main: {e}")

pipeline("monitor")