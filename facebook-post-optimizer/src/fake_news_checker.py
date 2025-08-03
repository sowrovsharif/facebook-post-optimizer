# src/fake_news_checker.py

from transformers import pipeline
from utils import get_groq_chatbot_response

# Load the zero-shot classifier only once
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def check_status_genuineness(text):

    if not text.strip():
        return {"classification": {}, "fact_check": "No status provided."}

    # Step 1: Classify using BART
    labels = ["real", "fake", "misleading"]
    classification_result = classifier(text, candidate_labels=labels)

    scores = {
        label: round(score * 100, 2)
        for label, score in zip(classification_result["labels"], classification_result["scores"])
    }

    # Step 2: Groq fact-checking
    prompt = f"Is the following statement true, fake, or misleading? Justify your answer.\n\n'{text}'"
    messages = [
        {"role": "system", "content": "You're a fact-checking assistant. Evaluate the truthfulness of the user's claim using up-to-date knowledge. And Generate the ouput shortly"},
        {"role": "user", "content": prompt}
    ]

    fact_check_response = get_groq_chatbot_response(messages, temperature=0.2)

    return {
        "classification": scores,
        "fact_check": fact_check_response
    }

