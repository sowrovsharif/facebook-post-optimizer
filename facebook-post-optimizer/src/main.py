import streamlit as st
import pandas as pd
import plotly.express as px
import re

# ↓ your helper modules (unchanged) ↓
from reach_predictor import train_model, interpret_prediction
from keyword_finder import extract_keywords
from hashtag_generator import generate_hashtags
from status_generator import generate_status_updates
from fake_news_checker import check_status_genuineness
from emotion_detector import detect_emotion
from auto_post_scheduler import post_to_facebook   # must be configured with ACCESS_TOKEN + PAGE_ID

# ────────────────────────────────────────────────────────────────
#  Helpers
# ────────────────────────────────────────────────────────────────
WEEKDAY = {1: "Sunday", 2: "Monday", 3: "Tuesday", 4: "Wednesday",
           5: "Thursday", 6: "Friday", 7: "Saturday"}

@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(r"E:\facebook_post_optimizer\Facebook_Metrics.csv")

@st.cache_data
def load_model(df: pd.DataFrame):
    return train_model(df)

def best_day_chart(df: pd.DataFrame):
    """Show average reach per weekday and highlight the winner."""
    st.subheader("📊 Best Day to Post (historical)")
    by_day = df.groupby("Post Weekday")["Lifetime Post Total Reach"].mean().reset_index()
    by_day["Weekday"] = by_day["Post Weekday"].map(WEEKDAY)

    top = by_day.sort_values("Lifetime Post Total Reach", ascending=False).iloc[0]
    st.markdown(
        f"<div style='font-size:18px'>📅 <b>Best:</b> <code>{WEEKDAY[top['Post Weekday']]}</code> "
        f"with <b>{int(top['Lifetime Post Total Reach']):,}</b> average reach</div>",
        unsafe_allow_html=True,
    )

    fig = px.bar(
        by_day,
        x="Weekday",
        y="Lifetime Post Total Reach",
        labels={"Lifetime Post Total Reach": "Avg Reach"},
        color="Lifetime Post Total Reach",
        color_continuous_scale="Blues",
        title="Average Reach by Weekday",
    )
    fig.update_layout(title_x=0.5, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)


def extract_reach_number(text: str) -> int:
    """
    Extract the number that appears just before the word 'people' in the string.
    """
    match = re.search(r'(\d{1,3}(?:,\d{3})*)\s+people', text)
    if match:
        number_str = match.group(1).replace(',', '')
        return int(number_str)
    else:
        raise ValueError("No numeric reach found before 'people' in prediction result")


# ────────────────────────────────────────────────────────────────
#  Main App
# ────────────────────────────────────────────────────────────────
def main():
    st.set_page_config("Facebook Post Optimizer", "🚀", layout="centered")
    st.title("🚀 Facebook Post Reach Optimizer")

    df = load_data()
    model = load_model(df)

    # ----------------------------------------------------------------------------
    # 1) PREDICTION FORM  ➜ saves st.session_state.predicted_reach
    # ----------------------------------------------------------------------------
    with st.sidebar.form("predict"):
        st.header("🎯 Predict Reach")
        post_type  = st.selectbox("Post Type", df["Type"].unique())
        weekday    = st.slider("Post Weekday (1=Sun, 7=Sat)", 1, 7, 3)
        hour       = st.slider("Post Hour (0-23)", 0, 23, 16)
        paid       = st.selectbox("Paid Post?", [0, 1])
        page_likes = st.number_input("Page Likes", 0, value=140_000)
        category   = st.selectbox("Category", df["Category"].unique())

        submit_pred = st.form_submit_button("🔮 Predict Reach")

    if submit_pred:
        result = interpret_prediction(model, post_type, weekday, hour, paid, page_likes, category)
        st.session_state.predicted_reach = result  # full message string

        try:
            predicted_number = extract_reach_number(result)
            st.session_state.predicted_reach_num = predicted_number

            st.sidebar.markdown(f"**Prediction:** {result}")
            st.sidebar.success(f"Extracted Reach: {predicted_number:,} people")
        except Exception as e:
            st.sidebar.error(f"Error parsing predicted reach: {e}")

    # ----------------------------------------------------------------------------
    # 2) STATUS GENERATOR FORM  ➜ saves st.session_state.generated_status
    # ----------------------------------------------------------------------------
    with st.form("generate"):
        st.header("✨ One-Click Status Generator")
        seed_text = st.text_area("💬 Your idea", height=150)
        submit_gen = st.form_submit_button("🚀 Generate")

    if submit_gen:
        if not seed_text.strip():
            st.error("Please write something first.")
        else:
            keywords  = extract_keywords(seed_text)
            hashtags  = generate_hashtags(keywords)
            candidates = generate_status_updates(keywords, hashtags)
            final_status = (candidates[0] if candidates else seed_text) + " " + " ".join(hashtags)

            st.session_state.generated_status = final_status
            emotion, conf = detect_emotion(final_status)
            genuineness   = check_status_genuineness(final_status)

            # Show the fully-enhanced status
            st.subheader("📝 Enhanced Status")
            st.markdown(f"""
<div style='padding:15px;background:#f9f9f9;border-left:5px solid #4CAF50'>
<b>Status:</b><br>{final_status}<br><br>
<b>Keywords:</b> {', '.join(keywords)}<br>
<b>Hashtags:</b> {' '.join(hashtags)}<br>
<b>Emotion:</b> {emotion} ({conf*100:.1f}%)<br><br>
<b>🕵️‍♂️ Genuineness:</b><br>
{"<br>".join(f"- {k.title()}: {v}%" for k, v in genuineness['classification'].items())}
</div>
""", unsafe_allow_html=True)

    # ----------------------------------------------------------------------------
    # 3) POST TO FACEBOOK (enabled only when both requirements met)
    # ----------------------------------------------------------------------------
    ready = (
        "predicted_reach_num" in st.session_state
        and isinstance(st.session_state.predicted_reach_num, int)
        and st.session_state.predicted_reach_num > 15_000
        and "generated_status" in st.session_state
    )

    post_clicked = st.button("✅ Post to Facebook Now",
                             type="primary",
                             disabled=not ready)

    if post_clicked:
        try:
            resp = post_to_facebook(st.session_state.generated_status)
            st.success("🎉 Posted successfully!")
            st.json(resp)          # show API response (optional)
        except Exception as ex:
            st.error(f"❌ Failed to post: {ex}")

    # ----------------------------------------------------------------------------
    # 4) HISTORICAL BEST DAY
    # ----------------------------------------------------------------------------
    st.markdown("---")
    best_day_chart(df)


if __name__ == "__main__":
    main()
