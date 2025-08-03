from transformers import pipeline

# Load emotion classifier once
emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)

def detect_emotion(text):
    """
    Detect emotion label and confidence score for given text.
    Args:
        text (str): Input status text
    Returns:
        tuple: (emotion_label: str, confidence: float)
    """
    if not text.strip():
        return None, 0.0

    results = emotion_classifier(text)[0]
    # Sort results descending by score
    sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
    top_emotion = sorted_results[0]
    return top_emotion['label'], top_emotion['score']