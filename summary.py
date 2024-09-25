from db_connection import DBConnection
import json
import ast
import pandas as pd

def calculateOverallSentiments(parent_asin):
    conn = DBConnection()
    print("connected")

    result = conn.fetch_keywords(parent_asin)
    # Create a Pandas DataFrame from the fetched results
    df = pd.DataFrame(result, columns=['keywords'])

    conn.close()
    #print(df.head())

    #type your required keywords
    keywords_to_check = ['perfect', 'price', 'shipping']
    positive_fractions = calculate_positive_fraction(df, keywords_to_check)

    #Output the result
    print(positive_fractions)
    #print(type(positive_fractions))

def calculate_positive_fraction(df, keywords_to_check):
    keyword_counts = {keyword: {'positive': 0, 'negative': 0, 'neutral': 0} for keyword in keywords_to_check}

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Convert the string of lists into a Python list
        keyword_list = ast.literal_eval(row['keywords'])

        # Loop through each keyword-sentiment pair in the row
        for keyword, sentiment in keyword_list:
            if keyword in keyword_counts:
                if sentiment == 'Positive':
                    keyword_counts[keyword]['positive'] += 1
                elif sentiment == 'Negative':
                    keyword_counts[keyword]['negative'] += 1
                elif sentiment == 'Neutral':
                    keyword_counts[keyword]['neutral'] += 1

    # Calculate fractions for each keyword
    fractions = {}
    for keyword, counts in keyword_counts.items():
        total = counts['positive'] + counts['negative'] + counts['neutral']
        if total > 0:
            fractions[keyword] = counts['positive'] / total
        else:
            fractions[keyword] = None  # In case there are no instances

    return fractions


calculateOverallSentiments('B00NQHZ2RU')