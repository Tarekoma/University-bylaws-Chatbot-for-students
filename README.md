<div align="center">

# 🎓 CERA — Computer Engineering Regulations Assistant
### An AI-Powered Chatbot for University Bylaws Navigation

**Transforming complex university regulations into accessible, accurate, and instant guidance — empowering students, not overwhelming them.**

</div>

---

## 📖 Overview

**CERA** is an AI-powered assistant designed to help students navigate university regulations efficiently. Built on a **Retrieval-Augmented Generation (RAG)** system, it solves the problem of students struggling to find accurate answers in large, complex academic policy documents — by retrieving and presenting precise information on demand. A second approach via **LLM Automation on Telegram** makes the system practically accessible for everyday student use.

🎬 Video Demo : __[Watch Demo Here](https://1drv.ms/v/c/47438efdb3ee2559/IQDhzmlYoC2cR5d_NL7iZ8PUAVkdVgNEk7dEV5FYvVPJr3U?e=o2SKoE)__

---

## 🔍 Problems We Solve

| # | Problem |
|---|---------|
| 1 | University bylaws are long, complex documents written in formal legal language |
| 2 | Students struggle to find specific answers through manual searching |
| 3 | No interactive or intelligent way to query official university regulations |
| 4 | Arabic legal text with mixed formatting makes automated processing challenging |
| 5 | Tables, embedded content, and unstructured PDFs hinder accurate retrieval |

---

## ✨ Core Features

### 🤖 AI Capabilities

| Feature | Description |
|---|---|
| 🧠 **RAG-Based Retrieval** | Extracts, chunks, and semantically searches bylaws to return grounded, traceable answers |
| 💬 **Natural Language Q&A** | Students ask questions in plain Arabic or English and receive instant, accurate responses |
| 📎 **Source Referencing** | Answers are tied to specific articles and pages in official documents |
| 🔎 **Semantic Search** | Uses vector embeddings and ChromaDB to find the most relevant regulation chunks |
| 🤖 **Telegram Automation** | LLM-powered chatbot via n8n workflows for high-usability student access |

### 🏫 System Capabilities

- 📄 Processes official Arabic university regulation PDFs automatically
- 🧹 Cleans and chunks legal text by articles and size for accurate retrieval
- 🗄️ Stores embeddings in **ChromaDB** vector database for fast semantic lookup
- 🌐 Supports **Arabic and English** mixed content natively
- ⚡ Provides instant responses — no waiting for office hours or admin replies
- 🔧 Scalable and customizable across faculties, universities, or policy documents

---

## ⚙️ Dual Approach Architecture

| Approach | Focus | Key Advantage |
|---|---|---|
| 🔬 **RAG-Based Chatbot** | Academic rigor · Explainability · Traceability | Answers grounded strictly in official documents |
| 📡 **LLM via Telegram (n8n)** | Practical usability · Reliability · Student experience | Familiar interface with instant automated responses |

> 🧩 Both systems address the same problem but follow different technical strategies — independently deployable and complementary.

---

## 🗂️ RAG System Architecture

### 🔄 Offline Phase — Document Indexing
```
PDF Regulations → Text Extraction → Text Cleaning
→ Chunking (by articles & size) → Embedding Generation → Vector Database (ChromaDB)
```

### 🌐 Online Phase — Query & Answer
```
User Question → Query Embedding → Vector Search (Top-K Chunks)
→ LLM Answer Generation → Final Answer to User
```

> 💡 If the LLM is unavailable, the system falls back to retrieved text snippets or rule-based extraction.

---

## 🚀 Implementation Plan

1. **Data Collection** — Gathered official university bylaws in PDF format
2. **Preprocessing** — Extracted, cleaned, and chunked Arabic legal text by articles
3. **Embedding & Indexing** — Generated semantic embeddings and stored them in ChromaDB
4. **RAG Pipeline** — Built retrieval + LLM generation pipeline for traceable Q&A
5. **Telegram Integration** — Deployed LLM automation via n8n workflows on Telegram
6. **Testing & Evaluation** — Validated answer accuracy, source referencing, and Arabic support

---

## 🎯 Objectives

- ✅ Answer students' questions using natural language in Arabic and English
- ✅ Ensure all answers are grounded in official university documents only
- ✅ Provide article-level and page-level source references for every answer
- ✅ Reduce confusion, manual searching, and repetitive administrative inquiries
- ✅ Deliver a scalable foundation for future multi-faculty or multi-university deployment

---

## 🏆 Benefits

| Benefit | Description |
|---|---|
| ⏱️ **Time Efficiency** | Eliminates hours of manual PDF searching for students and staff |
| 🕐 **24/7 Availability** | Students get immediate answers anytime without waiting for office hours |
| 📈 **Scalable & Customizable** | Easily adapted for different faculties, universities, or policy documents |

---

## 📁 Project Structure

| File | Owner | Description |
|---|---|---|
| `app.py` | Sandy | Main application entry point |
| `build_index.py` | Sandy | Builds the ChromaDB vector index |
| `bylaws.pdf` | Sandy | Official university regulations source |
| `chunking.py` | Hossam | Text chunking by articles and size |
| `config.py` | Mary | Configuration and environment settings |
| `pdf_extract.py` | Mary | PDF text extraction module |
| `embeddings_store.py` | Tarek | Embedding generation and storage |
| `llm_client.py` | Tarek | LLM API integration (Gemini) |
| `retriever.py` | Ibrahim | Semantic search and retrieval logic |
| `text_cleaning.py` | Ibrahim | Arabic text cleaning and normalization |

---

## 👥 Team

| Name | Role |
|---|---|
| Tarek Omar Mahmoud | Embeddings & LLM Integration |
| Ahmed Hossam Hussin | Text Chunking |
| Mohamed Ibrahim Mohamed | Retrieval & Text Cleaning |
| Sandy Alaa Ayiad | App & Index Builder |
| Mary Noshy Ayiad | PDF Extraction & Config |

---

<div align="center">
  Made with ❤️ by <strong>CERA Team</strong> · AI for Smarter Student Experience 🎓
</div>
