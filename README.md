# Rainbow Customer Assistant 🌈

A simple AI-powered customer support chatbot built with **Streamlit**, **Sentence Transformers**, and **semantic search**.  
It answers common customer questions such as orders, returns, warranty, repairs, and store information.

## Features

- Semantic FAQ search using **SentenceTransformer (all-MiniLM-L6-v2)**
- Cosine similarity matching for accurate responses
- Order tracking intent detection
- Clean chat-style UI
- Streamlit web interface
- JSON-based knowledge base
- Custom CSS styling

## Project Structure
# Project Structure


CHABOT_COMPANY/
│
├── app.py
├── app2.py
├── knowledge_base.json
├── logo.jpeg
├── README.md
└── requirements.txt


---

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd CHABOT_COMPANY
2. Install dependencies
pip install -r requirements.txt
Running the App

Start the Streamlit application:

streamlit run app.py

The chatbot will open in your browser.

Knowledge Base

The chatbot answers questions using the knowledge_base.json file.

Example format:

[
  {
    "question": "How can I return an item?",
    "answer": "You can return items within 30 days with the original receipt."
  }
]

You can expand this file to improve chatbot responses.

Technologies Used

Python

Streamlit

Sentence Transformers

Scikit-learn

NumPy

License

This project is for educational and demonstration purposes.