

import google.generativeai as genai
from openai import OpenAI

import streamlit as st
import google.generativeai as genai

# Configure Gemini once
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])


# OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

# genai.configure(api_key=st.secrets["GEMINI_API_KEY"])


# genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")
model2=genai.GenerativeModel("gemma-3-27b-it")




def generate_ai_response(stars, review_text):
    prompt = f"""
You are the owner of a restaurant.
understand review and then give  you can keep it short like few lines
Write a polite, friendly public reply to this customer review.
Sound human and appreciative.
Constraints:
- Do not mention star ratings explicitly.
- do not write big stories or email format

Review:
{stars} stars - {review_text}

Write only the reply message.
"""

    response = model.generate_content(prompt)
    return response.text.strip()

# using gemini
def generate_monthly_summary(reviews):
    if not reviews:
        return "No reviews this month."

    text = ""
    for r in reviews:
        text += f"- {r['stars']} stars: {r['review']}\n"

    prompt = f"""
ou are a restaurant review analyst.
Your task is to read and interpret customer reviews from the past month and produce a clear, concise summary of overall customer sentiment and experience.
Context:
The reviews include star ratings and short written feedback from multiple customers. They may mention food quality, service, ambiance, speed, or overall satisfaction. Opinions can be mixed.
Constraints:
- Focus on recurring themes rather than individual comments
- Highlight both positive and negative trends if present
- keep the summary brief and easy to understand
- Do not list individual reviews or star ratings
- use natural, human-sounding language
Output format:
Write one short paragraph (3–5 sentences) that summarizes how customers generally feel about the restaurant this month.

Reviews:
{text}
"""

    response = model2.generate_content(prompt)
    return response.text.strip()

# # using openroute
# def generate_monthly_summary(reviews):
#     if not reviews:
#         return "No reviews this month."

#     text = ""
#     for r in reviews:
#         text += f"- {r['stars']} stars: {r['review']}\n"

#     prompt = f"""
# You are analyzing customer feedback for a restaurant.

# Based on the reviews below, write a concise overall summary
# of customer sentiment and experience for this month.

# Reviews:
# {text}
# """

#     response = client.chat.completions.create(
#         model="tngtech/deepseek-r1t2-chimera:free",
#         messages=[{"role": "user", "content": prompt}],
#     )

#     return response.choices[0].message.content.strip()



def generate_recommended_actions(reviews):
    if not reviews:
        return "No recommendations available."

    text = ""
    for r in reviews:
        text += f"- {r['stars']} stars: {r['review']}\n"

    prompt = f"""
You are a restaurant consultant.you have good 20 yrs of experince in Hospitality domain
Based on the reviews below, suggest 3 clear, practical actions which need to give attention as early as possible
the restaurant should take to improve.from your suggestion our ultimate goal will be give best hospitality to customer.
Do not write things in very detail just keep 2-3 points realted to one suggestion
Reviews:
{text}
"""

    response = model.generate_content(prompt)
    return response.text.strip()

# using geimini
def classify_sentiment(review_text):
    prompt = f"""you are sentiment analysis expert.you have to go through all the reviws and give them one
    category. I have made 4 catgories  as happy, neutral, sad, angry.you have to add them in each one bucket

Review:
{review_text}

Return only the category name.
"""

    response = model2.generate_content(prompt)
    return response.text.strip().lower()

# using openroute
# def classify_sentiment(review_text):
#     prompt = f"""you are sentiment analysis expert.you have to go through all the reviws and give them one
#     category. I have made 4 catgories  as happy, neutral, sad, angry.you have to add them in each one bucket

# Review:
# {review_text}

# Return only the category name.
# """

#     response = client.chat.completions.create(
#         model="tngtech/deepseek-r1t2-chimera:free",
#         messages=[{"role": "user", "content": prompt}],
#     )

#     return response.choices[0].message.content.strip().lower()


# from openai import OpenAI
# from config import OPENROUTER_API_KEY

# client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key=OPENROUTER_API_KEY,
# )


# def generate_ai_response(reviews):
#     if not reviews:
#         return "No reviews yet."

#     combined_reviews = ""
#     for r in reviews:
#         combined_reviews += f"{r['stars']} stars: {r['review']}\n"

#     response = client.chat.completions.create(
#         model="tngtech/deepseek-r1t2-chimera:free",
#         messages=[
#             {
#                 "role": "user",
#                 "content": f"""
# These are restaurant reviews.
# Write a short friendly summary and one improvement suggestion.

# Reviews:
# {combined_reviews}
# """
#             }
#         ],
#         extra_body={"reasoning": {"enabled": True}},
#     )

#     return response.choices[0].message.content
