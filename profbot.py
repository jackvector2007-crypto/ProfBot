import os
import json
from flask import Flask, jsonify, request

# Minimal, valid Flask application for deployment on Render.
# Exposes `app` so gunicorn can import profbot:app

app = Flask(__name__)

HERE = os.path.dirname(__file__)
DATA_FILE = os.path.join(HERE, "profbot_v14_monstre_absolu.json")

# Load data if present (non-fatal)
_data = {}
if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            _data = json.load(f)
    except Exception:
        _data = {}

@app.route("/")
def index():
    return jsonify({
        "status": "ok",
        "message": "ProfBot is running",
        "endpoints": ["/health", "/info"]
    })

@app.route("/health")
def health():
    return "OK", 200

@app.route("/info")
def info():
    # Return a small summary of the loaded data (if any)
    summary = {
        "has_data_file": os.path.exists(DATA_FILE),
        "loaded_keys_count": len(_data) if isinstance(_data, dict) else 0,
    }
    return jsonify(summary)

# Add a simple POST example endpoint
@app.route("/ask", methods=["POST"]) 
def ask():
    payload = request.get_json(silent=True) or {}
    question = payload.get("q") or payload.get("question") or ""
    # This is a placeholder: implement your bot logic here.
    answer = {
        "question": question,
        "answer": "ProfBot received your question. Implement the logic in profbot.py to answer."
    }
    return jsonify(answer)

if __name__ == "__main__":
    # Local dev server (uses PORT env var if present for parity with Render)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
