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
# Header (Logo + Title)
# -----------------------------

# st.image("logo.jpeg", width=200)

st.title("🌈 Rainbow Customer Assistant")

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
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
    text = text.lower()
    for word in greetings:
        if word in text:
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

    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    # Display user message
    with st.chat_message("user"):
        st.write(user_input)

    # -----------------------------
    # Generate Response
    # -----------------------------

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

    # Save assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    # Display assistant message
    with st.chat_message("assistant"):
        st.write(response)