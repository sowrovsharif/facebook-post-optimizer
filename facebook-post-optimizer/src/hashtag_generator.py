# src/hashtag_generator.py

from utils import get_groq_chatbot_response

def generate_hashtags(keywords):
    """
    Generate social media hashtags based on input keywords using Groq.
    Args:
        keywords (List[str]): List of keywords
    Returns:
        List[str]: List of hashtags
    """
    if not keywords:
        return []

    prompt = f"""
Given the following keywords:

{', '.join(keywords)}

Generate a list of 5-7 unique and trendy hashtags. 
Each hashtag must start with # and be a single word or camelCase phrase.
Avoid using spaces. Output only hashtags separated by spaces.
"""

    messages = [
        {"role": "system", "content": "You are a helpful assistant that turns keywords into catchy hashtags."},
        {"role": "user", "content": prompt}
    ]

    response = get_groq_chatbot_response(messages)
    hashtags = [tag.strip() for tag in response.replace("\n", " ").split() if tag.startswith("#")]
    return hashtags
