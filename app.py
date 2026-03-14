import streamlit as st
import json
import base64
import re
from rapidfuzz import fuzz

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Rainbow Customer Assistant",
    page_icon="page_icon.ico",
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
# Custom CSS + HTML Header
# -----------------------------
st.markdown(f"""
<style>
.block-container {{ padding-top: 1.5rem !important; overflow: visible !important; }}
section[data-testid="stMain"] > div {{ overflow: visible !important; }}

.header-container {{
display:flex; align-items:center; gap:16px;
background:linear-gradient(135deg,#121212,#1f1f1f);
padding:16px 10px; border-radius:5px;
margin-bottom:10px;
box-shadow:0 3px 10px rgba(0,0,0,0.5);
border:0px solid #3a3a3a;
min-height:150px;
}}

.header-logo-wrap {{
width:110px; height:72px;
display:flex; align-items:center; justify-content:center;
background:#1a1a1a;
border-radius:8px;
overflow:hidden;
}}

.header-logo {{
width:100%;
height:100%;
object-fit:contain;
}}

.header-divider {{
width:2px;
height:52px;
background:linear-gradient(180deg,#e63000,#f0a500);
border-radius:2px;
}}

.header-title {{
color:white;
font-size:1.35rem;
font-weight:700;
}}

.header-title span {{
display:block;
font-size:0.82rem;
color:#f0a500;
margin-top:5px;
}}
</style>

<div class="header-container">
<div class="header-logo-wrap">
<img class="header-logo" src="data:image/jpeg;base64,{logo_base64}">
</div>
<div class="header-divider"></div>
<div class="header-title">
Rainbow Customer Assistant
<span>Your support, simplified.</span>
</div>
</div>
""", unsafe_allow_html=True)

st.write("Hello! Ask me about **orders, returns, warranty, repairs, or store information.**")

# -----------------------------
# Load FAQ Data
# -----------------------------
with open("intents.json", encoding="utf-8") as f:
    faq_data = json.load(f)

# -----------------------------
# Clean Response
# -----------------------------
def clean_response(text):
    return re.sub(r'`([^`]*)`', r'\1', text)

# -----------------------------
# Greeting Detection
# -----------------------------
def detect_greeting(text):
    greetings = ["hi","hello","hey",'heyy',"heyyy","good morning", "good evening","good afternoon", "hallo", "hii"]
    words = re.findall(r"\b\w+\b", text.lower())

    if len(words)<=3:
        if words and words[0] in greetings:
            return True
    return False

# -----------------------------
# Tracking Phrase Detection
# -----------------------------
tracking_phrases = [

"track my order","track order","where is my order",
"order status","check my order",
"track package","track shipment",
"tracking number","where is my package",
"where is my shipment"
]

def detect_order_tracking(text):
    text=text.lower()
    for phrase in tracking_phrases:
        if phrase in text:
            return True
    return False

# -----------------------------
# Detect Order Info
# -----------------------------
def detect_order_info_provided(text):

    if re.search(r'\b[0-9]{4,}\b',text):
        return True

    if re.search(r'\b[A-Z0-9]{5,}\b',text,re.IGNORECASE):
        return True

    if re.search(r'\b\d{5}\b',text):
        return True

    if re.search(r'\d+\s+\w+\s+(st|street|ave|avenue|blvd|road|rd|dr|lane)',text,re.IGNORECASE):
        return True

    if len(text.split())>=2:
        return True

    return False

# -----------------------------
# Sample Tracking Response
# -----------------------------
def sample_tracking_response():
    return (
        "Thanks! I found your order.\n\n"
        "Your package has shipped and is currently in transit.\n\n"
        "Tracking Number: 123456789\n\n"
        "Track your shipment here:\n"
        "https://tools.usps.com/go/TrackConfirmAction_input"
    )

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages=[]

if "waiting_for_tracking" not in st.session_state:
    st.session_state.waiting_for_tracking=False

if "tracking_faq_id" not in st.session_state:
    st.session_state.tracking_faq_id=None

# -----------------------------
# Display Chat History
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -----------------------------
# Chat Input
# -----------------------------
user_input=st.chat_input("Type your message...")

if user_input:

    st.session_state.messages.append({"role":"user","content":user_input})

    with st.chat_message("user"):
        st.write(user_input)

    response=""

# -----------------------------
# BOT LOGIC
# -----------------------------
    if detect_greeting(user_input):

        response="Hello! 👋 How can I assist you with your Rainbow Sandals today?"

# -----------------------------
# Waiting for order info
# -----------------------------
    elif st.session_state.waiting_for_tracking:

        if detect_order_info_provided(user_input):

            response=sample_tracking_response()
            st.session_state.waiting_for_tracking=False
            st.session_state.tracking_faq_id=None

        else:

            if st.session_state.tracking_faq_id == 7:

                response=(
                "Please provide one of the following so I can check your order:\n\n"
                "- Order Number\n\n"
                "OR\n\n"
                "- Full Name + Billing Address"
                )

            else:

                response=(
                "Please provide:\n\n"
                "- Order Number\n\n"
                "OR\n\n"
                "- Full Name + Billing Address"
                )

# -----------------------------
# Detect Tracking Phrases
# -----------------------------
    elif detect_order_tracking(user_input):

        response=(
        "Please provide:\n\n"
        "- Order Number\n\n"
        "OR\n\n"
        "- Full Name + Billing Address"
        )

        st.session_state.waiting_for_tracking=True
        st.session_state.tracking_faq_id=None

# -----------------------------
# FAQ Matching (UPDATED)
# -----------------------------
    else:

        def normalize(text):
            text = text.lower()
            text = re.sub(r'[^\w\s]', '', text)
            return text

        matched_faq = None
        best_score = 0

        user_text = normalize(user_input)

        THRESHOLD = 70

        for item in faq_data:

            phrases = []

            phrases.append(item.get("question",""))

            intents = item.get("intents",[])
            phrases.extend(intents)

            for phrase in phrases:

                phrase = normalize(phrase)

                score = fuzz.partial_ratio(user_text, phrase)

                if score > best_score:
                    best_score = score
                    matched_faq = item

        if best_score >= THRESHOLD:

            if matched_faq["id"] == 7:

                response = clean_response(matched_faq["answer"])

                st.session_state.waiting_for_tracking = True
                st.session_state.tracking_faq_id = 7

            else:

                response = clean_response(matched_faq["answer"])

        else:

            response=(
            "I'm not able to fully answer that question.\n\n"
            "Let me connect you with a customer service representative who can assist you."
            )

# -----------------------------
# Save + Display Response
# -----------------------------
    st.session_state.messages.append({"role":"assistant","content":response})

    with st.chat_message("assistant"):
        st.write(response)
