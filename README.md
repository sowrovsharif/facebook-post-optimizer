# 💬 Facebook Post Optimizer

A smart Facebook status generator and optimizer powered by AI. This tool helps you create engaging posts enriched with keywords, hashtags, sentiment/emotion detection, fake news verification, and reach prediction. If the predicted reach is high enough, it can even auto-post directly to Facebook.

---

## 🚀 Features

- 🔑 Keyword & Hashtag Generator  
- ✍️ AI-powered Status Generator  
- 🎭 Emotion & Sentiment Detection  
- 🚨 Fake News Checker  
- 📈 Reach Predictor  
- 🤖 Auto-post to Facebook if reach > threshold  

---

## 🛠️ Setup Instructions

```bash
# 1. Open Project Folder
cd facebook_post_optimizer

# 2. Create a Virtual Environment
python -m venv venv

# 3. Activate the Virtual Environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install Required Packages
pip install -r requirements.txt

# 5. Configure Environment Variables
# Create a `.env` file in the root folder with the following content:
# OPENAI_API_KEY=your_openai_api_key_here
# FACEBOOK_ACCESS_TOKEN=your_facebook_access_token_here

# 6. Run the Application
cd src
streamlit run main.py

