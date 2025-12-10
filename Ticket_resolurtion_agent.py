## 🛠️ **Agent #51: Automated Ticket Resolution Agent**

### 📝 Overview

This agent automatically resolves common IT support tickets using predefined knowledge base (KB) answers 
and LLM-based reasoning. It classifies ticket type, finds relevant KB entries or uses GPT to draft a response, and
logs the solution. In this lab, you'll simulate ticket intake, use GPT for solution generation, and output a resolution log.

---

### 🧪 Lab Objectives

By the end of this lab, you will:

* Input or simulate incoming IT support tickets
* Classify the issue type (e.g., password reset, network error)
* Retrieve or generate automated responses using GPT
* Visualize the resolution and response log in a dashboard

---

### 🧰 Tech Stack

* **Python**
* **Streamlit**
* **LangChain + GPT-4 or GPT-3.5**
* **(Optional)** SQLite for ticket logging

---

### 🧭 Step-by-Step Instructions

#### ✅ Step 1: Environment Setup

```bash
mkdir ticket_resolution_agent
cd ticket_resolution_agent
python -m venv venv
source venv/bin/activate
pip install streamlit openai langchain pandas
```

---

#### ✅ Step 2: Sample Ticket Generator (`tickets.py`)

```python
import pandas as pd
import random

def sample_tickets():
    return pd.DataFrame([
        {"Ticket ID": "TCK001", "Subject": "Can't connect to VPN", "Description": "VPN gives timeout when working from home."},
        {"Ticket ID": "TCK002", "Subject": "Forgot my password", "Description": "Need help resetting my company email password."},
        {"Ticket ID": "TCK003", "Subject": "Laptop running slow", "Description": "My device takes 10 minutes to boot."},
        {"Ticket ID": "TCK004", "Subject": "Software installation", "Description": "Need Adobe Acrobat Pro installed for team use."},
        {"Ticket ID": "TCK005", "Subject": "Printer offline", "Description": "Office printer won't connect, showing offline."}
    ])
```

---

#### ✅ Step 3: GPT Prompt for Ticket Resolution (`ticket_prompt.py`)

```python
from langchain.prompts import PromptTemplate

ticket_prompt = PromptTemplate.from_template("""
You are an IT support agent.

Resolve this ticket:
Subject: {subject}
Description: {description}

Steps:
1. Identify the issue type
2. Provide a clear resolution
3. Suggest any follow-up actions

Respond in professional IT support tone.
""")
```

---

#### ✅ Step 4: GPT Resolution Engine (`resolution_agent.py`)

```python
from ticket_prompt import ticket_prompt
from langchain.chat_models import ChatOpenAI

def resolve_ticket(subject, description):
    llm = ChatOpenAI(temperature=0.3)
    prompt = ticket_prompt.format(subject=subject, description=description)
    return llm.predict(prompt)
```

---

#### ✅ Step 5: Streamlit Dashboard (`app.py`)

```python
import streamlit as st
from tickets import sample_tickets
from resolution_agent import resolve_ticket

st.title("🛠️ Automated Ticket Resolution Agent")

df = sample_tickets()
ticket_list = df["Ticket ID"].tolist()
selected = st.selectbox("Select a Ticket", ticket_list)
ticket = df[df["Ticket ID"] == selected].iloc[0]

if st.button("Resolve Ticket"):
    resolution = resolve_ticket(ticket["Subject"], ticket["Description"])
    st.subheader("📋 Ticket Details")
    st.write(ticket["Description"])

    st.subheader("✅ Suggested Resolution")
    st.text_area("GPT Response", resolution, height=300)
    st.download_button("Download Resolution", resolution, file_name=f"{ticket['Ticket ID']}_resolution.txt")
```

Run the app:

```bash
streamlit run app.py
```

---

### 🧪 Example Output (for "VPN timeout"):

**Issue Type:** Connectivity Issue – VPN
**Resolution:**

1. Instruct the user to restart their router and try reconnecting.
2. Ensure VPN client is updated to the latest version.
3. If error persists, escalate to Network Admin with logs.
   **Follow-Up:** Ask user to confirm when fixed.

---
