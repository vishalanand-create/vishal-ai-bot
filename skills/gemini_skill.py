"""Google Gemini Pro Integration Skill for Agent Vish

Provides Gemini Pro AI integration for intelligent responses.
"""

import os
import logging
from typing import Optional, List, Dict

try:
    import google.generativeai as genai
except ImportError:
    genai = None

logger = logging.getLogger(__name__)


class GeminiSkill:
    """Skill for querying Google Gemini Pro models"""
    
    def __init__(self):
        """Initialize Gemini skill with API key"""
        if genai is None:
            raise ImportError("google-generativeai package not installed. Run: pip install google-generativeai")
        
        api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)
        
        # Use gemini-pro (you have Pro access)
        model_name = os.environ.get("GEMINI_MODEL", "gemini-pro")
        self.model = genai.GenerativeModel(model_name)
        
        logger.info(f"Gemini skill initialized with model: {model_name}")
    
    def _build_prompt(self, user_message: str, context: Optional[List[Dict]] = None) -> str:
        """Build a comprehensive prompt with system instructions and context"""
        system_prompt = """You are Agent Vish, an intelligent AI assistant for MyOperator.

Your role:
- Assist with customer success and onboarding queries
- Provide guidance on MyOperator features and integrations
- Help with troubleshooting and technical support
- Be professional, concise, and helpful

Critical Rules:
- If you don't know specific MyOperator details, say so clearly
- Never make up features or capabilities
- Always prioritize accuracy over completeness
- Suggest contacting MyOperator support for account-specific issues
"""
        
        prompt_parts = [system_prompt]
        
        # Add conversation context if provided
        if context:
            prompt_parts.append("\n--- Conversation History ---")
            for msg in context[-3:]:  # Last 3 messages
                role = msg.get("role", "user")
                content = msg.get("content", "")
                prompt_parts.append(f"{role.capitalize()}: {content}")
            prompt_parts.append("--- End History ---\n")
        
        # Add current user message
        prompt_parts.append(f"\nUser: {user_message}\n\nAssistant:")
        
        return "\n".join(prompt_parts)
    
    def query(self, user_message: str, context: Optional[List[Dict]] = None) -> str:
        """Query Gemini Pro with user message and optional context
        
        Args:
            user_message: The user's message/question
            context: Optional conversation history [{"role": "user/assistant", "content": "..."}]
            
        Returns:
            AI-generated response string
        """
        try:
            prompt = self._build_prompt(user_message, context)
            
            logger.info(f"Querying Gemini Pro: {user_message[:50]}...")
            
            response = self.model.generate_content(prompt)
            
            # Check if response was blocked
            if not response.text:
                logger.warning("Gemini response was blocked or empty")
                return "I couldn't generate a response for that query. Please rephrase or contact support."
            
            answer = response.text
            logger.info(f"Gemini Pro response: {answer[:50]}...")
            
            return answer
            
        except Exception as e:
            logger.error(f"Gemini query failed: {e}")
            return "I'm having trouble processing that right now. Please try again or contact support."
    
    def is_available(self) -> bool:
        """Check if Gemini service is available"""
        try:
            api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
            return bool(api_key and genai)
        except:
            return False


# Example usage
if __name__ == "__main__":
    skill = GeminiSkill()
    response = skill.query("What is MyOperator?")
    print(response)
