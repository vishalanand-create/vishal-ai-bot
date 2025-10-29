from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    """
    Chat endpoint to interact with Vishal AI Bot.
    Expects JSON with 'message' field and returns bot response.
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate input
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Missing required field: message'
            }), 400
        
        user_message = data['message']
        
        # TODO: Replace this with actual Vishal AI Bot logic
        # For now, this is a simple echo response
        bot_response = f"Vishal AI Bot received: {user_message}"
        
        # Return bot response as JSON
        return jsonify({
            'status': 'success',
            'message': user_message,
            'response': bot_response
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint.
    """
    return jsonify({
        'status': 'healthy',
        'service': 'Vishal AI Bot API'
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
