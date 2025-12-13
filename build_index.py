from __future__ import annotations

import os
from typing import List

from config import Config
from pdf_extract import extract_pdf_pages, enrich_pages_with_tables_and_ocr
from chunking import build_chunks
from embeddings_store import (
    load_embedder,
    e5_embed_passages,
    get_chroma_client,
    get_or_create_collection,
)

def main() -> None:
    cfg = Config()

    if not os.path.exists(cfg.PDF_PATH):
        raise FileNotFoundError(
            f"PDF not found: {cfg.PDF_PATH}\n"
            f"Put your PDF in the project folder and name it 'bylaws.pdf' (or change PDF_PATH in .env)."
        )

    print(f"[1/5] Reading PDF: {cfg.PDF_PATH}")
    pages = extract_pdf_pages(cfg.PDF_PATH)

    print("[2/5] Optional: tables/OCR enrichment (safe to ignore if not installed)")
    pages = enrich_pages_with_tables_and_ocr(cfg.PDF_PATH, pages)

    # Merge page text + optional table text
    pages_text: List[tuple[int, str]] = []
    for p in pages:
        combined = p.text
        if p.tables_text.strip():
            combined += "\n\n[TABLES]\n" + p.tables_text
        pages_text.append((p.page, combined))

    print("[3/5] Chunking")
    chunks = build_chunks(pages_text, chunk_chars=cfg.CHUNK_CHARS, overlap=cfg.CHUNK_OVERLAP)
    print(f"  -> chunks: {len(chunks)}")

    print("[4/5] Embedding")
    embedder = load_embedder(cfg.EMBEDDING_MODEL)
    texts = [c.text for c in chunks]
    vectors = e5_embed_passages(embedder, texts)

    print("[5/5] Saving to Chroma")
    client = get_chroma_client(cfg.CHROMA_DIR)
    col = get_or_create_collection(client, cfg.COLLECTION)

    # Clear collection (rebuild)
    try:
        col.delete(where={})
    except Exception:
        pass

    ids = [c.id for c in chunks]
    metadatas = [
        {
            "page_start": c.page_start,
            "page_end": c.page_end,
            "article": c.article or "",
            "title": c.title or "",
        }
        for c in chunks
    ]

    col.add(ids=ids, embeddings=vectors, documents=texts, metadatas=metadatas)

    print("✅ Index built successfully.")
    print(f"Chroma directory: {cfg.CHROMA_DIR}")
    print(f"Collection: {cfg.COLLECTION}")

if __name__ == "__main__":
    main()
