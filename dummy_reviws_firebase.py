import pandas as pd
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
FIREBASE_KEY_PATH = "fyndassignment-firebase-adminsdk-fbsvc-c4a18256fb.json"

RESTAURANT_ID = "abc"

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_KEY_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()

df = pd.read_excel("reviews.xlsx")

for _, row in df.iterrows():
    name = row["name"]
    stars = int(row["stars"])
    review_text = row["review"]
    created_at = pd.to_datetime(row["created_at"])
    ai_reply = row["ai_reply"] if "ai_reply" in row and pd.notna(row["ai_reply"]) else None

    data = {
        "name": name,
        "stars": stars,
        "review": review_text,
        "created_at": created_at
    }
    if ai_reply:
        data["ai_reply"] = ai_reply

    db.collection("restaurants") \
      .document(RESTAURANT_ID) \
      .collection("reviews") \
      .add(data)

    print(f"Uploaded review: {name} - {stars} stars")
