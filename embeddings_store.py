from __future__ import annotations

from typing import List, Dict, Any

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

def load_embedder(model_name: str) -> SentenceTransformer:
    return SentenceTransformer(model_name)

def e5_embed_passages(embedder: SentenceTransformer, texts: List[str]) -> List[List[float]]:
    # E5 expects prefix for best performance
    inputs = [f"passage: {t}" for t in texts]
    vecs = embedder.encode(inputs, normalize_embeddings=True, show_progress_bar=False)
    return vecs.tolist()

def e5_embed_query(embedder: SentenceTransformer, query: str) -> List[float]:
    vec = embedder.encode([f"query: {query}"], normalize_embeddings=True, show_progress_bar=False)[0]
    return vec.tolist()

def get_chroma_client(persist_dir: str) -> chromadb.PersistentClient:
    return chromadb.PersistentClient(path=persist_dir, settings=Settings(anonymized_telemetry=False))

def get_or_create_collection(client: chromadb.PersistentClient, name: str):
    return client.get_or_create_collection(name=name, metadata={"hnsw:space": "cosine"})
