"""Blog Module - builds a structured prompt (prompt engineering) and generates the blog.

Example prompt: "Write a 400-word Informative blog on Electric Vehicles for college students.
                 Tone: Friendly. Include Introduction, Main Content and Conclusion."
"""
from llm import ask

SYSTEM = "You are an expert blog writer. Write original, well-structured, easy-to-read blogs in Markdown."


def build_prompt(p):
    prompt = (f"Write a {p['word_count']}-word {p['style'].lower()} blog on \"{p['topic']}\".\n"
              f"Target audience: {p['audience']}.\nTone: {p['tone']}.\n"
              "Structure:\n# <Blog Title>\n## Introduction\n## <2-4 main section headings>\n## Conclusion\n"
              "Use simple English, short paragraphs and bullet points where useful.")
    if p["instructions"]:
        prompt += f"\nAdditional instructions: {p['instructions']}"
    return prompt


def generate(p):
    prompt = build_prompt(p)
    blog = ask(prompt, system=SYSTEM, temperature=0.7)
    return {"prompt": prompt, "blog": blog, "words": len(blog.split())}
