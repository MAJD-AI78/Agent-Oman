#!/bin/bash
pip install pyinstaller
pyinstaller --onefile --noconsole -n agent_oman_launcher app/main.py
