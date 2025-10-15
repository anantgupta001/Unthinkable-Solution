# backend/app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .ingestion import docs, index, model
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Knowledge Base Search Engine",
    description="RAG-based document search with LLM synthesis",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

class QueryResponse(BaseModel):
    query: str
    answer: str
    sources: list
    num_docs_searched: int

def search_docs_vector(query: str, top_k: int = 3):
    """Search for relevant document chunks using vector similarity."""
    if not docs:
        logger.warning("No documents loaded in the system")
        return [], []
    
    try:
        q_emb = model.encode(query).astype("float32")
        D, I = index.search(np.array([q_emb]), top_k)
        
        results = []
        sources = []
        
        for idx, distance in zip(I[0], D[0]):
            if idx < len(docs):
                doc = docs[idx]
                results.append(doc["text"])
                source_info = {
                    "file": doc.get("source", "unknown"),
                    "chunk": doc.get("chunk_id", 0),
                    "similarity": float(1 / (1 + distance))  # Convert distance to similarity
                }
                sources.append(source_info)
        
        return results, sources
    
    except Exception as e:
        logger.error(f"Error during search: {e}")
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

def synthesize_answer(query: str, context_chunks: list) -> str:
    """
    Synthesize an answer from retrieved chunks.
    For now, uses a simple approach. Can be enhanced with actual LLM.
    """
    if not context_chunks:
        return "I couldn't find relevant information to answer your question."
    
    # Simple synthesis: return formatted context
    # TODO: Integrate with actual LLM for better synthesis
    context = "\n\n---\n\n".join(context_chunks)
    
    # For now, return context with a note
    # In production, this would call the LLM from llm.py
    answer = f"Based on the available documents:\n\n{context}"
    
    return answer

@app.get("/")
def home():
    """Health check endpoint."""
    return {
        "message": "Knowledge Base Search Engine API",
        "status": "running",
        "docs_loaded": len(docs),
        "endpoints": {
            "search": "/search (POST)",
            "query": "/query/ (GET)"
        }
    }

@app.get("/query/")
def query_get(query: str, top_k: int = 3):
    """GET endpoint for compatibility."""
    if not query or not query.strip():
        raise HTTPException(status_code=400, detail="Query parameter is required")
    
    logger.info(f"Received GET query: {query}")
    
    try:
        chunks, sources = search_docs_vector(query, top_k)
        answer = synthesize_answer(query, chunks)
        
        return {
            "query": query,
            "answer": answer,
            "sources": sources,
            "num_docs_searched": len(docs)
        }
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
def search_post(request: QueryRequest):
    """POST endpoint for search (matches frontend)."""
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query is required")
    
    logger.info(f"Received POST query: {request.query}")
    
    try:
        chunks, sources = search_docs_vector(request.query, request.top_k)
        answer = synthesize_answer(request.query, chunks)
        
        return {
            "query": request.query,
            "answer": answer,
            "sources": sources,
            "num_docs_searched": len(docs)
        }
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
def get_stats():
    """Get system statistics."""
    return {
        "total_documents": len(docs),
        "index_size": index.ntotal if hasattr(index, 'ntotal') else 0,
        "embedding_dimension": 384,
        "model": "all-MiniLM-L6-v2"
    }
