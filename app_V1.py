import streamlit as st
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import base64
from pathlib import Path
import re

# -----------------------------
# Page Config
# -----------------------------

st.set_page_config(
    page_title="Rainbow Customer Assistant",
    page_icon="🌈",
    layout="centered"
)

# -----------------------------
# Load Logo as Base64
# -----------------------------

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

logo_base64 = get_base64_image("logo.jpeg")

# -----------------------------
# Custom CSS + HTML Header with Logo
# -----------------------------

st.markdown(f"""
    <style>
        /* Remove default Streamlit top padding and overflow clipping */
        .block-container {{
            padding-top: 1.5rem !important;
            overflow: visible !important;
        }}

        section[data-testid="stMain"] > div {{
            overflow: visible !important;
        }}

        /* Header bar */
        .header-container {{
            display: flex;
            align-items: center;
            gap: 16px;
            background: linear-gradient(135deg, #121212 0%, #1f1f1f 100%);
            padding: 16px 28px;
            border-radius: 5px;
            margin-bottom: 10px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.5);
            width: 100%;
            box-sizing: border-box;
            border: 1px solid #3a3a3a;
            min-height: 150px;
        }}

        /* Logo wrapper — clips to logo shape using screen blend */
        .header-logo-wrap {{
            flex-shrink: 0;
            width: 110px;
            height: 72px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #1a1a1a;
            border-radius: 8px;
            overflow: hidden;
        }}

        .header-logo {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            mix-blend-mode: screen;
        }}

        /* Vertical divider */
        .header-divider {{
            width: 2px;
            height: 52px;
            background: linear-gradient(180deg, #e63000, #f0a500);
            border-radius: 2px;
            flex-shrink: 0;
        }}

        /* Title */
        .header-title {{
            color: #ffffff;
            font-size: 1.35rem;
            font-weight: 700;
            font-family: 'Segoe UI', sans-serif;
            text-align: left;
            line-height: 1.3;
            flex: 1;
        }}

        .header-title span {{
            display: block;
            font-size: 0.82rem;
            font-weight: 400;
            color: #f0a500;
            margin-top: 5px;
            letter-spacing: 0.3px;
        }}
    </style>

    <div class="header-container">
        <div class="header-logo-wrap">
            <img class="header-logo" src="data:image/jpeg;base64,{logo_base64}" alt="Rainbow Logo" />
        </div>
        <div class="header-divider"></div>
        <div class="header-title">
            Rainbow Customer Assistant
            <span>Your support, simplified.</span>
        </div>
    </div>
""", unsafe_allow_html=True)

st.write(
    "Hello! Ask me about **orders, returns, warranty, repairs, or store information.**"
)

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

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

question_embeddings = model.encode(questions)

# -----------------------------
# FAQ Search Function
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
# Order Tracking Detection
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



def detect_greeting(text):
    greetings = ["hi", "hello", "hey"]

    text = text.lower().strip()

    words = re.findall(r"\b\w+\b", text)

    if len(words) <= 3:
        for g in greetings:
            if g == words[0]:
                return True

    return False

# -----------------------------
# Chat History
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# -----------------------------
# Chat Input
# -----------------------------

user_input = st.chat_input("Type your message...")

if user_input:

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    if detect_greeting(user_input):
        response = "Hello! 👋 How can I assist you with your Rainbow Sandals today?"

    elif detect_order_tracking(user_input):
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

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    with st.chat_message("assistant"):
        st.write(response)
