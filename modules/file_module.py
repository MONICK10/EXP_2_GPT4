"""File Module - saves the blog with its title, summary, keywords and meta description to a .txt file."""
import os
import re
from datetime import datetime

FOLDER = os.path.join(os.path.dirname(__file__), "..", "saved_blogs")


def save(d):
    os.makedirs(FOLDER, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "_", d.get("topic", "blog").lower()).strip("_")[:40]
    name = f"{slug}_{datetime.now():%Y%m%d_%H%M%S}.txt"
    lines = [
        "AI BLOG CONTENT GENERATOR - Monick S (URK23CS1167)",
        f"Saved on : {datetime.now():%d-%m-%Y %H:%M:%S}",
        f"Topic    : {d.get('topic', '')}",
        f"Style    : {d.get('style', '')} | Tone: {d.get('tone', '')} | Audience: {d.get('audience', '')}",
        "=" * 70,
        "TITLE OPTIONS:", *[f"  {i + 1}. {t}" for i, t in enumerate(d.get("titles") or [])],
        "", "SUMMARY:", d.get("summary") or "-",
        "", "SEO KEYWORDS: " + ", ".join(d.get("keywords") or []),
        "META DESCRIPTION: " + (d.get("meta") or "-"),
        "=" * 70, "", d.get("blog", ""),
    ]
    path = os.path.join(FOLDER, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return {"file": name, "path": os.path.abspath(path), "size": os.path.getsize(path)}
