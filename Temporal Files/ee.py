# from tensorflow.keras.models import load_model
# import re
# import numpy as np  
# from tensorflow.keras.preprocessing.text import one_hot
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# from nltk.stem import PorterStemmer
# from nltk.corpus import stopwords
# import nltk

# # Download the stopwords corpus
# nltk.download('stopwords')

# lstm_emo_classifier = load_model("models\model_lstm_new.h5")

# def predictive_system_dl(sentence):
#     stemmer = PorterStemmer()
#     corpus = []
#     text = re.sub("[^a-zA-Z]", " ", sentence)
#     text = text.lower()
#     text = text.split()
#     stop_words = set(stopwords.words("english"))  # Corrected line
#     text = [stemmer.stem(word) for word in text if word not in stop_words]
#     text = " ".join(text)
#     corpus.append(text)
#     print(corpus)
#     one_hot_word = [one_hot(input_text=word, n=11000) for word in corpus]
#     pad = pad_sequences(sequences=one_hot_word, maxlen=300, padding="pre")
#     return pad

# emotion_mapping = {
#     'sadness': 0,
#     'anger': 1,
#     'love': 2,
#     'surprise': 3,
#     'fear': 4,
#     'joy': 5
# }

# reverse_emotion_mapping = {v: k for k, v in emotion_mapping.items()}

# sentence = predictive_system_dl(" I am so happy with this purchase. Saved a ton of money too.")
# prediction = lstm_emo_classifier.predict(sentence)
# predicted_class_index = np.argmax(prediction, axis=1)[0]   
# result = reverse_emotion_mapping[predicted_class_index]
# prob = np.max(prediction)   
# print(f"{result} with probability of {prob}")

import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"

from transformers import pipeline

def get_highest_scored_emotion(output):
    # Mapping of labels to their corresponding emotions
    emotion_mapping = {
        'LABEL_0': 'sadness',
        'LABEL_1': 'joy',
        'LABEL_2': 'love',
        'LABEL_3': 'anger',
        'LABEL_4': 'fear',
        'LABEL_5': 'surprise'
    }

    # Find the label with the highest score
    highest_scored_label = max(output[0], key=lambda x: x['score'])

    # Get the corresponding emotion and score
    emotion = emotion_mapping.get(highest_scored_label['label'], 'Unknown')
    score = highest_scored_label['score']

    return emotion, score

# load from previously saved model
classifier = pipeline("text-classification", model="./distilbert-base-uncased-finetuned-emotion")

# New unseen by model data
new_data = "it came 2 days early & is exactly as described."

preds = classifier(new_data, return_all_scores=True)

emotion, score = get_highest_scored_emotion(preds)

print(f"Highest scored emotion: {emotion} with a score of {score:.4f}")
