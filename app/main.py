# agent_oman/app/main.py

import os
import streamlit as st
from dotenv import load_dotenv
from langdetect import detect
from document_loader import load_documents
from chat_engine import query_documents
from export_pdf import export_to_pdf
from dashboard import render_dashboard
from voice_input import capture_voice
from orchestration.orchestrator import run_orchestrated_task
from trust.trust_config import trust_center_config

load_dotenv()
st.set_page_config(page_title="Agent-Oman AI", layout="wide", page_icon="🧠")
st.title("🧠 Agent-Oman - Strategic AI Assistant")

# === Language Detection & Toggle ===
if "user_lang" not in st.session_state:
    st.session_state.user_lang = "en"
lang = st.sidebar.radio("🌐 Language", ["English", "Arabic"], index=0 if st.session_state.user_lang == "en" else 1)
st.session_state.user_lang = "en" if lang == "English" else "ar"

# === Persona Selection ===
persona = st.sidebar.selectbox("🎭 Persona", [
    "Strategic Consultant", "Investor Analyst", "Startup Mentor", "Corporate Lawyer", "Economic Policy Advisor"\])

# === Upload Interface ===
uploaded_files = st.sidebar.file_uploader("📥 Upload Files", type=["pdf", "docx", "xlsx", "pptx", "png", "jpg"], accept_multiple_files=True)
if uploaded_files and st.sidebar.button("🧠 Build Knowledge Base"):
    with st.spinner("Indexing files..."):
        os.makedirs("documents", exist_ok=True)
        for file in uploaded_files:
            with open(os.path.join("documents", file.name), "wb") as f:
                f.write(file.read())
        load_documents()
    st.success("✅ Documents loaded successfully!")

# === Dashboard / Data Analysis ===
data_file = st.sidebar.file_uploader("📊 Upload Excel/CSV", type=["csv", "xlsx"])
if data_file:
    render_dashboard(data_file)

# === Voice Input ===
if st.sidebar.button("🎙 Voice Input"):
    st.session_state.voice_text = capture_voice()
    st.sidebar.write(f"🗣️ You said: {st.session_state.voice_text}")

# === Trust Center ===
if st.sidebar.button("🔐 Trust Center"):
    persona_info = trust_center_config.get(persona, {})
    st.markdown(f"### Trust Center – {persona}")
    for key, value in persona_info.items():
        st.markdown(f"**{key}:** {value}")

# === Chat History ===
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# === Chat Input ===
user_input = st.chat_input("Ask Agent-Oman…") or st.session_state.get("voice_text", "")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking..."):
            response = run_orchestrated_task(user_input, persona, st.session_state.user_lang)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if st.session_state.get("messages") and st.button("📄 Export as PDF"):
    export_to_pdf(st.session_state.messages[-1]["content"])
    st.success("✅ PDF exported as agent_oman_report.pdf")
