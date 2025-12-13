from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    # Paths
    PDF_PATH: str = os.getenv("PDF_PATH", "bylaws.pdf")
    CHROMA_DIR: str = os.getenv("CHROMA_DIR", "chroma_db")
    COLLECTION: str = os.getenv("COLLECTION", "engineering_regs")

    # Chunking
    CHUNK_CHARS: int = int(os.getenv("CHUNK_CHARS", "1200"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))

    # Retrieval
    TOP_K: int = int(os.getenv("TOP_K", "6"))

    # Embeddings
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "intfloat/multilingual-e5-base")

    # LLM (Groq)
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
