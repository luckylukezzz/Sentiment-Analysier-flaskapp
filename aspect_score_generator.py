from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from tqdm import tqdm

class AspectScoreGenerator:
    def __init__(self, model_name="yangheng/deberta-v3-base-absa-v1.1"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.classifier = pipeline("text-classification", model=self.model, tokenizer=self.tokenizer)

    def extract_aspect_scores(self, reviews, aspects):
        aspect_results = []
        for review in tqdm(reviews, desc="Processing Reviews", unit="review"):
            review_text = review
            aspect_results.append(self.analyze(review_text, aspects))
        return aspect_results

    def analyze(self, review_text, aspects):
        aspect_results = {}
        for aspect in aspects:
            result = self.classifier(review_text, text_pair=aspect)
            label = result[0]['label']
            score = result[0]['score']
            aspect_results[f'aspect_{aspect.lower().replace(" ", "_")}'] = label
            aspect_results[f'{aspect.lower().replace(" ", "_")}_score'] = score
        return aspect_results



# Initialize aspects
# aspects = ['quality', 'price', 'shipping', 'Customer Service', 'Warranty']





# from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
# from tqdm import tqdm
# import mysql.connector

# class AspectSentimentAnalyzer:
#     def __init__(self, model_name, db_config):
#         # Initialize the tokenizer and model for aspect-based sentiment analysis
#         self.tokenizer = AutoTokenizer.from_pretrained(model_name)
#         self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
#         self.classifier = pipeline("text-classification", model=self.model, tokenizer=self.tokenizer)

#         # Initialize database connection
#         self.conn = mysql.connector.connect(**db_config)
#         self.cursor = self.conn.cursor()

#         # Define aspects to analyze
#         self.aspects = ['quality', 'price', 'shipping', 'Customer Service', 'Warranty']

#     def fetch_reviews(self, limit=150):
#         # Fetch reviews where aspect quality is not yet analyzed
#         query = "SELECT review_id, text FROM reviews WHERE aspect_quality IS NULL LIMIT %s;"
#         self.cursor.execute(query, (limit,))
#         return self.cursor.fetchall()

#     def analyze_aspects(self, review_text):
#         # Analyze sentiments for each aspect in a review
#         aspect_results = {}
#         for aspect in self.aspects:
#             result = self.classifier(review_text, text_pair=aspect)  # Perform sentiment analysis
#             label = result[0]['label']  # Predicted sentiment
#             score = result[0]['score']  # Confidence score

#             # Store the results in a dictionary
#             aspect_results[f'aspect_{aspect.lower().replace(" ", "_")}'] = label
#             aspect_results[f'{aspect.lower().replace(" ", "_")}_score'] = score
        
#         return aspect_results





