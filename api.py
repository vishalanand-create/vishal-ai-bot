from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import logging
from datetime import datetime

# Add the current directory to Python path to import agent_vish
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from agent_vish import AgenticAIBot
except ImportError:
    print("Warning: Could not import AgenticAIBot. Creating a mock version.")
    class AgenticAIBot:
        def __init__(self):
            self.skills = {}
            
        def process_message(self, message):
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
    logger.error(f"Failed to initialize Agent Vish: {e}")
    agent_vish = None

# Health check endpoint for Render
@app.route('/', methods=['GET'])
def home():
    return 'Agent Vish API is running.'
