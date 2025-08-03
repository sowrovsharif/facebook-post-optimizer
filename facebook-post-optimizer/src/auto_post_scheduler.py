import requests
import os
from dotenv import load_dotenv
load_dotenv()  # Load .env for API key

ACCESS_TOKEN = "EAAHxakjkLi8BPCH9e4Fe0ZBtl6FqqCrqa7Xh0PkZBT9ZC91tZCFx79yAiFnhw5GCI7E0NHGwlrpCQa1B5ZAe93A4O7miANv6gNnIudGN0Go40wDtcH0j1VpRavw7saceVKrFoYvJ4Mx2WZCtlFa4b6aahU9F849ZBceespTAjEqmNHQSjHDlkabHciHtxgx5DKZBKR6eGh0XBdymNpsZAd0dXhP9vl76CRSsVgBZA7vfJFxTWh85YahEvhxOSZBlZBbt"
PAGE_ID = "778747105311435"              # Your page ID

def post_to_facebook(message: str):
    """
    Posts a message to the Facebook page.

    Args:
        message (str): The content you want to post.

    Returns:
        dict: API response with post ID or error.
    """
    url = f"https://graph.facebook.com/{PAGE_ID}/feed"
    payload = {
        "message": message,
        "access_token": ACCESS_TOKEN
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        print("✅ Post shared successfully.")
        return response.json()
    else:
        print(f"❌ Failed to post: {response.status_code} - {response.text}")
        return {"error": response.text}

# Example usage
#post_to_facebook("Hello from Python script 2 🚀")
