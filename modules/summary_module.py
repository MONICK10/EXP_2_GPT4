"""Summary Module - writes a short summary of the generated blog (about 60 words)."""
import re

from llm import ask


def _strip_preamble(text):
    """Drop an opening line like 'Here is a summary of the blog in 60 words:'."""
    text = text.strip()
    first, sep, rest = text.partition("\n")
    if sep and first.rstrip().endswith(":") and len(first.split()) <= 20:
        return rest.strip()
    return re.sub(r"^here(?:'s| is)[^:]{0,80}:\s*", "", text, flags=re.I).strip()


def summarize(blog, words=60):
    prompt = (f"Summarize this blog in about {words} words, in one paragraph, simple English.\n"
              "Return only the summary paragraph. Do not write an introduction line.\n\n"
              f"{blog}")
    text = _strip_preamble(ask(prompt))
    return {"summary": text, "words": len(text.split())}
