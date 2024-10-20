import os
import pandas as pd
from transformers import pipeline

class EmotionExtractor:
    def __init__(self, model_path="./models/distilbert-base-uncased-finetuned-emotion"):
        # Initialize the pre-trained classifier model for emotion extraction
        try:
            self.classifier = pipeline("text-classification", model=model_path)
            print(f"Model loaded successfully from {model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    # Get the highest scored emotion
    @staticmethod
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

    # Method to extract emotions from a list of reviews
    def extract_emotions(self, reviews):
        emotions = []
        scores = []

        try:
            # Loop through the list of reviews
            for review in reviews:
                # Predict emotion and get the score for each review
                preds = self.classifier(review, return_all_scores=True)
                emotion, score = self.get_highest_scored_emotion(preds)

                # Append the emotion and score to the respective lists
                emotions.append(emotion)
                scores.append(score)

        except Exception as e:
            print(f"Error extracting emotion: {e}")

        return emotions, scores


    # try:
    #     # Fetch data from the reviews table where emotion or emo_score is missing
    #     query = "SELECT review_id, text FROM reviews WHERE emotion IS NULL OR emo_score IS NULL;"
    #     reviews_df = pd.read_sql(query, conn)

    #     # Loop through the dataframe to predict emotions and update the table
    #     for index, row in reviews_df.iterrows():
    #         review_id = row['review_id']
    #         text = row['text']
            
    #         # Predict emotion and score
    #         preds = classifier(text, return_all_scores=True)
    #         emotion, score = get_highest_scored_emotion(preds)
            
    #         # Update the reviews table with the predicted values
    #         update_query = """
    #             UPDATE reviews
    #             SET emotion = %s, emo_score = %s
    #             WHERE review_id = %s;
    #         """
    #         cursor.execute(update_query, (emotion, score, review_id))
    #         conn.commit()
    #         print(f"Updated review_id {review_id}: Emotion = {emotion}, Score = {score:.4f}")

    # finally:
    #     # Close the cursor and the database connection
    #     cursor.close()
    #     conn.close()

