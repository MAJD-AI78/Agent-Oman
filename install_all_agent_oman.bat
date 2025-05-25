@echo off
echo 🔧 Setting up Agent-Oman environment...

:: Activate virtual environment
call venv\Scripts\activate

echo 📦 Installing core dependencies...
pip install --upgrade pip
pip install langchain-core langchain-community langchain-openai

echo 📄 Installing document loaders & OCR support...
pip install unstructured python-docx python-pptx openpyxl pytesseract pypdf pdfplumber

echo 🧠 Embeddings & vector store...
pip install faiss-cpu

echo 🌐 Web scraping & HTML parsing...
pip install beautifulsoup4 playwright

echo 📊 Charts, dashboards & export...
pip install matplotlib seaborn pandas plotly reportlab

echo 🎙️ Voice input & audio...
pip install sounddevice SpeechRecognition

echo 🧪 Other essentials...
pip install streamlit python-dotenv tiktoken

echo ✅ Setup complete. You can now run:  streamlit run streamlit_app.py
pause