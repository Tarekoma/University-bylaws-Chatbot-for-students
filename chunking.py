from __future__ import annotations

import re

_ARABIC_INDIC_MAP = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")

def _to_latin_digits(s: str) -> str:
    return (s or "").translate(_ARABIC_INDIC_MAP)

from dataclasses import dataclass
from typing import List, Optional, Dict

@dataclass
class Chunk:
    id: str
    text: str
    page_start: int
    page_end: int
    article: Optional[str] = None
    title: Optional[str] = None

_ARTICLE_RE = re.compile(r"(?:^|\n)\s*(مادة\s*[\(\)]*\s*([0-9٠-٩]+)\s*[\(\)]*)(?:\s*[:：\-–])?", re.MULTILINE)

def split_by_articles(full_text: str) -> List[Dict[str, str]]:
    """Split into sections starting with 'مادة (X)' if present."""
    matches = list(_ARTICLE_RE.finditer(full_text))
    if not matches:
        return [{"header": None, "article": None, "body": full_text}]

    sections = []
    for idx, m in enumerate(matches):
        start = m.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(full_text)
        header = m.group(1).strip()
        art_no = _to_latin_digits(m.group(2).strip()) if m.group(2) else None
        body = full_text[start:end].strip()
        sections.append({"header": header, "article": art_no, "body": body})
    return sections

def chunk_text(text: str, chunk_chars: int = 1200, overlap: int = 200) -> List[str]:
    text = text.strip()
    if len(text) <= chunk_chars:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_chars)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = max(0, end - overlap)
    return chunks

def build_chunks(pages_text: List[tuple[int, str]], chunk_chars: int, overlap: int) -> List[Chunk]:
    """pages_text: list of (page_number, page_text)."""
    # Build a single combined text with page markers to keep page ranges
    # We'll keep mapping by assigning each page its own article split, then chunk.
    all_chunks: List[Chunk] = []
    chunk_i = 0

    for page, page_text in pages_text:
        if not page_text.strip():
            continue

        sections = split_by_articles(page_text)
        for sec in sections:
            body = sec["body"]
            art = sec["article"]
            header = sec["header"]

            for part in chunk_text(body, chunk_chars=chunk_chars, overlap=overlap):
                chunk_i += 1
                all_chunks.append(
                    Chunk(
                        id=f"chunk_{chunk_i:05d}",
                        text=part,
                        page_start=page,
                        page_end=page,
                        article=art,
                        title=header,
                    )
                )

    return all_chunks
