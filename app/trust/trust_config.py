# agent_oman/app/trust/trust_config.py

trust_center_config = {
    "Strategic Consultant": {
        "Model": "GPT-4 (consulting-tuned)",
        "Sources": "Strategic memos, economic forecasts",
        "Privacy": "Data is processed locally; no cloud sync"
    },
    "Investor Analyst": {
        "Model": "GPT-4 (financial mode)",
        "Sources": "Annual reports, IMF datasets",
        "Privacy": "Encrypted input; session-based memory only"
    },
    "Startup Mentor": {
        "Model": "GPT-3.5 (startup fine-tuned)",
        "Sources": "YC decks, product strategies",
        "Privacy": "No tracking or external logging"
    },
    "Corporate Lawyer": {
        "Model": "Majd-ASI Legal LLM",
        "Sources": "Oman Commercial Code, OECD reports",
        "Privacy": "Jurisdictional logic applied"
    },
    "Economic Policy Advisor": {
        "Model": "GPT-4 (macro mode)",
        "Sources": "World Bank, Trade Reports, Vision 2040",
        "Privacy": "Insights generated on-device"
    }
}