import os
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from app.web_scraper import scrape_google, scrape_full_page

def run_orchestrated_task(query, persona, lang="en"):
    embeddings = OpenAIEmbeddings()
    db = FAISS.load_local("vectorstore", embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever()
    llm = ChatOpenAI(model="gpt-4", temperature=0.2)

    system_prompt = f"You are Agent-Oman, a {persona}. Reply in {'Arabic' if lang == 'ar' else 'English'} with strategic clarity."

    tools = [
        Tool(name="📄 LocalDocs", func=lambda q: RetrievalQA.from_chain_type(llm=llm, retriever=retriever).run(q),
             description="Search in uploaded knowledge base"),
        Tool(name="🌐 GoogleSearch", func=lambda q: scrape_google(q), description="Search recent web data"),
        Tool(name="🕵️ FullPageScraper", func=lambda q: scrape_full_page(q), description="Scrape page content by URL")
    ]

    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False)
    return agent.run(query)
