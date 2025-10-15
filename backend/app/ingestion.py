# backend/app/ingestion.py
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
import re

folder_path = os.path.join(os.path.dirname(__file__), "docs")

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_text(text, chunk_size=500, overlap=100):
    """Split text into overlapping chunks for better retrieval."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    return chunks

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file."""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        print(f"[Error] Failed to read PDF {pdf_path}: {e}")
        return ""

def load_documents():
    """Load and process documents from the docs folder."""
    docs = []
    if not os.path.exists(folder_path):
        print(f"[Warning] Folder {folder_path} not found. Returning empty docs.")
        return docs
    
    print(f"[Info] Loading documents from {folder_path}...")
    
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        # Skip directories
        if os.path.isdir(file_path):
            continue
        
        text = ""
        
        # Handle .txt files
        if file_name.endswith(".txt"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
                print(f"[Info] Loaded text file: {file_name}")
            except Exception as e:
                print(f"[Error] Failed to read {file_name}: {e}")
                continue
        
        # Handle .pdf files
        elif file_name.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
            if text:
                print(f"[Info] Loaded PDF file: {file_name}")
            else:
                print(f"[Warning] No text extracted from {file_name}")
                continue
        
        else:
            print(f"[Info] Skipping unsupported file: {file_name}")
            continue
        
        # Chunk the text
        if text.strip():
            chunks = chunk_text(text, chunk_size=500, overlap=100)
            
            # Create embeddings for each chunk
            for i, chunk in enumerate(chunks):
                try:
                    emb = model.encode(chunk).astype("float32")
                    docs.append({
                        "text": chunk,
                        "embedding": emb,
                        "source": file_name,
                        "chunk_id": i
                    })
                except Exception as e:
                    print(f"[Error] Failed to embed chunk from {file_name}: {e}")
            
            print(f"[Info] Created {len(chunks)} chunks from {file_name}")
    
    print(f"[Info] Total documents loaded: {len(docs)}")
    return docs

# Load documents at startup
docs = load_documents()

# Create or load FAISS index
embedding_dim = 384  # for MiniLM-L6-v2
if docs:
    index = faiss.IndexFlatL2(embedding_dim)
    embeddings = np.array([doc["embedding"] for doc in docs])
    index.add(embeddings)
    print(f"[Info] FAISS index created with {len(docs)} vectors")
else:
    index = faiss.IndexFlatL2(embedding_dim)
    print("[Warning] No documents loaded. Index is empty.")
