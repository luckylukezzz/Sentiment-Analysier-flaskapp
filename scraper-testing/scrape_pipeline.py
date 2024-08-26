from reviews_scrape_final import scrape_reviews
from components.playwrightt import get_asin_list
from get_product_info import product_info

search_term="ps5"
asins=get_asin_list(search_term)

for asin in asins:
    product_okay = product_info(asin)
    if product_okay:
        scrape_reviews(asin)