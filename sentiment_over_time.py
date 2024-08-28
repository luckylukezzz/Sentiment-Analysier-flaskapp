from flask import Flask, request, jsonify
import CursorPool

app = Flask(__name__)

def search_products(cursor_pool):
    asin = request.args.get('asin', '').strip()

    try:
        if asin:
            # Query to get the sentiment data over time for the given parent_asin
            sentiment_query = """
                SELECT 
                    YEAR(FROM_UNIXTIME(timestamp / 1000)) AS year,
                    AVG(pos_score) AS avg_positive_score,
                    AVG(neg_score) AS avg_negative_score,
                    AVG(neu_score) AS avg_neutral_score,
                    COUNT(*) AS review_count
                FROM 
                    reviews
                WHERE 
                    parent_asin = %s
                GROUP BY 
                    year
                ORDER BY 
                    year;
            """
            sentiment_over_time = cursor_pool.execute_query(sentiment_query, (asin,))

            # Query to get the sentiment distribution for the given parent_asin
            distribution_query = """
                SELECT 
                    SUM(CASE WHEN pos_score >= GREATEST(neu_score, neg_score) THEN 1 ELSE 0 END) AS positive,
                    SUM(CASE WHEN neu_score >= GREATEST(pos_score, neg_score) THEN 1 ELSE 0 END) AS neutral,
                    SUM(CASE WHEN neg_score >= GREATEST(pos_score, neu_score) THEN 1 ELSE 0 END) AS negative
                FROM reviews
                WHERE parent_asin = %s;
            """
            sentiment_distribution = cursor_pool.execute_query(distribution_query, (asin,))
            
            # Query to get the product details for the given parent_asin
            product_query = """
                SELECT 
                    *
                FROM 
                    products
                WHERE 
                    asin = %s;
            """
            product_details = cursor_pool.execute_query(product_query, (asin,))

            # Prepare the response
            response = {
                "product_details": product_details,
                "sentiment_over_time": sentiment_over_time,
                "sentiment_distribution": sentiment_distribution
            }
        else:
            # Prepare the response for when no parent_asin is provided
            response = {
                "product_details": product_details,
                "sentiment_over_time": [],
                "sentiment_distribution": {}
            }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

'''
# Example route to use the search function with a cursor pool
@app.route('/search-products', methods=['GET'])
def handle_search_products():
    db_path = {
        'host': 'localhost',
        'user': 'your_username',
        'password': 'your_password',
        'database': 'your_database'
    }
    # Initialize the cursor pool
    cursor_pool = CursorPool(db_path, pool_size=5)
    try:
        return search_products(cursor_pool)
    finally:
        cursor_pool.close()

if __name__ == '__main__':
    app.run(debug=True)

    parent_asin = 'B07CQNF813'  # Example ASIN; replace with actual value
    api_token = os.getenv("GROQ_API_KEY")
    processor = ReviewProcessor(parent_asin, api_token)
    processor.process()
'''