
# import streamlit as st
# from datetime import datetime
# from firebase_db import get_reviews, add_review, save_review_reply
# from ai_model import generate_ai_response
# from config import RESTAURANT_ID

# st.set_page_config(page_title="Restaurant Reviews", layout="centered")

# if "page" not in st.session_state:
#     st.session_state.page = "home"


# if st.session_state.page == "home":
#     st.title("Restaurant: ABC")

#     reviews = get_reviews(RESTAURANT_ID)

#     st.subheader("Customer Reviews")
#     if reviews:
#         for r in reviews:
         
#             review_time = r["created_at"]
#             if isinstance(review_time, datetime):
#                 review_time_str = review_time.strftime("%Y-%m-%d %H:%M")
#             else:
#                 review_time_str = str(review_time)

#             st.write(f"⭐ {r['stars']} — **{r['name']}** ({review_time_str})")
#             st.write(r["review"])

#             if "ai_reply" in r:
#                 st.info(f"💬 Restaurant reply: {r['ai_reply']}")
#             else:
#                 st.warning("No reply yet")

#             st.divider()
#     else:
#         st.info("No reviews yet.")

# if st.button("Add Review"):
#     st.session_state.page = "add_review"
#     st.rerun()


# if st.session_state.page == "add_review":
#     st.title("Add Review")

#     stars = st.slider("Stars", 1, 5, 5)
#     name = st.text_input("Your Name")
#     review = st.text_area("Your Review")

#     col1, col2 = st.columns(2)

#     with col1:
#         if st.button("Submit"):
#             if name and review:
                
#                 review_id = add_review(RESTAURANT_ID, name, stars, review)
#                 ai_reply = generate_ai_response(stars, review)
#                 save_review_reply(RESTAURANT_ID, review_id, ai_reply)
#                 st.session_state.page = "home"
#                 st.rerun()
#             else:
#                 st.warning("Please fill all fields")

#     with col2:
#         if st.button("Cancel"):
#             st.session_state.page = "home"
#             st.rerun()

import streamlit as st
from datetime import datetime
from firebase_db import get_reviews, add_review, save_review_reply
from ai_model import generate_ai_response
from config import RESTAURANT_ID

st.set_page_config(page_title="Restaurant Reviews", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    # Title and Add Review button in one row
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title("Restaurant: ABC")
    
    with col2:
        if st.button("Add Review"):
            st.session_state.page = "add_review"
            st.rerun()

    reviews = get_reviews(RESTAURANT_ID)

    st.subheader("Customer Reviews")
    if reviews:
        for r in reviews:
            review_time = r["created_at"]
            if isinstance(review_time, datetime):
                review_time_str = review_time.strftime("%Y-%m-%d %H:%M")
            else:
                review_time_str = str(review_time)

            st.write(f"⭐ {r['stars']} — **{r['name']}** ({review_time_str})")
            st.write(r["review"])

            if "ai_reply" in r:
                st.info(f"💬 Restaurant reply: {r['ai_reply']}")
            else:
                st.warning("No reply yet")

            st.divider()
    else:
        st.info("No reviews yet.")

if st.session_state.page == "add_review":
    st.title("Add Review")

    stars = st.slider("Stars", 1, 5, 5)
    name = st.text_input("Your Name")
    review = st.text_area("Your Review")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Submit"):
            if name and review:
                review_id = add_review(RESTAURANT_ID, name, stars, review)
                ai_reply = generate_ai_response(stars, review)
                save_review_reply(RESTAURANT_ID, review_id, ai_reply)
                st.session_state.page = "home"
                st.rerun()
            else:
                st.warning("Please fill all fields")

    with col2:
        if st.button("Cancel"):
            st.session_state.page = "home"
            st.rerun()
