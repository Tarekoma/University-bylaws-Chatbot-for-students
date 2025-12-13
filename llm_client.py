from __future__ import annotations

from typing import List, Dict, Any, Optional
from config import Config

SYSTEM_PROMPT = """أنت مساعد جامعي متخصص في لوائح وأنظمة كلية الهندسة.
مهمتك: الإجابة فقط اعتماداً على النص المسترجع من اللائحة.

قواعد الإخراج (مهم جداً):
1) ابدأ بسطر واحد مباشر جداً بصيغة: "الإجابة: ..."
2) بعده سطر "الدليل:" وتذكر رقم الصفحة (والمادة إن وجدت).
3) لا تكتب أكثر من 3 نقاط توضيح.
4) إذا لم تجد المعلومة في السياق، قل: "الإجابة: لم أجد ذلك في اللائحة المرفقة".
5) لا تخترع أرقاماً أو شروطاً غير موجودة.
"""

def build_user_prompt(question: str, contexts: List[Dict[str, Any]]) -> str:
    blocks = []
    for idx, c in enumerate(contexts, 1):
        meta = c.get("meta", {}) or {}
        page = meta.get("page_start", "?")
        art = meta.get("article", "")
        title = meta.get("title", "")
        header = f"[{idx}] صفحة: {page}"
        if art:
            header += f" | مادة: {art}"
        if title:
            header += f" | {title}"
        blocks.append(header + "\n" + c["text"])

    context_text = "\n\n---\n\n".join(blocks) if blocks else "(لا يوجد سياق)"
    return f"""سؤال الطالب:
{question}

السياق من اللائحة:
{context_text}

اكتب الإجابة بالعربية (وبإمكانك إضافة سطر إنجليزي مختصر إذا كان السؤال بالإنجليزية).
"""

def answer_with_groq(question: str, contexts: List[Dict[str, Any]], cfg: Config) -> Optional[str]:
    if not cfg.GROQ_API_KEY:
        return None

    try:
        from groq import Groq  # type: ignore
    except Exception:
        return None

    client = Groq(api_key=cfg.GROQ_API_KEY)

    user_prompt = build_user_prompt(question, contexts)

    chat = client.chat.completions.create(
        model=cfg.GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        max_tokens=800,
    )

    return chat.choices[0].message.content


import re
from text_cleaning import normalize_nfkc

def _snippet_around(text: str, start: int, end: int, window: int = 140) -> str:
    s = max(0, start - window)
    e = min(len(text), end + window)
    return text[s:e].strip()

def simple_extractive_answer(question: str, contexts: List[Dict[str, Any]]) -> Optional[str]:
    """Rule-based concise answer when LLM is not available."""
    q = normalize_nfkc(question)

    # Q: graduation credit hours?
    if ("الساعات" in q and "التخرج" in q) or ("عدد" in q and "التخرج" in q and "ساع" in q):
        patterns = [
            r"عدد\s+الساعات\s+المعتمدة\s+اللازمة\s+للتخرج\s+هو\s*([0-9٠-٩]+)",
            r"إجمالي\s+عدد\s+الساعات\s+المعتمدة\s+اللازمة\s+للتخرج\s+هو\s*([0-9٠-٩]+)",
            r"اللازمة\s+للتخرج\s+هو\s*([0-9٠-٩]+)\s*ساعة\s+معتمدة",
        ]
        for c in contexts:
            t = c.get("text", "")
            for pat in patterns:
                m = re.search(pat, t)
                if m:
                    n = m.group(1).translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789"))
                    meta = c.get("meta", {}) or {}
                    page = meta.get("page_start", "?")
                    art = meta.get("article", "")
                    snip = _snippet_around(t, m.start(), m.end())
                    return (
                        f"**الإجابة:** عدد الساعات المعتمدة اللازمة للتخرج هو **{n} ساعة معتمدة**.\n\n"
                        f"**الدليل:** صفحة {page}" + (f" | مادة {art}" if art else "") + f"\n\n> {snip}"
                    )

        return "**الإجابة:** لم أجد رقم الساعات اللازمة للتخرج في المقاطع المسترجعة."

    return None
