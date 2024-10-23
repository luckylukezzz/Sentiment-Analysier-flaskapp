import logging
from scraper.reviews_scrape_final import scrape_reviews
from scraper.get_product_info import product_info

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='scrape_with_asin.log',  # Specify the log file name
    filemode='w'  # 'w' mode overwrites the file, 'a' would append
)


def scrape_reviews_final(asin):
    print("strarted sraping.................................................")
    product_status = product_info(asin)
    print("fetched product info")
    if product_status:
        logging.info(f"Product info retrieved successfully for ASIN: {asin}")
        logging.info(f"Scraping reviews for ASIN: {asin}")
        print(f"Scraping reviews for ASIN: {asin}")
        scrape_reviews(asin)
    else:
        logging.warning(f"Failed to retrieve product info for ASIN: {asin}")

    logging.info("Processing complete")
