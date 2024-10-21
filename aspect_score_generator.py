from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from tqdm import tqdm

model_name = "yangheng/deberta-v3-base-absa-v1.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

# 
# Fetch reviews from the table
cursor.execute("SELECT review_id, text FROM reviews WHERE aspect_quality IS NULL LIMIT 150;")
reviews = cursor.fetchall()

# Initialize aspects
aspects = ['quality', 'price', 'shipping', 'Customer Service', 'Warranty']

for review in tqdm(reviews, desc="Processing Reviews", unit="review"):
    review_id, review_text = review
    aspect_results = {}

    # Perform aspect-based sentiment analysis for each aspect
    for aspect in aspects:
        result = classifier(review_text, text_pair=aspect)  # Perform sentiment analysis
        label = result[0]['label']  # Get the predicted sentiment label
        score = result[0]['score']  # Get the confidence score

        # Store the results in the dictionary
        aspect_results[f'aspect_{aspect.lower().replace(" ", "_")}'] = label
        aspect_results[f'{aspect.lower().replace(" ", "_")}_score'] = score
        
    x= ("""
            UPDATE reviews
            SET aspect_quality = '%s', quality_score = %s,
                aspect_price = '%s', price_score = %s,
                aspect_shipping = '%s', shipping_score = %s,
                aspect_customer_service ='%s', customer_service_score = %s,
                aspect_warranty = '%s', warranty_score = %s
            WHERE review_id = %s
        """%(
            aspect_results['aspect_quality'], aspect_results['quality_score'],
            aspect_results['aspect_price'], aspect_results['price_score'],
            aspect_results['aspect_shipping'], aspect_results['shipping_score'],
            aspect_results['aspect_customer_service'], aspect_results['customer_service_score'],
            aspect_results['aspect_warranty'], aspect_results['warranty_score'],
            review_id
        ))
    
   
    cursor.execute(x)
    conn.commit()

cursor.close()
conn.close()