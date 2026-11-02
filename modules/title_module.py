"""Title Module - suggests 5 catchy blog titles.

Example: Electric Vehicles -> "Charging Ahead: Why EVs Are the Future of Indian Roads"
"""
import re

from llm import as_list, ask_json


def _clean(t):
    """The model sometimes copies the blog's '# Heading' markdown or wraps the title in quotes."""
    return re.sub(r"^#{1,6}\s*", "", str(t).strip()).strip().strip('"').strip()


def titles(topic, blog=""):
    prompt = (f"Suggest 5 catchy, SEO-friendly blog titles (under 70 characters each) for a blog on \"{topic}\".\n"
              "Make them creative and clickable - use a hook, a question or a colon subtitle. "
              "Do not simply restate the topic, and do not reuse the blog's own headings.\n"
              "Do not begin a title with '#' or a number.\n\n"
              f"BLOG START:\n{blog[:1200]}\n\n"
              'Now return ONLY JSON: {"titles": ["t1", "t2", "t3", "t4", "t5"]}')
    data = ask_json(prompt, temperature=0.8, default={}) or {}
    out = [t for t in (_clean(x) for x in as_list(data.get("titles"))) if t]
    return out[:5] or [topic]
