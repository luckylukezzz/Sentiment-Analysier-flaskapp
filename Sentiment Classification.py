from transformers import pipeline

# reivews are in a list format
def get_sentiments(reviews):
    # Initialize the sentiment analysis pipeline
    sentiment_pipeline = pipeline("sentiment-analysis")

    # Perform sentiment analysis on each review
    results = sentiment_pipeline(reviews)

    # Extract sentiment labels
    sentiments = [result['label'] for result in results]

    return sentiments