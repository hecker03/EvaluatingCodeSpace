import google.generativeai as genai
import os

class ChatService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            # Fallback or log warning - for now we'll just print
            print("WARNING: GOOGLE_API_KEY not found in environment variables.")
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-2.0-flash")
            self.chat = self.model.start_chat(history=[])

    def get_response(self, message):
        if not hasattr(self, 'chat'):
            return "Error: Chat service not initialized. Please check API key."
        
        try:
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
