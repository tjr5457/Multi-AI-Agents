
## 🛡️ **Agent #52: Security Threat Detection Agent**

### 📝 Overview

This agent monitors system logs, API access patterns, or network traffic to detect suspicious behavior. It uses AI to flag anomalies like brute-force login attempts, abnormal API calls, or data exfiltration patterns. In this project, you’ll simulate log entries, apply simple detection rules, and use GPT to classify and summarize threats.

---

### 🧪  Objectives

By the end of this project, you will:

* Simulate security logs with various activities
* Apply basic anomaly detection logic
* Use GPT to label suspicious behaviors and suggest actions
* Generate an incident summary report

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
mkdir security_threat_agent
cd security_threat_agent
python -m venv venv
source venv/bin/activate
pip install streamlit openai langchain pandas
```

---

#### ✅ Step 2: Simulated Security Logs (`logs.py`)

```python
import pandas as pd
import random
from datetime import datetime, timedelta

def generate_logs():
    events = [
        "Login Success", "Login Failed", "File Access", "API Call", 
        "Privilege Escalation", "Port Scan", "Database Query", 
        "Multiple Login Failures", "Unusual File Download"
    ]
    ips = ["192.168.1.1", "10.0.0.2", "172.16.0.5", "192.168.1.45"]
    data = []

    for _ in range(50):
        timestamp = datetime.now() - timedelta(minutes=random.randint(0, 720))
        event = random.choice(events)
        ip = random.choice(ips)
        user = random.choice(["alice", "bob", "charlie", "admin"])
        data.append({
            "timestamp": timestamp,
            "user": user,
            "ip": ip,
            "event": event
        })

    return pd.DataFrame(data)
```

---

#### ✅ Step 3: GPT Prompt for Threat Summary (`threat_prompt.py`)

```python
from langchain.prompts import PromptTemplate

threat_prompt = PromptTemplate.from_template("""
You are a cybersecurity analyst.

Given the following suspicious events:
{events}

1. Identify the type of threat(s)
2. Suggest actions to mitigate or escalate
3. Summarize key users or IPs involved

Be concise and structured like an incident response memo.
""")
```

---

#### ✅ Step 4: GPT Detection Engine (`threat_agent.py`)

```python
from langchain.chat_models import ChatOpenAI
from threat_prompt import threat_prompt

def generate_threat_summary(events: str):
    llm = ChatOpenAI(temperature=0.3)
    prompt = threat_prompt.format(events=events)
    return llm.predict(prompt)
```

---

#### ✅ Step 5: Streamlit Interface (`app.py`)

```python
import streamlit as st
from logs import generate_logs
from threat_agent import generate_threat_summary

st.title("🛡️ Security Threat Detection Agent")

df = generate_logs()
st.subheader("🔍 Simulated Logs")
st.dataframe(df)

suspicious_events = df[df['event'].isin([
    "Login Failed", "Multiple Login Failures", 
    "Privilege Escalation", "Port Scan", 
    "Unusual File Download"
])]

if st.button("Analyze Threats"):
    event_str = suspicious_events.to_string(index=False)
    summary = generate_threat_summary(event_str)

    st.subheader("⚠️ GPT Threat Summary")
    st.text_area("Incident Report", summary, height=400)
    st.download_button("Download Report", summary, file_name="threat_report.txt")
```

Run the app:

```bash
streamlit run app.py
```

---

### 🧪 Example Output:

**Incident Report**
**Threats Detected:**

* Multiple login failures and port scanning suggest a brute-force attack
* Privilege escalation and unusual file downloads indicate a possible insider threat

**Key Entities:**

* User: `admin`, `bob`
* IPs: `192.168.1.45`, `10.0.0.2`

**Suggested Actions:**

* Temporarily disable affected accounts
* Block suspicious IPs via firewall
* Initiate forensic review of file access logs

---
