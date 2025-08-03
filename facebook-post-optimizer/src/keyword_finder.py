from keybert import KeyBERT

# Initialize the KeyBERT model once
kw_model = KeyBERT(model='all-MiniLM-L6-v2')

def extract_keywords(text, top_n=10):
    """
    Extract top keywords from input text.
    Args:
        text (str): Input Facebook status text.
        top_n (int): Number of keywords to extract.
    Returns:
        List[str]: List of extracted keywords.
    """
    if not text or text.strip() == "":
        return []
    
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=top_n)
    # keywords is a list of tuples (keyword, score), extract just keywords
    return [kw[0] for kw in keywords]

# For quick testing
if __name__ == "__main__":
    sample_text = "Excited to launch our new product today! Stay tuned for amazing offers and giveaways!"
    print("Extracted Keywords:", extract_keywords(sample_text))
