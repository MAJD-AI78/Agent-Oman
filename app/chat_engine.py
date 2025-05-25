import os
import requests
from bs4 import BeautifulSoup
from langchain.schema import SystemMessage, HumanMessage
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from dotenv import load_dotenv

load_dotenv()

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# 📌 Define all system prompts for personas
PROMPTS = {
    "Strategic Consultant": SystemMessage(content="""
You are Agent-Oman, a highly strategic AI consultant trained in McKinsey, Bain, and BCG frameworks.
You specialize in delivering structured insights, strategic recommendations, and analytical breakdowns
using tools such as SWOT, BCG Matrix, Porter's Five Forces, and OKRs. Your responses must follow this format:

1. **Insight Summary**
2. **Strategic Analysis**
3. **Recommendation**
4. **📎 Sources Cited (if applicable)**

Use a formal tone. Be precise. Prioritize clarity, value, and executive usefulness.
"""),
    "Investor Analyst": SystemMessage(content="""
You are Agent-Oman, a financial and investment analyst. Provide valuations, ratio analysis, market risk assessments,
and strategic forecasts. Use concise, investor-friendly language with data references.
"""),
    "Startup Mentor": SystemMessage(content="""
You are Agent-Oman, a startup coach and incubator strategist. You advise founders on lean startup models, 
go-to-market, funding strategies, and growth hacking. Keep language energetic but structured.
"""),
    "Corporate Lawyer": SystemMessage(content="""
You are Agent-Oman, a corporate legal advisor. Answer with regulatory context, risk frameworks, and jurisdictional precision.
Avoid giving legal advice, but cite relevant laws and implications when applicable.
"""),
    "Economic Policy Advisor": SystemMessage(content="""
You are Agent-Oman, an economic policy strategist working with governments and international bodies.
Focus on macroeconomic trends, trade policy, fiscal reforms, and international competitiveness.
""")
}

def scrape_google(query):
    try:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")
        snippets = soup.select(".BNeawe.s3v9rd.AP7Wnd")
        return "\n".join([s.text for s in snippets[:5]])
    except Exception as e:
        return f"Google scraping failed: {e}"

def scrape_duckduckgo(query):
    try:
        url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")
        results = soup.select(".result__snippet")
        return "\n".join([r.text.strip() for r in results[:5]])
    except Exception as e:
        return f"DuckDuckGo fallback failed: {e}"

def format_consulting_response(answer, sources):
    md = "### 🧠 Strategic Recommendation\n\n"
    md += f"{answer}\n\n"
    if sources:
        md += "---\n\n**📎 Sources Cited:**\n"
        for i, src in enumerate(sources, 1):
            md += f"{i}. [{src['title']}]({src['url']})\n"
    return md

def query_documents(query, persona="Strategic Consultant"):
    embeddings = OpenAIEmbeddings()
    db = FAISS.load_local("vectorstore", embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever()

    # 🧠 Use the selected persona's system prompt
    system_prompt = PROMPTS.get(persona, PROMPTS["Strategic Consultant"])
    llm = ChatOpenAI(model="gpt-4", temperature=0.2)

    def format_query(q):
        return [system_prompt, HumanMessage(content=q)]

    tools = [
        Tool(name="Local Docs", func=lambda q: RetrievalQA.from_chain_type(llm=llm, retriever=retriever).run(q),
             description="Searches local business documents."),
        Tool(name="Web Scraper", func=lambda q: scrape_google(q), description="Google snippet search."),
        Tool(name="DuckDuckGo Fallback", func=lambda q: scrape_duckduckgo(q), description="Backup web search engine.")
    ]

    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False
    )

    raw = agent.run(format_query(query))

    sources = [{"title": "Google Search Result", "url": f"https://www.google.com/search?q={query.replace(' ', '+')}"}]
    return format_consulting_response(raw, sources)


