"""SEO Module - creates SEO keywords and a meta description.

Example: keywords = ["electric vehicles", "EV charging", ...]
         meta     = "Learn how electric vehicles work, their benefits and..." (max 160 characters)
"""
from llm import as_list, ask, ask_json


def keywords(topic, blog):
    prompt = (f"Extract 8 SEO keywords or key phrases for a blog on \"{topic}\". Mix short and long-tail keywords.\n"
              f"Blog:\n{blog[:3000]}\n"
              'Return JSON: {"keywords": ["...", "..."]}')
    data = ask_json(prompt, default={}) or {}
    return as_list(data.get("keywords"))[:10]


def meta_description(topic, blog):
    prompt = (f"Write one SEO meta description for a blog on \"{topic}\". Maximum 155 characters. "
              "Make it engaging and include the main keyword. Return only the sentence, no quotes.\n\n"
              f"Blog:\n{blog[:2000]}")
    meta = ask(prompt).strip().strip('"')
    if len(meta) > 160:  # keep it within Google's limit
        meta = meta[:157].rsplit(" ", 1)[0] + "..."
    return {"meta": meta, "chars": len(meta)}
