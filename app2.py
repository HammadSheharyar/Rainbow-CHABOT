import streamlit as st
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# Page Config
# -----------------------------

st.set_page_config(
    page_title="Rainbow Customer Assistant",
    page_icon="🌈",
    layout="centered"
)

# -----------------------------
# Styling
# -----------------------------

st.markdown("""
<style>

body {
    background-color: #121212;  /* dark background */
    color: #eee;
    font-family: Arial, sans-serif;
}

.chatbot-title {
    text-align: center;
    font-size: 32px;
    font-weight: bold;
    color: #ff6f61;
    margin-bottom: 10px;
}

/* Container for each user-bot message pair */
.message-pair {
    display: flex;
    flex-direction: column;
    margin-bottom: 20px;  /* space between pairs */
    max-width: 70%;
    word-wrap: break-word;
}

/* User message style */
.user-message {
    background-color: #ff6f61;
    color: white;
    padding: 12px;
    border-radius: 10px;
    text-align: right;
    align-self: flex-end;  /* right align */
}

/* Bot message style */
.bot-message {
    background-color: #2c2c2c;  /* dark gray */
    color: #f0f0f0;
    padding: 12px;
    border-radius: 10px;
    text-align: left;
    margin-top: 6px;  /* gap below user message */
    align-self: flex-start;  /* left align */
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.image("logo.jpeg", width=120)  # Add your logo image here
st.markdown('<div class="chatbot-title">🌈 Rainbow Customer Assistant</div>', unsafe_allow_html=True)

st.write("Hello! Ask me about orders, returns, warranty, repairs, or store information.")

# -----------------------------
# Load Dataset
# -----------------------------

with open("knowledge_base.json", encoding="utf-8") as f:
    faq_data = json.load(f)

questions = [item["question"] for item in faq_data]
answers = [item["answer"] for item in faq_data]

# -----------------------------
# Load Embedding Model
# -----------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")
question_embeddings = model.encode(questions)

# -----------------------------
# Search Function
# -----------------------------

def search_faq(user_input):
    query_embedding = model.encode([user_input])
    similarity = cosine_similarity(query_embedding, question_embeddings)
    best_match = np.argmax(similarity)
    score = similarity[0][best_match]

    if score > 0.45:
        return answers[best_match]

    return None

# -----------------------------
# Intent Detection
# -----------------------------

def detect_order_tracking(text):
    keywords = [
        "track order",
        "where is my order",
        "order status",
        "tracking number",
        "track my package"
    ]
    text = text.lower()
    for k in keywords:
        if k in text:
            return True
    return False

# -----------------------------
# Chat History Initialization
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Display Messages In Pairs
# -----------------------------

for i in range(0, len(st.session_state.messages), 2):
    user_msg = st.session_state.messages[i]["content"]
    bot_msg = ""
    if i + 1 < len(st.session_state.messages):
        bot_msg = st.session_state.messages[i + 1]["content"]

    st.markdown(
        f"""
        <div class="message-pair">
            <div class="user-message">{user_msg}</div>
            <div class="bot-message">{bot_msg}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------
# User Input
# -----------------------------

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Check for order tracking intent
    if detect_order_tracking(user_input):
        response = """
Please provide:

• Order Number  
OR  
• Full Name + Billing Address
"""
    else:
        faq_answer = search_faq(user_input)
        if faq_answer:
            response = faq_answer
        else:
            response = """
I'm not able to fully answer that question.

Let me connect you with a customer service representative who can assist you.
"""

    st.session_state.messages.append({"role": "assistant", "content": response})

    st.experimental_singleton.clear()
    st.experimental_memo.clear()
    st.session_state.clear()