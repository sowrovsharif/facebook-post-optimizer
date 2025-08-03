def preprocess_text(text):
    # Placeholder for text preprocessing
    return text.lower().strip()

# src/utils.py

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()  # Load .env for API key

# Initialize Groq client from .env key
api_key = os.getenv("GROQ_API_KEY")  # You should add this in your .env
client = Groq(api_key=api_key)
model_name = "llama3-8b-8192"

def get_groq_chatbot_response(messages, temperature=0):

    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content.strip()
