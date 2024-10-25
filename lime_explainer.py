from tqdm import tqdm
import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from lime.lime_text import LimeTextExplainer
import numpy as np

class LimeExplainer:
    def __init__(self, model_name="yangheng/deberta-v3-base-absa-v1.1"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.classifier = pipeline("text-classification", model=self.model, tokenizer=self.tokenizer)
        self.explainer = LimeTextExplainer(class_names=['Negative','Positive', 'Neutral'])

    # Function to predict probabilities (used for LIME explanations)
    def predict_proba(self, texts):
        probs = np.zeros((len(texts), 3))  # 3 classes: Negative, Neutral, Positive
        for i, text in enumerate(texts):
            result = self.classifier(text, text_pair=global_aspect)[0]
            if result['label'] == 'Negative':
                probs[i, 0] = result['score']
            elif result['label'] == 'Neutral':
                probs[i, 1] = result['score']
            else:  # Positive
                probs[i, 2] = result['score']
        return probs

    # Function to explain review and its aspects
    def explain_review(self, reviews, aspects_list):
        global global_aspect
        lime_results = []
        
        # Loop through each review and its corresponding aspects
        for review, aspects in zip(reviews, aspects_list):
            lime_explanations = {"text": review}
        
            # Loop through each aspect and generate LIME explanation
            for aspect, sentiment in aspects.items():
                if "score" in aspect:  # Skip score fields
                    continue

                # Remove the 'aspect_' prefix from the aspect name (e.g., 'aspect_price' -> 'price')
                global_aspect = aspect.replace("aspect_", "")  # Get the aspect name (e.g., 'quality', 'price')
                
                # Map sentiment labels to index for LIME
                sentiment_label = ['Negative', 'Neutral', 'Positive'].index(sentiment)
                
                # Generate LIME explanation for the aspect
                exp = self.explainer.explain_instance(review, lambda x: self.predict_proba(x), num_samples=50, num_features=6, labels=[sentiment_label])
                
                # Collect explanation features and weights
                features = []
                for feature, weight in exp.as_list(label=sentiment_label):
                    features.append({"feature": feature, "weight": round(weight, 4)})
                
                # Store the LIME explanation for the current aspect (with 'aspect_' removed from the key)
                lime_explanations[global_aspect] = {
                    "sentiment": sentiment,
                    "features": features
                }
            
            # Append explanations for the current review
            lime_results.append(lime_explanations)
        
        return lime_results


# # Instantiate the LIME Explainer
# explainer = LimeExplainer()

# # Example list of reviews and aspects
# reviews = [
#     "The product quality is excellent but the price is too high. Customer service could be better.",
#     "The shipping was very slow and warranty coverage is lacking. However, the price was reasonable."
# ]

# aspects_list = [
#     {
#         'aspect_quality': 'Positive',
#         'quality_score': 0.998171,
#         'aspect_price': 'Negative',
#         'price_score': 0.917172,
#         'aspect_shipping': 'Negative',
#         'shipping_score': 0.931703,
#         'aspect_customer_service': 'Neutral',
#         'customer_service_score': 0.951092,
#         'aspect_warranty': 'Negative',
#         'warranty_score': 0.967939
#     },
#     {
#         'aspect_quality': 'Neutral',
#         'quality_score': 0.591166,
#         'aspect_price': 'Positive',
#         'price_score': 0.990009,
#         'aspect_shipping': 'Negative',
#         'shipping_score': 0.931702,
#         'aspect_customer_service': 'Negative',
#         'customer_service_score': 0.567753,
#         'aspect_warranty': 'Negative',
#         'warranty_score': 0.967939
#     }
# ]

# # Generate LIME explanations for the reviews and aspects
# lime_explanations = explainer.explain_review(reviews, aspects_list)

# # # Output the results (ready to be inserted into the database)
# # for explanation in lime_explanations:
# #     print(json.dumps(explanation, indent=2))

# print(lime_explanations)

# aspect_results = [{'aspect_quality': 'Negative', 'quality_score': 0.9747533202171326, 'aspect_price': 'Negative', 'price_score': 0.9328009486198425, 'aspect_shipping': 'Negative', 'shipping_score': 0.9708723425865173, 'aspect_customer_service': 'Negative', 'customer_service_score': 0.9813087582588196, 'aspect_warranty': 'Negative', 'warranty_score': 0.9620404839515686}, {'aspect_quality': 'Negative', 'quality_score': 0.9909541010856628, 'aspect_price': 'Negative', 'price_score': 0.9698894619941711, 'aspect_shipping': 'Negative', 'shipping_score': 0.9849259257316589, 'aspect_customer_service': 'Negative', 'customer_service_score': 0.9111804366111755, 'aspect_warranty': 'Negative', 'warranty_score': 0.9824346899986267}, {'aspect_quality': 'Neutral', 'quality_score': 0.8493894934654236, 'aspect_price': 'Neutral', 'price_score': 0.8637327551841736, 'aspect_shipping': 'Neutral', 'shipping_score': 0.8469873070716858, 'aspect_customer_service': 'Neutral', 'customer_service_score': 0.5670762658119202, 'aspect_warranty': 'Neutral', 'warranty_score': 0.7487170696258545}, {'aspect_quality': 'Positive', 'quality_score': 0.9642613530158997, 'aspect_price': 'Positive', 'price_score': 0.6883973479270935, 'aspect_shipping': 'Positive', 'shipping_score': 0.7137025594711304, 'aspect_customer_service': 'Positive', 'customer_service_score': 0.5622305870056152, 'aspect_warranty': 'Positive', 'warranty_score': 0.7055509090423584}, {'aspect_quality': 'Neutral', 'quality_score': 0.5263849496841431, 'aspect_price': 'Neutral', 'price_score': 0.652712881565094, 'aspect_shipping': 'Neutral', 'shipping_score': 0.7759869694709778, 'aspect_customer_service': 'Positive', 'customer_service_score': 0.6305484771728516, 'aspect_warranty': 'Negative', 'warranty_score': 0.7330822944641113}]

