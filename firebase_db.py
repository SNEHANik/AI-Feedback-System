
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# if not firebase_admin._apps:
#     cred = credentials.Certificate("fyndassignment-firebase-adminsdk-fbsvc-c4a18256fb.json")
#     firebase_admin.initialize_app(cred)

# db = firestore.client()

import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": st.secrets["FIREBASE_PROJECT_ID"],
        "private_key_id": st.secrets["FIREBASE_PRIVATE_KEY_ID"],
        "private_key": st.secrets["FIREBASE_PRIVATE_KEY"].replace("\\n", "\n"),
        "client_email": st.secrets["FIREBASE_CLIENT_EMAIL"],
        "client_id": st.secrets["FIREBASE_CLIENT_ID"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": ""
    })
    firebase_admin.initialize_app(cred)

db = firestore.client()



def get_reviews(restaurant_id):
    docs = (
        db.collection("restaurants")
        .document(restaurant_id)
        .collection("reviews")
        .order_by("created_at", direction=firestore.Query.DESCENDING)
        .stream()
    )
    return [doc.to_dict() for doc in docs]


def add_review(restaurant_id, name, stars, review):
    ref = (
        db.collection("restaurants")
        .document(restaurant_id)
        .collection("reviews")
        .add({
            "name": name,
            "stars": stars,
            "review": review,
            "created_at": datetime.utcnow(),
        })
    )
    return ref[1].id


def save_ai_reply(restaurant_id, message):
    db.collection("restaurants") \
        .document(restaurant_id) \
        .set(
            {
                "ai_reply": {
                    "message": message,
                    "updated_at": datetime.utcnow(),
                }
            },
            merge=True,
        )


def get_ai_reply(restaurant_id):
    doc = db.collection("restaurants").document(restaurant_id).get()
    data = doc.to_dict()

    if data and "ai_reply" in data:
        return data["ai_reply"]["message"]

    return None
def save_review_reply(restaurant_id, review_id, ai_reply):
    db.collection("restaurants") \
        .document(restaurant_id) \
        .collection("reviews") \
        .document(review_id) \
        .update({
            "ai_reply": ai_reply
        })
