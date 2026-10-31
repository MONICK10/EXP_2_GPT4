"""Intent Module - understands a free-text request and decides which module to run.

Example: "give me some catchy headings"   -> TITLE
         "make it short"                  -> SUMMARY
         "what keywords should I target?" -> SEO
"""
from llm import ask_json

INTENTS = {
    "BLOG": "write or rewrite a full blog",
    "TITLE": "suggest blog titles or headings",
    "SUMMARY": "summarize or shorten the blog",
    "SEO": "SEO keywords or tags",
    "META": "meta description for search engines",
    "SAVE": "save or download the blog to a file",
}


def keyword_intent(text):
    t = text.lower()
    rules = [("META", ["meta"]), ("SEO", ["seo", "keyword", "tag"]), ("TITLE", ["title", "heading", "headline"]),
             ("SUMMARY", ["summar", "short", "tl;dr", "brief"]), ("SAVE", ["save", "download", "file"])]
    for intent, words in rules:
        if any(w in t for w in words):
            return intent
    return "BLOG"


def detect(text):
    options = "\n".join(f"{k} - {v}" for k, v in INTENTS.items())
    prompt = (f"A user of a blog-writing app typed: \"{text}\"\nChoose the one intent that matches:\n{options}\n"
              'Return JSON: {"intent": "<INTENT>", "topic": "<blog topic if the user mentioned one, else empty>", '
              '"reason": "<short reason>"}')
    data = ask_json(prompt, default={}) or {}
    intent = str(data.get("intent", "")).upper()
    if intent not in INTENTS:
        return {"intent": keyword_intent(text), "topic": "", "reason": "Keyword fallback", "source": "rules"}
    return {"intent": intent, "topic": data.get("topic", ""), "reason": data.get("reason", ""), "source": "LLM"}
