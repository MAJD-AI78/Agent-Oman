import os
import pytesseract
import pandas as pd
from PIL import Image
from pptx import Presentation
from langchain.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import Document


# Optional: explicitly set path to Tesseract if not in system PATH
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def load_pdf(path):
    loader = PyPDFLoader(path)
    return loader.load()

def load_docx(path):
    loader = UnstructuredWordDocumentLoader(path)
    return loader.load()

def load_excel(path):
    df = pd.read_excel(path, sheet_name=None)
    content = ""
    for sheet_name, sheet in df.items():
        content += f"Sheet: {sheet_name}\n\n"
        content += sheet.astype(str).to_string(index=False)
        content += "\n\n"
    return [Document(page_content=content, metadata={"source": path})]

def load_pptx(path):
    prs = Presentation(path)
    content = ""
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                content += shape.text + "\n"
    return [Document(page_content=content, metadata={"source": path})]

def load_image(path):
    text = pytesseract.image_to_string(Image.open(path))
    return [Document(page_content=text, metadata={"source": path})]

def load_documents(doc_dir="documents"):
    all_docs = []
    for file in os.listdir(doc_dir):
        path = os.path.join(doc_dir, file)
        ext = file.lower().split(".")[-1]

        if ext == "pdf":
            all_docs.extend(load_pdf(path))
        elif ext == "docx":
            all_docs.extend(load_docx(path))
        elif ext in ["xlsx", "xls"]:
            all_docs.extend(load_excel(path))
        elif ext == "pptx":
            all_docs.extend(load_pptx(path))
        elif ext in ["png", "jpg", "jpeg"]:
            all_docs.extend(load_image(path))
        else:
            print(f"Skipping unsupported file type: {file}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(all_docs)

    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local("vectorstore")
    print(f"Loaded and indexed {len(chunks)} chunks.")

