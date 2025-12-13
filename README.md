# Engineering Regulations Chatbot (RAG)

A small chatbot that answers students' questions using your **Undergraduate Regulations of the College of Engineering** PDF.

## What this project does
- Extracts and cleans Arabic text from the PDF (incl. converting Arabic presentation forms to normal letters via Unicode NFKC)
- Splits content by **articles (مادة)** + safe chunking
- Builds a local **Chroma** vector database using **Sentence-Transformers (E5 multilingual)**
- Provides a **Streamlit** chat UI
- Optional: tries vector **table extraction** (Camelot / Tabula) and falls back to **OCR** *only for pages that need it*

---

## 1) Setup (PyCharm / Windows 11)

### Create venv
```bash
python -m venv .venv
.venv\Scripts\activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Put your PDF
Copy your regulations PDF into this folder and name it:
`bylaws.pdf`

(or change `PDF_PATH` in `.env`)

### Add your API key (Groq recommended)
Copy `.env.example` to `.env` and fill:
- `GROQ_API_KEY=...`

---

## 2) Build the index
```bash
python build_index.py
```

It will create a local vector DB in `./chroma_db`.

---

## 3) Run the chatbot
```bash
streamlit run app.py
```

---

## Optional (only if you need it)
### Camelot (vector tables)
Camelot may require Ghostscript on Windows if you use lattice mode. If you don't have tables, you can ignore it.

### Tabula (vector tables)
Tabula needs Java installed.

### OCR fallback
OCR needs Tesseract installed + Arabic language pack.
If your PDF is already text-based, OCR is not needed.

---

## Troubleshooting
- If the chatbot answers poorly: increase `TOP_K` to 6–10, or reduce `CHUNK_CHARS`.
- If Arabic text looks broken: this project normalizes using Unicode NFKC (works well for many PDFs).


## If you see: 'LLM not available'
Install Groq client:
```bash
pip install groq
```
