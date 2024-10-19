from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
from tqdm import tqdm


class AspectExtractor:
    def __init__(self, model_name="ilsilfverskiold/tech-keywords-extractor", max_new_tokens=50):
        self.extract_aspects = pipeline("text2text-generation", model=model_name, max_new_tokens=max_new_tokens)

    def process_in_batches(self, reviews, batch_size=32):
        aspects = []
        num_errors = 0

        for i in tqdm(range(0, len(reviews), batch_size)):
            batch = reviews[i:i + batch_size]
            try:
                batch_results = self.extract_aspects(batch)
                aspects.extend(batch_results)
            except IndexError as e:
                aspects.extend(["IndexError-py"] * len(batch))
                num_errors += len(batch)
            except Exception as e:
                aspects.extend(["OtherError-py"] * len(batch))
                num_errors += len(batch)

        return aspects, num_errors

    def process_reviews(self, reviews):
        processed_reviews, num_errors = self.process_in_batches(reviews)
        print(f"Number of errors: {num_errors}")
        return processed_reviews

    def process_aspects(self, reviews):
        result = []
        for aspect in self.process_reviews(reviews):
            if isinstance(aspect, dict) and 'generated_text' in aspect:
                text = aspect['generated_text']
                keywords = [keyword.strip() for keyword in text.split(',')]
            elif isinstance(aspect, str):
                keywords = [aspect]
            else:
                keywords = ["UnknownFormat"]
            result.append(keywords)
        return result


class SentimentAspectAnalyzer:
    def __init__(self, model_name="yangheng/deberta-v3-base-absa-v1.1"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        #print("Model loadedloololololololololololol")

    def analyze_aspects(self, reviews, aspects):
        sentiment_aspect = []
        for i in tqdm(range(len(aspects))):
            temp = []
            for j in range(len(aspects[i])):
                inputs = self.tokenizer(reviews[i], aspects[i][j], return_tensors="pt")
                with torch.inference_mode():
                    outputs = self.model(**inputs)
                    scores = F.softmax(outputs.logits[0], dim=-1)
                    label_id = torch.argmax(scores).item()
                    temp.append([
                        aspects[i][j],
                        self.model.config.id2label[label_id],
                        #scores[label_id].item()
                    ])
            sentiment_aspect.append(temp)
        return sentiment_aspect

    def analyze_overall(self, reviews):
        overall_sentiments = []
        for review in tqdm(reviews):
            inputs = self.tokenizer(review, return_tensors="pt")
            with torch.inference_mode():
                outputs = self.model(**inputs)
                scores = F.softmax(outputs.logits[0], dim=-1)
                label_id = torch.argmax(scores).item()

            overall_sentiments.append([
                #"review": review,
                #self.model.config.id2label[label_id],
                    scores[2].item(), #pos_score
                    scores[1].item(), #neu_score
                    scores[0].item()  #neg_score
            ])
        return overall_sentiments

    def analyze(self, reviews, aspects):
        aspect_sentiments = self.analyze_aspects(reviews, aspects)
        overall_sentiments = self.analyze_overall(reviews)
        return aspect_sentiments, overall_sentiments


# Example usage:
aspect_extractor = AspectExtractor()
reviews = ["The battery life is great but the screen is dim.", "The product is very durable."]
aspects = aspect_extractor.process_aspects(reviews)

sentiment_analyzer = SentimentAspectAnalyzer()
aspect_sentiments, overall_sentiments = sentiment_analyzer.analyze(reviews, aspects)

#print("Aspect-wise Sentiments:", aspect_sentiments)
#print("Overall Sentiments:", overall_sentiments)

"""
print("Aspect-wise Sentiments:")
for i in range(len(reviews)):
     print(f"Review: {reviews[i]}")
     for aspect in aspect_sentiments[i]:
         print(f"  Aspect: {aspect['aspect']}, Sentiment: {aspect['sentiment_label']}, Score: {aspect['sentiment_score']}")
     print()

print("Overall Sentiments:")
for overall in overall_sentiments:
     print(f"Review: {overall['review']}")
     print(f"  Sentiment: {overall['overall_sentiment_label']}")
     print(f"  Scores: {overall['overall_sentiment_scores']}")
     print()
"""