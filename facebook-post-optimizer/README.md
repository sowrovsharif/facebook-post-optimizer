# 💬 Facebook Post Optimizer

A smart Facebook status generator and optimizer powered by AI. It helps you create engaging posts with keywords, hashtags, sentiment/emotion detection, fake news checking, and predicts potential reach. If the predicted reach is high enough, it can even auto-post to Facebook.

---

## 🚀 Features

- 🔑 Keyword & Hashtag Generator
- ✍️ Status Generator using AI
- 🎭 Emotion & Sentiment Detector
- 🚨 Fake News Checker
- 📈 Reach Predictor
- 🤖 Auto-post to Facebook if reach > threshold

---

## 🛠️ Setup Instructions

Follow the steps below to get started:

### ✅ 1. Open Project Folder

Open your terminal and navigate to the project directory: facebook_post_optimizer

### 🌱 2. Create a Virtual Environment
Run the following command to create a virtual environment:
python -m venv venv

### ⚙️ 3. Activate the Virtual Environment
For Windows:
venv\Scripts\activate
For macOS/Linux:
source venv/bin/activate
0r Drag and Drop activate.ps1 to Terminal and Press Enter

### 📦 4. Install Required Packages
Install all the required packages using the following command:
pip install -r requirements.txt

### 🔐 5. Configure Environment Variables
Create or edit a .env file in the root of your project folder. Add your API keys like this:
OPENAI_API_KEY=your_openai_api_key_here
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token_here

### ▶️ 6. Run the Application
Navigate to the src directory and start the Streamlit app:
cd src 
streamlit run main.py
