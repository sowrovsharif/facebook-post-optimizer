# src/status_generator.py

from utils import get_groq_chatbot_response

def generate_status_updates(keywords, hashtags):
    """
    Generate a single, engaging Facebook status update using keywords and hashtags.
    Args:
        keywords (List[str]): Extracted keywords
        hashtags (List[str]): Generated hashtags
    Returns:
        List[str]: List with a single status update
    """
    if not keywords and not hashtags:
        return []

    prompt = f"""
Using the following keywords and hashtags, write **only one** short, catchy, and engaging Facebook status.

- Incorporate the keywords and hashtags naturally.
- Do not include explanations or numbering.
- Do not describe what the status is about.
- Only return the actual status content.

Keywords: {', '.join(keywords)}
Hashtags: {' '.join(hashtags)}

Just output the one-liner Facebook status only:
"""

    messages = [
        {"role": "system", "content": "You are a creative writer for social media. Write engaging, short posts."},
        {"role": "user", "content": prompt}
    ]

    response = get_groq_chatbot_response(messages)
    return [response.strip()]
