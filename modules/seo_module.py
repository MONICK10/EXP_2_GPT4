"""SEO Module - creates SEO keywords and a meta description.

Example: keywords = ["electric vehicles", "EV charging", ...]
         meta     = "Learn how electric vehicles work, their benefits and..." (max 160 characters)
"""
from llm import as_list, ask, ask_json


def keywords(topic, blog):
    # The task goes first AND is repeated after the blog: with the instruction only at the end,
    # Llama 3.2 reads past it and returns an empty {}.
    prompt = (f"Extract exactly 8 SEO keywords for a blog on \"{topic}\". "
              "Mix short keywords (1-2 words) and long-tail keywords (3-5 words).\n\n"
              f"BLOG:\n{blog[:1800]}\n\n"
              'Now return ONLY JSON with 8 keywords, like: '
              '{"keywords": ["kw1", "kw2", "kw3", "kw4", "kw5", "kw6", "kw7", "kw8"]}')
    for _ in range(2):  # one retry if the model returns an empty object
        data = ask_json(prompt, default={}) or {}
        out = as_list(data.get("keywords"))
        if len(out) >= 4:
            return out[:8]
    return out[:8]


def meta_description(topic, blog):
    prompt = (f"Write one SEO meta description for a blog on \"{topic}\".\n"
              "It must be ONE complete sentence of at most 150 characters, ending with a full stop. "
              "Make it engaging and include the main keyword. Return only the sentence, no quotes.\n\n"
              f"Blog:\n{blog[:1500]}\n\n"
              "Remember: one complete sentence, at most 150 characters.")
    best = ""
    for _ in range(3):  # ask again if the model overshoots, so we keep a whole sentence
        meta = ask(prompt, temperature=0.4).strip().strip('"').split("\n")[0].strip()
        if len(meta) <= 160:
            return {"meta": meta, "chars": len(meta)}
        if not best or len(meta) < len(best):
            best = meta
    meta = best[:157].rsplit(" ", 1)[0].rstrip(",;:") + "..."  # last resort: trim at a word
    return {"meta": meta, "chars": len(meta)}
