from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Dict, Any

import fitz  # PyMuPDF

from text_cleaning import clean_text, is_probably_scanned, detect_table_like

@dataclass
class PageContent:
    page: int
    text: str
    tables_text: str = ""
    used_ocr: bool = False
    used_table_extractor: str = ""

def extract_pdf_pages(pdf_path: str) -> List[PageContent]:
    doc = fitz.open(pdf_path)
    pages: List[PageContent] = []

    for i in range(len(doc)):
        raw = doc[i].get_text("text") or ""
        text = clean_text(raw)

        pages.append(PageContent(page=i+1, text=text))

    return pages

# ---------------------------
# Optional: vector table extraction
# ---------------------------
def try_extract_tables(pdf_path: str, page_numbers: List[int]) -> Dict[int, str]:
    """Return {page_number: tables_as_text}. Tries Camelot then Tabula, if installed."""
    # Try Camelot
    try:
        import camelot  # type: ignore
        out: Dict[int, str] = {}
        for p in page_numbers:
            # Camelot page numbers are 1-based in the string argument
            tables = camelot.read_pdf(pdf_path, pages=str(p), flavor="lattice")
            if tables and tables.n > 0:
                joined = []
                for t in tables:
                    df = t.df
                    joined.append(df.to_markdown(index=False))
                out[p] = "\n\n".join(joined)
        if out:
            return out
    except Exception:
        pass

    # Try Tabula
    try:
        import tabula  # type: ignore
        out = {}
        for p in page_numbers:
            dfs = tabula.read_pdf(pdf_path, pages=p, multiple_tables=True)
            joined = []
            for df in dfs:
                joined.append(df.to_markdown(index=False))
            if joined:
                out[p] = "\n\n".join(joined)
        if out:
            return out
    except Exception:
        pass

    return {}

# ---------------------------
# Optional: OCR fallback (only if needed)
# ---------------------------
def ocr_page_to_text(pdf_path: str, page_number: int, dpi: int = 200) -> Optional[str]:
    """OCR a single page. Requires pytesseract + installed Tesseract (with Arabic language)."""
    try:
        import pytesseract  # type: ignore
        from PIL import Image  # type: ignore
    except Exception:
        return None

    doc = fitz.open(pdf_path)
    page = doc[page_number - 1]
    pix = page.get_pixmap(dpi=dpi)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Arabic + English often helps in mixed docs; adjust if needed.
    text = pytesseract.image_to_string(img, lang="ara+eng")
    return clean_text(text)

def enrich_pages_with_tables_and_ocr(pdf_path: str, pages: List[PageContent]) -> List[PageContent]:
    # 1) Determine table-like pages
    table_pages = [p.page for p in pages if detect_table_like(p.text)]

    # 2) Try to extract vector tables
    tables = try_extract_tables(pdf_path, table_pages)

    # 3) Apply extracted tables text
    for p in pages:
        if p.page in tables:
            p.tables_text = tables[p.page]
            p.used_table_extractor = "camelot/tabula"

    # 4) OCR only scanned pages (rare for your PDF)
    for p in pages:
        if is_probably_scanned(p.text):
            ocr_text = ocr_page_to_text(pdf_path, p.page)
            if ocr_text:
                p.text = ocr_text
                p.used_ocr = True

    return pages
