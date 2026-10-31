"""Input Module - collects and checks the user's blog settings.

Example: {"topic": "Electric Vehicles", "style": "Informative", "tone": "Friendly", "word_count": 400}
"""
STYLES = ["Professional", "Informative", "Conversational", "Storytelling", "Technical", "Listicle"]
TONES = ["Friendly", "Formal", "Persuasive", "Inspirational", "Neutral", "Humorous"]


def collect(data):
    topic = (data.get("topic") or "").strip()
    if len(topic) < 3:
        raise ValueError("Please enter a blog topic.")
    try:
        words = int(data.get("word_count") or 400)
    except ValueError:
        words = 400
    return {
        "topic": topic,
        "style": data.get("style") if data.get("style") in STYLES else "Informative",
        "tone": data.get("tone") if data.get("tone") in TONES else "Friendly",
        "audience": (data.get("audience") or "General readers").strip(),
        "word_count": max(150, min(words, 1500)),
        "instructions": (data.get("instructions") or "").strip(),
    }
