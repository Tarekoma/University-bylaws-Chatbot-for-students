from __future__ import annotations

from typing import List, Dict, Any

from config import Config
from embeddings_store import (
    load_embedder,
    e5_embed_query,
    get_chroma_client,
    get_or_create_collection,
)

def retrieve(query: str, cfg: Config) -> List[Dict[str, Any]]:
    embedder = load_embedder(cfg.EMBEDDING_MODEL)
    qvec = e5_embed_query(embedder, query)

    client = get_chroma_client(cfg.CHROMA_DIR)
    col = get_or_create_collection(client, cfg.COLLECTION)
    res = col.query(
        query_embeddings=[qvec],
        n_results=cfg.TOP_K,
        include=["documents", "metadatas", "distances"],  # ✅ removed "ids"
    )

    ids = res.get("ids", [[]])[0]
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dists = res.get("distances", [[]])[0] if "distances" in res else [None] * len(ids)

    hits = []
    for i in range(len(ids)):
        hits.append(
            {
                "id": ids[i],
                "text": docs[i],
                "meta": metas[i],
                "distance": dists[i],
            }
        )

    return hits
