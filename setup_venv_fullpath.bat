@echo off
echo 🧪 Creating virtual environment...
python -m venv venv

echo 📦 Activating virtual environment...
call venv\Scripts\activate

echo 🚀 Installing requirements from full path...
python -m pip install --upgrade pip
pip install --no-cache-dir -r C:\personal_bots\Agent-Oman\requirements.txt

echo ✅ Environment setup complete.
pause