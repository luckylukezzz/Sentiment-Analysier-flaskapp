import os
from transformers import AutoModel, AutoTokenizer
from tqdm.auto import tqdm

# Define model and tokenizer names
model_name = "bert-base-uncased"
tokenizer_name = "bert-base-uncased"

# Define the directory where you want to save the model
save_directory = "./models"

# Create the directory if it doesn't exist
os.makedirs(save_directory, exist_ok=True)

# Download and save the tokenizer with a progress bar
print(f"Downloading and saving the tokenizer '{tokenizer_name}'...")
tokenizer = AutoTokenizer.from_pretrained(tokenizer_name, cache_dir=save_directory, tqdm_class=tqdm)

# Download and save the model with a progress bar
print(f"Downloading and saving the model '{model_name}'...")
model = AutoModel.from_pretrained(model_name, cache_dir=save_directory, tqdm_class=tqdm)

print(f"Model and tokenizer saved in {save_directory}")
