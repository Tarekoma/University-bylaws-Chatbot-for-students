from __future__ import annotations

import streamlit as st

from config import Config
from retriever import retrieve
from llm_client import answer_with_groq, simple_extractive_answer

cfg = Config()

st.set_page_config(page_title="Engineering Regulations Chatbot", page_icon="🎓", layout="wide")
st.title("🎓 Engineering Regulations Chatbot")
st.caption("Answers are based on your PDF regulations (RAG).")

with st.sidebar:
    st.header("Settings")
    st.write(f"PDF_PATH: `{cfg.PDF_PATH}`")
    st.write(f"Chroma: `{cfg.CHROMA_DIR}`")
    st.write(f"Top-K: `{cfg.TOP_K}`")
    st.write(f"Embedding: `{cfg.EMBEDDING_MODEL}`")
    if cfg.GROQ_API_KEY:
        st.success("Groq API key detected ✅")
    else:
        st.warning("No GROQ_API_KEY found. The app will show retrieved text only.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Ask about registration, GPA, warnings, graduation project, etc...")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving relevant rules..."):
            hits = retrieve(question, cfg)

        # If no LLM key, show retrieval results
        answer = answer_with_groq(question, hits, cfg)

        if not answer:
            extracted = simple_extractive_answer(question, hits)
            if extracted:
                st.markdown(extracted)
                final = extracted
            else:
                # Show retrieval-only snippets
                st.markdown("**(LLM not available — showing top retrieved text snippets)**")
            for i, h in enumerate(hits, 1):
                meta = h.get("meta", {})
                st.markdown(f"**[{i}] Page {meta.get('page_start','?')} | Article {meta.get('article','')}**")
                st.markdown(h["text"][:1200] + ("..." if len(h["text"]) > 1200 else ""))
                st.markdown("---")
            final = "LLM not available. Install `groq` and set `GROQ_API_KEY` in `.env` to generate concise answers."
        else:
            st.markdown(answer)
            final = answer

    st.session_state.messages.append({"role": "assistant", "content": final})
