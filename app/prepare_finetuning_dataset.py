import os
import json
import time
from dotenv import load_dotenv
from collections import Counter
from openai import OpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings

# Load API key from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Track persona distribution
persona_counter = Counter()

def classify_persona_and_domain(text):
    text = text.lower()

    persona_domain_map = {
        "Investor Analyst": {
            "domain": "finance",
            "keywords": ["investment", "valuation", "equity", "return", "roi", "asset", "capital"]
        },
        "Strategic Consultant": {
            "domain": "strategy",
            "keywords": ["business model", "strategy", "swot", "competitive", "growth", "vision", "mission"]
        },
        "Corporate Lawyer": {
            "domain": "legal",
            "keywords": ["regulation", "legal", "compliance", "jurisdiction", "contract", "law"]
        },
        "Startup Mentor": {
            "domain": "startup",
            "keywords": ["startup", "incubator", "founder", "mvp", "seed", "pitch", "accelerator"]
        },
        "Economic Policy Advisor": {
            "domain": "policy",
            "keywords": ["gdp", "policy", "economy", "macroeconomic", "tax", "fiscal", "trade"]
        }
    }

    for persona, data in persona_domain_map.items():
        if any(keyword in text for keyword in data["keywords"]):
            persona_counter[persona] += 1
            return persona, data["domain"]

    persona_counter["Strategic Consultant"] += 1
    return "Strategic Consultant", "general"

def query_gpt(content, persona):
    system_prompt = f"You are Agent-Oman, a {persona} answering with expert clarity."
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"What does this mean or suggest?\n\n{content}"}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"⚠️ GPT Error: {e}")
        return "[Error generating summary.]"

def prepare_dataset(output_path="finetune_dataset.jsonl"):
    print("🔍 Loading vectorstore...")
    embeddings = OpenAIEmbeddings()
    db = FAISS.load_local("vectorstore", embeddings, allow_dangerous_deserialization=True)
    docs = db.docstore._dict.values()
    print(f"📄 {len(docs)} documents loaded.")

    # GPT test
    print("🧪 Testing GPT-4 response...")
    test = query_gpt("Summarize Oman Vision 2040.", "Strategic Consultant")
    print(f"✅ GPT-4 test successful: {test[:60]}...\n")

    os.makedirs("fine_tune_subsets", exist_ok=True)
    full_dataset = []
    chunk_count = 0

    for i, doc in enumerate(docs):
        content = doc.page_content.strip()
        if not content or len(content) < 50:
            continue

        chunk_count += 1
        persona, domain = classify_persona_and_domain(content)

        print(f"🔹 [{chunk_count}] Persona: {persona} | Domain: {domain}")
        assistant_reply = query_gpt(content, persona)

        qa_pair = {
            "messages": [
                {"role": "system", "content": f"You are a {persona}."},
                {"role": "user", "content": f"What does this content mean or suggest?\n\n{content}"},
                {"role": "assistant", "content": assistant_reply}
            ]
        }

        full_dataset.append(qa_pair)

        # Save domain subset
        with open(f"fine_tune_subsets/{domain}.jsonl", "a", encoding="utf-8") as df:
            df.write(json.dumps(qa_pair) + "\n")

        time.sleep(0.5)  # Optional: avoid rate limits

    if chunk_count == 0:
        print("⚠️ No valid content chunks found. Vectorstore might be empty.")
        return

    with open(output_path, "w", encoding="utf-8") as f:
        for item in full_dataset:
            f.write(json.dumps(item) + "\n")

    print(f"\n✅ Done! {chunk_count} samples saved to: {output_path}")
    print("📂 Domain subsets saved in: /fine_tune_subsets/")

    print("\n📊 Persona distribution:")
    for persona, count in persona_counter.items():
        print(f"   - {persona}: {count}")

if __name__ == "__main__":
    prepare_dataset()
