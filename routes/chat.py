from flask import Blueprint, request, jsonify
from utils.ai_chat import ChatService

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')
chat_service = ChatService()

@chat_bp.route('/message', methods=['POST'])
def chat_message():
    data = request.get_json()
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    response = chat_service.get_response(user_message)
    return jsonify({'response': response})
