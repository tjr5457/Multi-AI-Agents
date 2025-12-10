import streamlit as st
import pandas as pd
import os
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI # Updated import for newer LangChain versions

# --- 1. SETUP PAGE CONFIG ---
st.set_page_config(page_title="Agent #51: Ticket Resolver", page_icon="🛠️")

st.title("🛠️ Agent #51: Automated Ticket Resolution")
st.markdown("Select a ticket below to generate an AI-powered solution.")

# --- 2. SIDEBAR: API KEY ---
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

if not api_key:
    st.warning("⚠️ Please enter your OpenAI API Key in the sidebar to proceed.")
    st.stop()

# Set the key for LangChain
os.environ["OPENAI_API_KEY"] = api_key

# --- 3. DATA: SAMPLE TICKETS ---
def sample_tickets():
    return pd.DataFrame([
        {"Ticket ID": "TCK001", "Subject": "Can't connect to VPN", "Description": "VPN gives timeout when working from home."},
        {"Ticket ID": "TCK002", "Subject": "Forgot my password", "Description": "Need help resetting my company email password."},
        {"Ticket ID": "TCK003", "Subject": "Laptop running slow", "Description": "My device takes 10 minutes to boot."},
        {"Ticket ID": "TCK004", "Subject": "Software installation", "Description": "Need Adobe Acrobat Pro installed for team use."},
        {"Ticket ID": "TCK005", "Subject": "Printer offline", "Description": "Office printer won't connect, showing offline."}
    ])

# --- 4. AI ENGINE: PROMPT & RESOLVER ---
ticket_prompt = PromptTemplate.from_template("""
You are an IT support agent.

Resolve this ticket:
Subject: {subject}
Description: {description}

Steps:
1. Identify the issue type
2. Provide a clear resolution (numbered list)
3. Suggest any follow-up actions

Respond in a professional, empathetic IT support tone.
""")

def resolve_ticket(subject, description):
    # We use ChatOpenAI. Ideally use gpt-3.5-turbo or gpt-4
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3)
    
    # Create the chain (New LangChain syntax uses | pipe, but this old style works too)
    formatted_prompt = ticket_prompt.format(subject=subject, description=description)
    response = llm.invoke(formatted_prompt)
    return response.content

# --- 5. UI: MAIN APP ---
df = sample_tickets()
ticket_list = df["Ticket ID"].tolist()

# Layout: Two columns
col1, col2 = st.columns([1, 2])

with col1:
    selected_id = st.selectbox("Select a Ticket", ticket_list)
    # Filter data to get the selected ticket details
    ticket = df[df["Ticket ID"] == selected_id].iloc[0]
    
    st.info(f"**Subject:** {ticket['Subject']}")
    st.caption(f"**Description:** {ticket['Description']}")

with col2:
    if st.button("Resolve Ticket 🚀"):
        with st.spinner("AI Agent is analyzing the issue..."):
            try:
                resolution = resolve_ticket(ticket["Subject"], ticket["Description"])
                
                st.subheader("✅ Suggested Resolution")
                st.markdown(resolution) # markdown renders lists/bolding better than text_area
                
                st.download_button(
                    "Download Resolution", 
                    resolution, 
                    file_name=f"{ticket['Ticket ID']}_resolution.txt"
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")