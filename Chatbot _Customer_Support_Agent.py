
## 💬 **Agent  AI Chatbot for Customer Support**

### 📝 Overview

This agent acts as a 24/7 customer support representative, answering FAQs, resolving common issues, and escalating complex queries. Powered by GPT, it uses context-aware responses, maintains session memory, and handles polite escalation. In this project, you’ll build an interactive GPT-based chatbot for simulated customer support interactions.

---

### 🧪 Objectives

By the end of this hands on, you will:

* Create a live chatbot interface using Streamlit
* Accept customer queries and return GPT responses
* Maintain basic conversation memory
* Simulate escalation for complex or unresolved issues

---

### 🧰 Tech Stack

* **Python**
* **Streamlit**
* **LangChain + GPT-4 or GPT-3.5**
* *(Optional: Add RAG or vector memory later)*

---

export OPENAI_API_KEY="your-secret-key"


### 🧭 Step-by-Step Instructions

#### ✅ Step 1: Environment Setup

```bash
mkdir ai_customer_chatbot
cd ai_customer_chatbot
python -m venv venv
source venv/bin/activate
pip install streamlit openai langchain
```

---

#### ✅ Step 2: Prompt Template (`chat_prompt.py`)

```python
from langchain.prompts import PromptTemplate

chat_prompt = PromptTemplate.from_template("""
You are an AI customer service chatbot.

Respond to the customer message below:
"{user_message}"

Your goals:
1. Be polite and professional
2. Solve the issue if possible
3. If the query is too complex, say: "Let me connect you with a human support agent."

Limit your reply to 100 words.
""")
```

---

#### ✅ Step 3: GPT Chat Logic (`chat_agent.py`)

```python
from langchain.chat_models import ChatOpenAI
from chat_prompt import chat_prompt

def customer_reply(user_message):
    llm = ChatOpenAI(temperature=0.4)
    prompt = chat_prompt.format(user_message=user_message)
    return llm.predict(prompt)
```

---

#### ✅ Step 4: Streamlit Chatbot UI (`app.py`)

```python
import streamlit as st
from chat_agent import customer_reply

st.title("💬 AI Chatbot for Customer Support")
st.caption("Ask a product or support-related question")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Your message:")

if st.button("Send"):
    if user_input:
        response = customer_reply(user_input)
        st.session_state.history.append(("Customer", user_input))
        st.session_state.history.append(("AI Support", response))

for speaker, message in reversed(st.session_state.history[-10:]):
    st.markdown(f"**{speaker}:** {message}")
```

Run the app:

```bash
streamlit run app.py
```

---

### 🧪 Example Dialog

**Customer:** I didn’t receive my order placed last Thursday.
**AI Chatbot:** I’m sorry to hear that! Please check your tracking number in your confirmation email. If you still can’t locate it, I’ll connect you with a human support agent.

**Customer:** How do I return an item?
**AI Chatbot:** You can return your item within 30 days of delivery. Visit your order history, select the item, and click “Return Item” to generate a return label.

---
