"""Summary Module - writes a short summary of the generated blog (about 60 words)."""
from llm import ask


def summarize(blog, words=60):
    prompt = f"Summarize this blog in about {words} words, in one paragraph, simple English:\n\n{blog}"
    text = ask(prompt)
    return {"summary": text, "words": len(text.split())}
