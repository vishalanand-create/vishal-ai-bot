"""Perplexity AI Pro Integration Skill for Agent Vish

Provides Perplexity AI Pro integration with real-time web search.
"""

import os
import logging
import requests
from typing import Optional, List, Dict

logger = logging.getLogger(__name__)


class PerplexitySkill:
    """Skill for querying Perplexity AI with web search capabilities"""
    
    def __init__(self):
        """Initialize Perplexity skill with API key"""
        api_key = os.environ.get("PERPLEXITY_API_KEY")
        if not api_key:
            raise ValueError("PERPLEXITY_API_KEY environment variable not set")
        
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai/chat/completions"
        # Use sonar-pro for your Pro subscription
        self.model = os.environ.get("PERPLEXITY_MODEL", "sonar-pro")
        
        logger.info(f"Perplexity skill initialized with model: {self.model}")
    
    def query(self, user_message: str, context: Optional[List[Dict]] = None) -> str:
        """Query Perplexity AI with user message
        
        Args:
            user_message: The user's message/question
            context: Optional conversation history
            
        Returns:
            AI-generated response string
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            messages = [
                {
                    "role": "system",
                    "content": """You are Agent Vish, MyOperator's AI assistant.
                    
Your role:
- Provide accurate, factual information
- Use web search for current information
- Be professional and helpful
- Cite sources when possible

Critical Rules:
- If you don't know something, say so clearly
- Never make up information
- Always prioritize accuracy"""
                }
            ]
            
            # Add context if provided
            if context:
                messages.extend(context[-3:])
            
            # Add user message
            messages.append({"role": "user", "content": user_message})
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.2,  # Lower for more factual responses
                "max_tokens": 1000
            }
            
            logger.info(f"Querying Perplexity: {user_message[:50]}...")
            
            response = requests.post(self.base_url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                answer = response.json()["choices"][0]["message"]["content"]
                logger.info(f"Perplexity response: {answer[:50]}...")
                return answer
            else:
                logger.error(f"Perplexity API error: {response.status_code} - {response.text}")
                return "I'm having trouble accessing real-time information. Please try again."
                
        except requests.Timeout:
            logger.error("Perplexity API timeout")
            return "The search is taking too long. Please try a simpler query."
        except Exception as e:
            logger.error(f"Perplexity query failed: {e}")
            return "I'm having trouble processing that right now. Please try again."
    
    def is_available(self) -> bool:
        """Check if Perplexity service is available"""
        try:
            api_key = os.environ.get("PERPLEXITY_API_KEY")
            return bool(api_key)
        except:
            return False


# Example usage
if __name__ == "__main__":
    skill = PerplexitySkill()
    response = skill.query("What are the latest features in MyOperator?")
    print(response)
