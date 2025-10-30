from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import logging
from datetime import datetime
import json
import re
from werkzeug.exceptions import BadRequest

# Add the current directory to Python path to import agent_vish
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from agent_vish import AgenticAIBot
except ImportError:
    print("Warning: Could not import AgenticAIBot. Creating a mock version.")

    class AgenticAIBot:
        def __init__(self):
            self.skills = {}

        def receive_message(self, message):
            return f"Agent Vish received: {message}"

        def get_available_skills(self):
            return ["conversation", "analysis", "help"]

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Agent Vish
try:
    agent_vish = AgenticAIBot()
    logger.info("Agent Vish initialized successfully")
except Exception as e:
    logger.exception("Failed to initialize Agent Vish: %s", e)
    agent_vish = None

CONTROL_CHARS_PATTERN = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]")

def strip_control_chars(s: str) -> str:
    if not isinstance(s, str):
        return s
    return CONTROL_CHARS_PATTERN.sub("", s)

@app.route("/", methods=["GET"]) 
def health():
    return "OK", 200

@app.route("/chat", methods=["POST"]) 
def chat():
    try:
        # Read raw data safely first
        raw = request.get_data(cache=False, as_text=True) or ""
        # Remove control characters that could break JSON parsing
        cleaned = strip_control_chars(raw)

        # Attempt to parse JSON explicitly
        try:
            data = json.loads(cleaned) if cleaned else {}
        except json.JSONDecodeError as je:
            logger.error("JSON decode failed: %s", je)
            return jsonify({
                "error": "Invalid JSON",
                "message": "Request body must be valid JSON without control characters.",
                "hint": "Send {\"message\": \"text\"} with Content-Type: application/json"
            }), 400

        # Fallback to Flask's get_json if empty and content-type is proper
        if not data:
            try:
                data = request.get_json(silent=True) or {}
            except BadRequest:
                pass

        msg = data.get("message", "").strip()
        msg = strip_control_chars(msg)

        if not msg:
            return jsonify({
                "error": "Empty message",
                "message": "Provide a non-empty 'message' field"
            }), 400

        logger.info("Received message: %s", msg[:200] + ("..." if len(msg) > 200 else ""))

        if agent_vish is None:
            reply = "Service temporarily unavailable. Please try again later."
        else:
            reply = agent_vish.receive_message(msg)

        resp = {"ok": True, "message": reply, "timestamp": datetime.utcnow().isoformat() + "Z"}
        logger.info("Response generated: %s", (reply[:200] + ("..." if len(reply) > 200 else "")))
        return jsonify(resp), 200

    except Exception as e:
        logger.exception("Unexpected error in chat endpoint: %s", e)
        return jsonify({
            "error": "Server error",
            "message": "An unexpected error occurred. Please try again later."
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
