
import streamlit as st
from datetime import datetime
import calendar
import plotly.express as px

from firebase_db import get_reviews
from ai_model import (
    generate_monthly_summary,
    generate_recommended_actions,
    classify_sentiment,
)
from config import RESTAURANT_ID

st.set_page_config(page_title="Review Analytics", layout="wide")
st.title("Restaurant Review Analytics")

# ---------------- LOAD DATA ----------------
reviews = get_reviews(RESTAURANT_ID)

if not reviews:
    st.info("No reviews available.")
    st.stop()

# ---------------- MONTH DROPDOWN ----------------
months = list(calendar.month_name)[1:]  # ['January', ..., 'December']
now = datetime.utcnow()
default_month = now.month
selected_month = st.selectbox(
    "Select Month for Analytics",
    options=months,
    index=default_month - 1
)
selected_month_num = months.index(selected_month) + 1

# ---------------- FILTER BY MONTH ----------------
monthly_reviews = [
    r for r in reviews
    if r["created_at"].month == selected_month_num
    and r["created_at"].year == now.year
]

st.subheader(f"Customer Submissions ({selected_month})")
for r in reviews:
    review_time_str = r["created_at"].strftime("%Y-%m-%d %H:%M")
    st.write(f"⭐ {r['stars']} — {r['review']} ({review_time_str})")

st.divider()

# ---------------- AI INSIGHTS ----------------
st.subheader(f"AI Insights ({selected_month})")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Monthly Summary")
    with st.spinner("Generating summary..."):
        summary = generate_monthly_summary(monthly_reviews)
    st.write(summary)

with col2:
    st.markdown("### Recommended Actions")
    with st.spinner("Generating actions..."):
        actions = generate_recommended_actions(monthly_reviews)
    st.write(actions)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown("###  Star Rating Distribution")
    stars = [r["stars"] for r in reviews]
    star_fig = px.histogram(
        x=stars,
        nbins=5,
        labels={"x": "Star Rating"},
    )
    star_fig.update_layout(
        yaxis_title="Number of Reviews",
        bargap=0.2,
    )
    st.plotly_chart(star_fig, use_container_width=True)

# Sentiment Analysis
with col2:
    st.markdown("###  Sentiment Distribution")
    sentiment_counts = {"happy": 0, "neutral": 0, "sad": 0, "angry": 0}
    with st.spinner("Analyzing sentiments..."):
        for r in reviews:
            sentiment = classify_sentiment(r["review"])
            if sentiment in sentiment_counts:
                sentiment_counts[sentiment] += 1

    sentiment_fig = px.bar(
        x=list(sentiment_counts.keys()),
        y=list(sentiment_counts.values()),
        labels={"x": "Sentiment", "y": "Number of Reviews"},
    )
    st.plotly_chart(sentiment_fig, use_container_width=True)
