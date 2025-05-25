import streamlit as st
from PIL import Image
import os
from dotenv import load_dotenv
from langdetect import detect

from document_loader import load_documents
from chat_engine import query_documents
from export_pdf import export_to_pdf
from dashboard import render_dashboard
from voice_input import capture_voice
from orchestration.orchestrator import run_orchestrated_task
from trust.trust_config import trust_center_config

# === MUST BE FIRST ===
st.set_page_config(page_title="Agent-Oman", page_icon="logo.png", layout="centered")

# === Login Layer ===
def login():
    st.sidebar.title("🔐 Login")
    password = st.sidebar.text_input("Enter password", type="password")
    if password != "Majd2025":
        st.warning("🔒 Access Denied")
        st.stop()
    st.success("✅ Access granted")

login()

# === Translation Helper ===
def t(en, ar):
    return ar if st.session_state.get("user_lang") == "ar" else en

# === Branding ===
logo_path = os.path.join(os.path.dirname(__file__), "..", "logo.png")
if os.path.exists(logo_path):
    st.image(logo_path, width=180)

st.title(t("Agent-Oman", "العميل العماني"))
st.caption(t("Empowering Oman’s Strategic Intelligence", "تمكين الذكاء الاستراتيجي لعُمان"))

# === Config ===
load_dotenv()

# === Language Toggle ===
if "user_lang" not in st.session_state:
    st.session_state.user_lang = "en"
lang = st.sidebar.radio("🌐 Language", ["English", "Arabic"], index=0 if st.session_state.user_lang == "en" else 1)
st.session_state.user_lang = "en" if lang == "English" else "ar"

# === Persona ===
persona = st.sidebar.selectbox("🎭 Persona", [
    "Strategic Consultant", "Investor Analyst", "Startup Mentor", "Corporate Lawyer", "Economic Policy Advisor"])

# === File Upload ===
uploaded_files = st.sidebar.file_uploader("📥 Upload Files", type=["pdf", "docx", "xlsx", "pptx", "png", "jpg"], accept_multiple_files=True)
if uploaded_files and st.sidebar.button("🧠 Build Knowledge Base"):
    with st.spinner("Indexing files..."):
        os.makedirs("documents", exist_ok=True)
        for file in uploaded_files:
            with open(os.path.join("documents", file.name), "wb") as f:
                f.write(file.read())
        load_documents()
    st.success("✅ Documents loaded successfully!")

# === Dashboard Upload ===
data_file = st.sidebar.file_uploader("📊 Upload Excel/CSV", type=["csv", "xlsx"])
if data_file:
    render_dashboard(data_file)

# === Voice Input ===
if st.sidebar.button("🎙 Voice Input"):
    st.session_state.voice_text = capture_voice()
    st.sidebar.write(f"🗣️ {t('You said', 'قلت')}: {st.session_state.voice_text}")

# === Trust Center ===
if st.sidebar.button("🔐 Trust Center"):
    persona_info = trust_center_config.get(persona, {})
    st.markdown(f"### {t('Trust Center', 'مركز الثقة')} – {persona}")
    for key, value in persona_info.items():
        st.markdown(f"**{t(key, key)}:** {t(value, value)}")

# === Chat Memory ===
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# === Streamlit Chat Input ===
user_input = st.chat_input(t("Ask Agent-Oman…", "اسأل العميل العماني…")) or st.session_state.get("voice_text", "")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking..."):
            response = run_orchestrated_task(user_input, persona, st.session_state.user_lang)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# === Export Button ===
if st.session_state.get("messages") and st.button("📄 Export as PDF"):
    export_to_pdf(st.session_state.messages[-1]["content"])
    st.success("✅ PDF exported as agent_oman_report.pdf")