"""
Ex. No. 2 - AI-Powered Blog Content Generator using Ollama
Monick S - URK23CS1167

Run:  python app.py    then open  http://localhost:5002
"""
from flask import Flask, jsonify, render_template, request

from llm import LLMError, status
from modules import blog_module, file_module, input_module, seo_module, summary_module, title_module
from modules import intent_module

app = Flask(__name__)


@app.errorhandler(LLMError)
def llm_error(e):
    return jsonify(error=str(e)), 503


@app.errorhandler(ValueError)
def bad_input(e):
    return jsonify(error=str(e)), 400


def need_blog(d):
    if not (d.get("blog") or "").strip():
        raise ValueError("Generate a blog first.")
    return d["blog"]


@app.get("/")
def home():
    return render_template("index.html", exp_no=2, title="BlogCraft AI – Blog Content Generator",
                           styles=input_module.STYLES, tones=input_module.TONES)


@app.get("/api/status")
def api_status():
    return jsonify(status())


@app.post("/api/generate")
def api_generate():
    params = input_module.collect(request.get_json())
    return jsonify({"params": params, **blog_module.generate(params)})


@app.post("/api/titles")
def api_titles():
    d = request.get_json()
    return jsonify(titles=title_module.titles(d.get("topic", ""), need_blog(d)))


@app.post("/api/summary")
def api_summary():
    return jsonify(summary_module.summarize(need_blog(request.get_json())))


@app.post("/api/seo")
def api_seo():
    d = request.get_json()
    return jsonify(keywords=seo_module.keywords(d.get("topic", ""), need_blog(d)))


@app.post("/api/meta")
def api_meta():
    d = request.get_json()
    return jsonify(seo_module.meta_description(d.get("topic", ""), need_blog(d)))


@app.post("/api/save")
def api_save():
    d = request.get_json()
    need_blog(d)
    return jsonify(file_module.save(d))


@app.post("/api/intent")
def api_intent():
    """Detect what the user wants, then run that module."""
    d = request.get_json()
    text = (d.get("text") or "").strip()
    if not text:
        raise ValueError("Type a request first.")
    intent = intent_module.detect(text)
    action = intent["intent"]
    result = {}
    if action == "BLOG":
        params = input_module.collect({**d.get("params", {}), "topic": intent.get("topic") or d.get("topic") or text})
        result = {"params": params, **blog_module.generate(params)}
    elif action == "TITLE":
        result = {"titles": title_module.titles(d.get("topic", ""), need_blog(d))}
    elif action == "SUMMARY":
        result = summary_module.summarize(need_blog(d))
    elif action == "SEO":
        result = {"keywords": seo_module.keywords(d.get("topic", ""), need_blog(d))}
    elif action == "META":
        result = seo_module.meta_description(d.get("topic", ""), need_blog(d))
    elif action == "SAVE":
        result = file_module.save({**d, "blog": need_blog(d)})
    return jsonify(intent=intent, result=result)


if __name__ == "__main__":
    app.run(port=5002, debug=False)
