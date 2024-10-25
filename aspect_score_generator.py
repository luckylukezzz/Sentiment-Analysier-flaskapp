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







