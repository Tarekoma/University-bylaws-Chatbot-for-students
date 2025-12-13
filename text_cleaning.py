from __future__ import annotations

import re
import unicodedata

_ARABIC_DIACRITICS = re.compile(r"[\u064B-\u065F\u0670\u06D6-\u06ED]")

def normalize_nfkc(text: str) -> str:
    # Converts Arabic presentation forms -> normal Arabic letters (very important for PDFs like yours)
    return unicodedata.normalize("NFKC", text)

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = normalize_nfkc(text)

    # Normalize whitespace
    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove stray spaces around punctuation
    text = re.sub(r"\s+([،؛:!?.])", r"\1", text)
    text = re.sub(r"([،؛:!?.])\s+", r"\1 ", text)

    # Optional: remove Arabic diacritics (usually not in regulations PDFs)
    # text = _ARABIC_DIACRITICS.sub("", text)

    return text.strip()

def is_probably_scanned(page_text: str, min_chars: int = 50) -> bool:
    # If a page has very little extractable text, it may be scanned (image-only)
    return len(page_text.strip()) < min_chars

def detect_table_like(page_text: str) -> bool:
    # Heuristic: tables often have many numbers / repeated spacing / "جدول"
    if "جدول" in page_text:
        return True
    digits = sum(ch.isdigit() for ch in page_text)
    if digits > 60 and ("|" in page_text or "  " in page_text):
        return True
    return False
