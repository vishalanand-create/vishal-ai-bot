"""ChatGPT Integration Skill for Agent Vish

Provides OpenAI GPT integration for intelligent conversational responses.
"""

import os
import logging
from typing import Optional, List, Dict

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

logger = logging.getLogger(__name__)


class ChatGPTSkill:
    """Skill for querying OpenAI ChatGPT models"""
    
    def __init__(self):
        """Initialize ChatGPT skill with API key"""
        if OpenAI is None:
            raise ImportError("openai package not installed. Run: pip install openai")
        
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.client = OpenAI(api_key=api_key)
        self.model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
        self.system_prompt = self._get_system_prompt()
        logger.info(f"ChatGPT skill initialized with model: {self.model}")
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for Agent Vish"""
        return """You are Agent Vish, an intelligent AI assistant for MyOperator.

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
    
    def query(self, user_message: str, context: Optional[List[Dict]] = None, 
             temperature: float = 0.7, max_tokens: int = 500) -> str:
        """Query ChatGPT with user message and optional context
        
        Args:
            user_message: The user's message/question
            context: Optional conversation history [{"role": "user/assistant", "content": "..."}]
            temperature: Controls randomness (0.0-1.0). Lower = more focused
            max_tokens: Maximum response length
            
        Returns:
            AI-generated response string
        """
        try:
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add conversation context if provided
            if context:
                messages.extend(context[-5:])  # Last 5 messages for context
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            logger.info(f"Querying ChatGPT: {user_message[:50]}...")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                n=1
            )
            
            answer = response.choices[0].message.content
            logger.info(f"ChatGPT response: {answer[:50]}...")
            
            return answer
            
        except Exception as e:
            logger.error(f"ChatGPT query failed: {e}")
            return f"I'm having trouble processing that right now. Please try again or contact support."
    
    def is_available(self) -> bool:
        """Check if ChatGPT service is available"""
        try:
            api_key = os.environ.get("OPENAI_API_KEY")
            return bool(api_key and OpenAI)
        except:
            return False


# Example usage
if __name__ == "__main__":
    # Test the skill
    skill = ChatGPTSkill()
    response = skill.query("What is MyOperator?")
    print(response)
