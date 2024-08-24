from transformers import pipeline

# reivews are in a list format
def get_sentiments_wo_neu(reviews):
    # Initialize the sentiment analysis pipeline
    sentiment_pipeline = pipeline("sentiment-analysis")

    # Perform sentiment analysis on each review
    results = sentiment_pipeline(reviews)

    # Extract sentiment labels
    sentiments = [result['label'] for result in results]

    return sentiments

#get sentiments with neutral label
def get_sentiments(reviews, neutral_threshold=0.05):
    # Initialize the sentiment analysis pipeline
    sentiment_pipeline = pipeline("sentiment-analysis")

    # Perform sentiment analysis on each review
    results = sentiment_pipeline(reviews)

    # Extract sentiment labels and scores
    sentiments = []
    for result in results:
        label = result['label']
        score = result['score']

        # If the confidence is low, classify as neutral
        if abs(score - 0.5) < neutral_threshold:
            sentiments.append("NEUTRAL")
        else:
            sentiments.append(label)

    return sentiments
