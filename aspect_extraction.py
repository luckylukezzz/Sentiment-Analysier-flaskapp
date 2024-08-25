######## PyABSA model to extract the aspects and their sentiment polarity############

from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from tqdm import tqdm
import torch
import torch.nn.functional as F

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
            except IndexError:
                aspects.extend(["IndexError-py"] * len(batch))
                num_errors += len(batch)
            except Exception:
                aspects.extend(["OtherError-py"] * len(batch))
                num_errors += len(batch)

        return aspects, num_errors

    def process_aspects(self, reviews):
        result = []
        for aspect in self.process_in_batches(reviews)[0]:
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

    def analyze(self, reviews, aspects):
        sentiment_aspect = []
        for i in tqdm(range(len(aspects))):
            temp = []
            for j in range(len(aspects[i])):
                inputs = self.tokenizer(reviews[i], aspects[i][j], return_tensors="pt")
                with torch.inference_mode():
                    outputs = self.model(**inputs)
                    scores = F.softmax(outputs.logits[0], dim=-1)
                    label_id = torch.argmax(scores).item()
                    temp.append(aspects[i][j])
                    temp.append((self.model.config.id2label[label_id], scores[label_id].item()))
            sentiment_aspect.append(temp)
        return sentiment_aspect
