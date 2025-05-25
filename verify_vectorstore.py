
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings

def verify_vectorstore():
    try:
        print("🔍 Loading vectorstore...")
        embeddings = OpenAIEmbeddings()
        db = FAISS.load_local("vectorstore", embeddings, allow_dangerous_deserialization=True)
        docs = list(db.docstore._dict.values())

        print(f"✅ Loaded {len(docs)} documents from vectorstore.")

        for i, doc in enumerate(docs[:5]):  # Show preview of first 5 docs
            print(f"\n--- Document {i+1} ---")
            print(f"📄 Source: {doc.metadata.get('source')}")
            print(f"📝 Content Preview: {doc.page_content[:300]}...")

    except Exception as e:
        print(f"❌ Error verifying vectorstore: {e}")

if __name__ == "__main__":
    verify_vectorstore()
