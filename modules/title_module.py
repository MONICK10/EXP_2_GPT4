"""Title Module - suggests 5 catchy blog titles.

Example: Electric Vehicles -> "Charging Ahead: Why EVs Are the Future of Indian Roads"
"""
from llm import as_list, ask_json


def titles(topic, blog=""):
    prompt = (f"Suggest 5 catchy, SEO-friendly blog titles (under 70 characters each) for a blog on \"{topic}\".\n"
              f"Blog start: {blog[:1200]}\n"
              'Return JSON: {"titles": ["...", "...", "...", "...", "..."]}')
    data = ask_json(prompt, temperature=0.8, default={}) or {}
    out = as_list(data.get("titles"))
    return out[:5] or [topic]
