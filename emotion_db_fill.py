import os
import pandas as pd
from transformers import pipeline

class EmotionExtractor:
    def __init__(self, model_path="./models/distilbert-base-uncased-finetuned-emotion", max_length=512):
        # Initialize the pre-trained classifier model for emotion extraction
        self.max_length = max_length
        try:
            self.classifier = pipeline("text-classification", model=model_path)
            print("Emotion Model loaded successfully from disk")
        except Exception as e:
            print(f"Error loading Emotion Model from disk: {str(e)}")
            self.classifier = pipeline("text-classification", model="transformersbook/distilbert-base-uncased-finetuned-emotion")
            print("Emotion Model loaded from internet successfully")

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
                # Split the review into chunks if it's longer than max_length
                chunks = [review[i:i + self.max_length] for i in range(0, len(review), self.max_length)]
                chunk_emotions = []
                chunk_scores = []

                for chunk in chunks:
                    # Predict emotion and get the score for each chunk
                    preds = self.classifier(chunk, return_all_scores=True)
                    emotion, score = self.get_highest_scored_emotion(preds)
                    chunk_emotions.append(emotion)
                    chunk_scores.append(score)

                # Aggregate results from all chunks 
                final_emotion = max(set(chunk_emotions), key=chunk_emotions.count)
                final_score = sum(chunk_scores) / len(chunk_scores) if chunk_scores else 0

                emotions.append(final_emotion)
                scores.append(final_score)

        except Exception as e:
            print(f"Error extracting emotion: {e}")

        return emotions, scores




