
## 🗂️ **Agent #53: IT Ticket Prioritization Agent**

### 📝 Overview

This agent reads incoming IT support tickets and automatically assigns a priority level (High, Medium, Low) based on urgency, impact, and keywords. It uses GPT to reason through the ticket content and outputs a structured priority log. In this poject, you’ll simulate ticket intake, analyze content, and use GPT to assign priorities.

---

### 🧪  Objectives

By the end of this project, you will:

* Simulate a set of incoming IT tickets
* Use GPT to classify priority (High / Medium / Low)
* Visualize and export a prioritized ticket queue
* Optionally assign escalation suggestions

---

### 🧰 Tech Stack

* **Python**
* **Streamlit**
* **LangChain + GPT-4 or GPT-3.5**
* **Pandas**

---

### 🧭 Step-by-Step Instructions

#### ✅ Step 1: Environment Setup

```bash
mkdir ticket_prioritization_agent
cd ticket_prioritization_agent
python -m venv venv
source venv/bin/activate
pip install streamlit openai langchain pandas
```

---

#### ✅ Step 2: Sample Ticket Generator (`tickets.py`)

```python
import pandas as pd

def get_tickets():
    return pd.DataFrame([
        {"Ticket ID": "IT001", "Subject": "Email not syncing", "Description": "My Outlook is not syncing emails since morning."},
        {"Ticket ID": "IT002", "Subject": "Laptop overheating", "Description": "Device heats up even when idle. Very hot to touch."},
        {"Ticket ID": "IT003", "Subject": "VPN not connecting", "Description": "Unable to connect to VPN from home."},
        {"Ticket ID": "IT004", "Subject": "Access request", "Description": "Need access to Jira and Confluence for my new project."},
        {"Ticket ID": "IT005", "Subject": "Data loss", "Description": "Files deleted from shared drive accidentally. Need recovery ASAP."}
    ])
```

---

#### ✅ Step 3: GPT Prompt for Priority Assignment (`priority_prompt.py`)

```python
from langchain.prompts import PromptTemplate

priority_prompt = PromptTemplate.from_template("""
You are an IT service desk manager.

Given the following ticket:
Subject: {subject}
Description: {description}

Assign a priority: High, Medium, or Low.

Rules:
- High = business-critical or data/security risks
- Medium = blocks daily work but has a workaround
- Low = access/setup requests or minor issues

Also provide a short explanation for the priority.
Format:
Priority: <priority>
Reason: <reason>
""")
```

---

#### ✅ Step 4: GPT-Based Classifier (`priority_agent.py`)

```python
from priority_prompt import priority_prompt
from langchain.chat_models import ChatOpenAI

def prioritize_ticket(subject, description):
    llm = ChatOpenAI(temperature=0.2)
    prompt = priority_prompt.format(subject=subject, description=description)
    return llm.predict(prompt)
```

---

#### ✅ Step 5: Streamlit App (`app.py`)

```python
import streamlit as st
from tickets import get_tickets
from priority_agent import prioritize_ticket

st.title("🗂️ IT Ticket Prioritization Agent")

tickets = get_tickets()
ticket_ids = tickets["Ticket ID"].tolist()
selected_id = st.selectbox("Select Ticket", ticket_ids)
selected_ticket = tickets[tickets["Ticket ID"] == selected_id].iloc[0]

if st.button("Assign Priority"):
    result = prioritize_ticket(
        selected_ticket["Subject"], 
        selected_ticket["Description"]
    )
    st.subheader("📋 Ticket Info")
    st.write(selected_ticket)

    st.subheader("🎯 Priority Assignment")
    st.text_area("GPT Output", result, height=200)
    st.download_button("Download Result", result, file_name=f"{selected_id}_priority.txt")
```

Run the app:

```bash
streamlit run app.py
```

---

### 🧪 Example Output

**Subject:** Data loss
**Description:** Files deleted from shared drive accidentally. Need recovery ASAP.

**GPT Output:**

```
Priority: High  
Reason: Involves data loss with potential business impact and urgency. Requires immediate recovery action.
```

---
