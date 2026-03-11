# 🌈 Rainbow Customer Assistant

An AI-powered **customer support chatbot** built using **Streamlit**, **Sentence Transformers**, and **semantic search**.  
The chatbot helps customers quickly find answers related to **orders, returns, warranty, repairs, shipping, and store information**.

The system retrieves the most relevant answer from a knowledge base using **semantic similarity**, allowing it to understand user questions even if they are phrased differently.

---

# 🚀 Live Demo (Cloud Deployment)

The application is deployed on **Streamlit Cloud**, allowing users to access the chatbot directly through a web browser without installing anything.

👉 Access the chatbot here:

**Rainbow Customer Assistant**  
https://rainbow-chabot-gcns2g6l892hvkgalpa9vd.streamlit.app/

Simply open the link and start chatting with the assistant.

---

# ✨ Features

- 🤖 **Semantic FAQ Search**
  - Uses **SentenceTransformer (all-MiniLM-L6-v2)** to understand question meaning.

- 🔎 **Cosine Similarity Matching**
  - Retrieves the most relevant answer using semantic similarity.

- 📦 **Order Tracking Detection**
  - Detects order tracking queries and requests required information.

- 💬 **Interactive Chat UI**
  - Built with Streamlit’s chat interface.

- 📚 **JSON Knowledge Base**
  - Easily expandable dataset of FAQ questions and answers.

- 🎨 **Custom UI**
  - Styled header with logo and clean layout.

- ⚡ **Fast and Lightweight**
  - Runs locally without requiring external APIs.

---

# 🧠 How the Chatbot Works

1. The chatbot loads FAQ questions from **knowledge_base.json**.
2. Each question is converted into an **embedding** using a **SentenceTransformer model**.
3. When a user asks a question:
   - The query is converted into an embedding.
   - **Cosine similarity** is calculated between the query and stored question embeddings.
4. The answer corresponding to the most similar question is returned if the similarity score exceeds a threshold.

---

# 📂 Project Structure

```
CHABOT_COMPANY/
│
├── app.py                # Main Streamlit chatbot application
├── app2.py               # Alternate/test version
├── knowledge_base.json   # FAQ dataset
├── logo.jpeg             # Logo used in the UI
├── README.md             # Project documentation
└── requirements.txt      # Python dependencies
```

---

# ⚙️ Requirements

- Python **3.8+**
- pip package manager

Required libraries:

- streamlit
- sentence-transformers
- scikit-learn
- numpy

---

# 🛠 Installation Guide (Run Locally)

Follow these steps to test the chatbot **on your local machine**.

---

## 1️⃣ Clone the Repository

```bash
git clone <your-repository-url>
cd CHABOT_COMPANY
```

---

## 2️⃣ Create Virtual Environment (Recommended)

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required libraries.

---

# ▶️ Running the Application Locally

Start the Streamlit app with:

```bash
streamlit run app.py
```

After running the command:

1. Streamlit will start a local server.
2. Your browser will open automatically.

If it does not open, visit:

```
http://localhost:8501
```

You can now interact with the chatbot locally.

---

# ☁️ Streamlit Cloud Deployment

This project is deployed using **Streamlit Cloud**, which allows hosting Streamlit apps directly from a GitHub repository.

### Deployment Steps

1. Push the project to a **GitHub repository**
2. Go to **Streamlit Cloud**
3. Connect your **GitHub account**
4. Select the repository
5. Set the main file as:

```
app.py
```

6. Deploy the application

Streamlit Cloud will automatically install dependencies from:

```
requirements.txt
```

Once deployed, the app will be accessible via a public URL.

---

# 🌐 Access the Deployed App

You can access the deployed chatbot here:

**Rainbow Customer Assistant**

https://rainbow-chabot-gcns2g6l892hvkgalpa9vd.streamlit.app/

No installation is required — simply open the link and start asking questions.

---

# 📚 Knowledge Base

The chatbot retrieves answers from **knowledge_base.json**.

Example format:

```json
[
  {
    "question": "How can I return an item?",
    "answer": "You can return items within 30 days with the original receipt."
  },
  {
    "question": "Do you ship internationally?",
    "answer": "Yes, we ship internationally. Shipping fees may vary depending on the destination."
  }
]
```

You can improve chatbot performance by:

- Adding more FAQ questions
- Expanding answer explanations
- Increasing dataset coverage

---

# 🧪 Example Questions to Try

Try asking the chatbot:

- Hello
- Do you ship internationally?
- How do I place an international order?
- How do I return an item?
- Where is my order?
- What is the warranty policy?

---

# 🧰 Technologies Used

- **Python**
- **Streamlit**
- **Sentence Transformers**
- **Scikit-learn**
- **NumPy**

---

# 📈 Possible Future Improvements

- Integrate **LLM models (GPT / Llama / Gemini)**
- Implement **Retrieval Augmented Generation (RAG)**
- Add **conversation memory**
- Build **analytics for customer queries**
- Add **customer support escalation**

---

# 📜 License

This project is intended for **educational and demonstration purposes**.

---

