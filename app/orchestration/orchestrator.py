# agent_oman/app/orchestration/orchestrator.py

import os
from chat_engine import query_documents
from web_scraper import scrape_google
from langchain.chat_models import ChatOpenAI

fallback_model = "gpt-3.5-turbo"

# === Run Task via Orchestration ===
def run_orchestrated_task(query, persona, lang):
    try:
        if "search" in query.lower():
            return scrape_google(query)

        model = os.getenv("FINE_TUNED_MODEL", fallback_model)

        # Adjust the prompt based on language
        if lang == "ar":
            adjusted_query = f"الرجاء إعطائي استشارة مهنية لهذا المحتوى:\n\n{query}"
        else:
            adjusted_query = f"Please provide a professional strategic recommendation for the following:\n\n{query}"

        # Send to document query engine
        return query_documents(adjusted_query, persona)

    except Exception as e:
        return f"⚠️ Error occurred while routing task: {e}"
