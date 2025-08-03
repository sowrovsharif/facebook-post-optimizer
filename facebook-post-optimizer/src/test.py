import streamlit as st
import pandas as pd
import plotly.express as px
from reach_predictor import train_model, interpret_prediction
from keyword_finder import extract_keywords
from hashtag_generator import generate_hashtags
from status_generator import generate_status_updates
from fake_news_checker import check_status_genuineness
from emotion_detector import detect_emotion
from auto_post_scheduler import post_to_facebook




# Map for weekday numbers to names
weekday_map = {
    1: 'Sunday', 2: 'Monday', 3: 'Tuesday', 4: 'Wednesday',
    5: 'Thursday', 6: 'Friday', 7: 'Saturday'
}

@st.cache_data
def load_data():
    return pd.read_csv(r"E:\facebook_post_optimizer\Facebook_Metrics.csv")

@st.cache_data
def get_model(df):
    return train_model(df)

def show_best_day_chart(df):
    st.subheader("📊 Best Day to Post (Based on Historical Reach)")

    # Calculate average reach by day
    avg_reach_by_day = df.groupby('Post Weekday')['Lifetime Post Total Reach'].mean().reset_index()
    best_day = avg_reach_by_day.sort_values(by='Lifetime Post Total Reach', ascending=False).iloc[0]

    # Map numeric day to name
    avg_reach_by_day['Weekday'] = avg_reach_by_day['Post Weekday'].map(weekday_map)
    day_name = weekday_map[best_day['Post Weekday']]
    avg_reach = int(best_day['Lifetime Post Total Reach'])

    st.markdown(
        f"<div style='font-size:18px;'>📅 <b>Best Day to Post:</b> <code>{day_name}</code> "
        f"with average reach of <b>{avg_reach:,}</b> people.</div>",
        unsafe_allow_html=True
    )

    # Plot with Plotly
    fig = px.bar(
        avg_reach_by_day,
        x='Weekday',
        y='Lifetime Post Total Reach',
        title="📈 Average Reach by Day of the Week",
        labels={'Lifetime Post Total Reach': 'Average Reach'},
        color='Lifetime Post Total Reach',
        color_continuous_scale='Blues'
    )
    fig.update_layout(
        xaxis_title="Day of the Week",
        yaxis_title="Average Reach",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(size=14),
        title_x=0.5
    )

    st.plotly_chart(fig, use_container_width=True)

def main():
    st.set_page_config(page_title="Facebook Reach Optimizer", page_icon="🚀", layout="centered")
    st.title("🚀 Facebook Post Reach Optimizer")

    df = load_data()
    model = get_model(df)

    st.sidebar.header("🎯 Predict Post Reach")
    post_type = st.sidebar.selectbox("Post Type", df['Type'].unique())
    weekday = st.sidebar.slider("Post Weekday (1=Sun, 7=Sat)", 1, 7, 3)
    hour = st.sidebar.slider("Post Hour (0-23)", 0, 23, 16)
    paid = st.sidebar.selectbox("Paid Post?", [0, 1])
    page_likes = st.sidebar.number_input("Page Total Likes", min_value=0, value=140000)
    category = st.sidebar.selectbox("Category", df['Category'].unique())

    if st.sidebar.button("🔮 Predict Reach"):
        result = interpret_prediction(model, post_type, weekday, hour, paid, page_likes, category)
        st.success(result)

    st.markdown("---")
    show_best_day_chart(df)

if __name__ == "__main__":
    main()



input_status = st.text_area("Enter your Facebook status here:", height=150)

# Store keywords and hashtags in session state to keep between button clicks
if 'keywords' not in st.session_state:
    st.session_state.keywords = []
if 'hashtags' not in st.session_state:
    st.session_state.hashtags = []
if 'generated_statuses' not in st.session_state:
    st.session_state.generated_statuses = []

col1, col2 = st.columns(2)

with col1:
    if st.button("Extract Keywords & Hashtags"):
        if input_status.strip() == "":
            st.warning("Please enter some status text first.")
        else:
            # Extract keywords
            keywords = extract_keywords(input_status)
            st.session_state.keywords = keywords

            # Generate hashtags from keywords
            hashtags = generate_hashtags(keywords)
            st.session_state.hashtags = hashtags

            st.success("Keywords and Hashtags extracted!")
            st.write("### Keywords:")
            st.write(", ".join(keywords) if keywords else "No keywords found.")
            st.write("### Hashtags:")
            st.write(" ".join(hashtags) if hashtags else "No hashtags generated.")

with col2:
    if st.button("Generate New Status"):
        if not st.session_state.keywords or not st.session_state.hashtags:
            st.warning("First extract keywords and hashtags before generating new status updates.")
        else:
            # Generate new statuses using saved keywords and hashtags
            new_statuses = generate_status_updates(st.session_state.keywords, st.session_state.hashtags)
            st.session_state.generated_statuses = new_statuses

            if new_statuses:
                st.success("New status updates generated!")
                for i, status in enumerate(new_statuses, 1):
                    # Detect emotion for each generated status
                    emotion, confidence = detect_emotion(status)
                    st.write(f"**Status {i}:** {status}")
                    if emotion:
                        st.write(f"Emotion: {emotion} ({confidence*100:.1f}%)")
                    st.write("---")
            else:
                st.info("No new status updates generated.")

# Optionally, show saved keywords, hashtags, and statuses if already generated
if st.session_state.keywords and st.session_state.hashtags:
    st.write("### Current Keywords:")
    st.write(", ".join(st.session_state.keywords))
    st.write("### Current Hashtags:")
    st.write(" ".join(st.session_state.hashtags))

if st.session_state.generated_statuses:
    st.write("### Generated Status Updates:")
    for i, status in enumerate(st.session_state.generated_statuses, 1):
        st.write(f"**Status {i}:** {status}")

st.subheader("🕵️ Fake News Detector")
user_text = st.text_area("Enter a status to verify if it's real, fake or misleading:", key="fake_check_input")

if st.button("Check Status Genuineness"):
    if user_text.strip() == "":
        st.warning("Please enter a status to check.")
    else:
        result = check_status_genuineness(user_text)
        st.success("Results:")
        st.write("### 🔍 Classification (BART Zero-Shot):")
        for label, score in result["classification"].items():
            st.write(f"- **{label.title()}**: {score}%")


