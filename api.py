from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import logging
from datetime import datetime

# Add the current directory to Python path to import agent_vish
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from agent_vish import AgentVish
except ImportError:
    print("Warning: Could not import AgentVish. Creating a mock version.")
    class AgentVish:
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
    agent_vish = AgentVish()
    logger.info("Agent Vish initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Agent Vish: {e}")
    agent_vish = AgentVish()  # Use mock version

# Store conversation history (in production, use a database)
conversation_history = []

@app.route('/', methods=['GET'])
def home():
    """Home endpoint providing API information"""
    return jsonify({
        'service': 'Agent Vish API',
        'version': '1.0.0',
        'status': 'active',
        'endpoints': {
            '/': 'GET - API information',
            '/health': 'GET - Health check',
            '/chat': 'POST - Chat with Agent Vish',
            '/skills': 'GET - List available skills',
            '/conversation': 'GET - Get conversation history',
            '/conversation/clear': 'POST - Clear conversation history'
        },
        'description': 'Flask API for Agent Vish - An AI assistant with multiple skills'
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'agent_status': 'active' if agent_vish else 'inactive',
        'version': '1.0.0'
    }), 200

@app.route('/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint to interact with Agent Vish.
    
    Expects JSON payload:
    {
        "message": "Your message here",
        "user_id": "optional_user_identifier",
        "context": "optional_additional_context"
    }
    
    Returns:
    {
        "status": "success",
        "message": "user_message",
        "response": "agent_response",
        "timestamp": "ISO_timestamp",
        "conversation_id": "conversation_identifier"
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate input
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Missing required field: message',
                'status': 'error'
            }), 400
        
        user_message = data['message'].strip()
        user_id = data.get('user_id', 'anonymous')
        context = data.get('context', '')
        
        if not user_message:
            return jsonify({
                'error': 'Message cannot be empty',
                'status': 'error'
            }), 400
        
        # Process message with Agent Vish
        try:
            if hasattr(agent_vish, 'process_message'):
                bot_response = agent_vish.process_message(user_message)
            else:
                # Fallback response
                bot_response = f"Agent Vish received: {user_message}"
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            bot_response = "I'm experiencing some technical difficulties. Please try again later."
        
        # Create conversation entry
        conversation_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'message': user_message,
            'response': bot_response,
            'context': context
        }
        
        # Add to conversation history (limit to last 100 entries)
        conversation_history.append(conversation_entry)
        if len(conversation_history) > 100:
            conversation_history.pop(0)
        
        # Return successful response
        return jsonify({
            'status': 'success',
            'message': user_message,
            'response': bot_response,
            'timestamp': conversation_entry['timestamp'],
            'conversation_id': len(conversation_history)
        }), 200
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        return jsonify({
            'error': f'An unexpected error occurred: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/skills', methods=['GET'])
def get_skills():
    """
    Get list of available skills from Agent Vish
    
    Returns:
    {
        "status": "success",
        "skills": ["skill1", "skill2", ...],
        "count": number_of_skills
    }
    """
    try:
        if hasattr(agent_vish, 'get_available_skills'):
            skills = agent_vish.get_available_skills()
        else:
            # Default skills if method doesn't exist
            skills = ["conversation", "analysis", "help", "general_assistance"]
        
        return jsonify({
            'status': 'success',
            'skills': skills,
            'count': len(skills),
            'description': 'Available skills for Agent Vish'
        }), 200
        
    except Exception as e:
        logger.error(f"Skills endpoint error: {e}")
        return jsonify({
            'error': f'Error retrieving skills: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/conversation', methods=['GET'])
def get_conversation():
    """
    Get conversation history
    
    Query parameters:
    - limit: Maximum number of entries to return (default: 50)
    - user_id: Filter by specific user ID
    
    Returns:
    {
        "status": "success",
        "conversations": [...],
        "total": total_count,
        "returned": returned_count
    }
    """
    try:
        limit = int(request.args.get('limit', 50))
        user_id = request.args.get('user_id')
        
        # Filter conversations
        filtered_conversations = conversation_history
        if user_id:
            filtered_conversations = [
                conv for conv in conversation_history 
                if conv.get('user_id') == user_id
            ]
        
        # Apply limit
        returned_conversations = filtered_conversations[-limit:] if limit > 0 else filtered_conversations
        
        return jsonify({
            'status': 'success',
            'conversations': returned_conversations,
            'total': len(filtered_conversations),
            'returned': len(returned_conversations)
        }), 200
        
    except Exception as e:
        logger.error(f"Conversation endpoint error: {e}")
        return jsonify({
            'error': f'Error retrieving conversations: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/conversation/clear', methods=['POST'])
def clear_conversation():
    """
    Clear conversation history
    
    Optional JSON payload:
    {
        "user_id": "specific_user_to_clear"
    }
    
    Returns:
    {
        "status": "success",
        "message": "Conversation history cleared",
        "cleared_count": number_of_entries_cleared
    }
    """
    try:
        global conversation_history
        
        data = request.get_json() or {}
        user_id = data.get('user_id')
        
        if user_id:
            # Clear specific user's conversation
            initial_count = len(conversation_history)
            conversation_history = [
                conv for conv in conversation_history 
                if conv.get('user_id') != user_id
            ]
            cleared_count = initial_count - len(conversation_history)
            message = f"Cleared conversation history for user: {user_id}"
        else:
            # Clear all conversations
            cleared_count = len(conversation_history)
            conversation_history = []
            message = "Cleared all conversation history"
        
        return jsonify({
            'status': 'success',
            'message': message,
            'cleared_count': cleared_count
        }), 200
        
    except Exception as e:
        logger.error(f"Clear conversation endpoint error: {e}")
        return jsonify({
            'error': f'Error clearing conversations: {str(e)}',
            'status': 'error'
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'error',
        'code': 404
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'error': 'Method not allowed',
        'status': 'error',
        'code': 405
    }), 405

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'error': 'Internal server error',
        'status': 'error',
        'code': 500
    }), 500

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Get debug mode from environment variable
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Agent Vish API on port {port}")
    logger.info(f"Debug mode: {debug_mode}")
    logger.info(f"Available endpoints: /, /health, /chat, /skills, /conversation")
    
    # Run the Flask app
    app.run(
        debug=debug_mode,
        host='0.0.0.0',
        port=port,
        threaded=True
    )
