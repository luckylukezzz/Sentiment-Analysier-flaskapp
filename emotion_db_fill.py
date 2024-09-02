import os
from dotenv import load_dotenv
import mysql.connector
import pandas as pd
from transformers import pipeline

# Load environment variables from the .env file
load_dotenv()

# Get database connection details from environment variables
host = os.getenv('HOST')
port = os.getenv('PORT')
database = os.getenv('DATABASE')
user = os.getenv('USER')
password = os.getenv('PASSWORD')

# Establish the connection to the MySQL database
conn = mysql.connector.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database,
    ssl_disabled=False,
)

# Create a cursor object
cursor = conn.cursor()
print("db cons okay")
# Define a function to get the highest scored emotion
def get_highest_scored_emotion(output):
    emotion_mapping = {
        'LABEL_0': 'sadness',
        'LABEL_1': 'joy',
        'LABEL_2': 'love',
        'LABEL_3': 'anger',
        'LABEL_4': 'fear',
        'LABEL_5': 'surprise'
    }
    highest_scored_label = max(output[0], key=lambda x: x['score'])
    emotion = emotion_mapping.get(highest_scored_label['label'], 'Unknown')
    score = highest_scored_label['score']
    return emotion, score

# Load the pre-trained classifier model
classifier = pipeline("text-classification", model="./distilbert-base-uncased-finetuned-emotion")

try:
    # Fetch data from the reviews table where emotion or emo_score is missing
    query = "SELECT review_id, text FROM reviews WHERE emotion IS NULL OR emo_score IS NULL;"
    reviews_df = pd.read_sql(query, conn)

    # Loop through the dataframe to predict emotions and update the table
    for index, row in reviews_df.iterrows():
        review_id = row['review_id']
        text = row['text']
        
        # Predict emotion and score
        preds = classifier(text, return_all_scores=True)
        emotion, score = get_highest_scored_emotion(preds)
        
        # Update the reviews table with the predicted values
        update_query = """
            UPDATE reviews
            SET emotion = %s, emo_score = %s
            WHERE review_id = %s;
        """
        cursor.execute(update_query, (emotion, score, review_id))
        conn.commit()
        print(f"Updated review_id {review_id}: Emotion = {emotion}, Score = {score:.4f}")

finally:
    # Close the cursor and the database connection
    cursor.close()
    conn.close()
