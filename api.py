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
    logger.error(f"Failed to initialize Agent Vish: {e}")
    agent_vish = None

# Health check endpoint for Render
@app.route('/', methods=['GET'])
def home():
    return 'Agent Vish API is running.'

# Chat endpoint
@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from the frontend."""
    try:
        # Validate request has JSON data
        if not request.is_json:
            logger.warning("Request is not JSON")
            return jsonify({
                'error': 'Content-Type must be application/json',
                'message': None,
                'response': None
            }), 400
        
        data = request.get_json()
        
        # Validate message field exists
        if 'message' not in data:
            logger.warning("Message field missing from request")
            return jsonify({
                'error': 'Missing required field: message',
                'message': None,
                'response': None
            }), 400
        
        user_message = data['message']
        
        # Only reject empty or whitespace-only messages
        if not user_message or not user_message.strip():
            logger.warning("Empty message received")
            return jsonify({
                'error': 'Message cannot be empty',
                'message': user_message,
                'response': None
            }), 400
        
        logger.info(f"Received message: {user_message[:50]}...")  # Log first 50 chars
        
        # Check if agent is initialized
        if agent_vish is None:
            logger.error("Agent Vish is not initialized")
            return jsonify({
                'error': 'Agent is not initialized',
                'message': user_message,
                'response': 'Sorry, the AI agent is currently unavailable. Please try again later.'
            }), 500
        
        # Process the message
        try:
            response = agent_vish.receive_message(user_message)
            logger.info(f"Response generated: {str(response)[:50]}...")  # Log first 50 chars
            
            return jsonify({
                'message': user_message,
                'response': response,
                'timestamp': datetime.now().isoformat()
            }), 200
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}", exc_info=True)
            return jsonify({
                'error': f'Error processing message: {str(e)}',
                'message': user_message,
                'response': 'Sorry, I encountered an error processing your message. Please try again.'
            }), 500
            
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}", exc_info=True)
        return jsonify({
            'error': f'Unexpected error: {str(e)}',
            'message': None,
            'response': 'Sorry, an unexpected error occurred. Please try again later.'
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal server error: {str(e)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
