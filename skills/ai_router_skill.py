"""
AI Router Skill - Intelligent routing to ChatGPT, Gemini, or Perplexity
Routes queries to the most suitable AI model based on query type
"""
import logging
import re
from typing import Dict, Any, Optional

# Import all AI skills
from skills.chatgpt_skill import ChatGPTSkill
from skills.gemini_skill import GeminiSkill
from skills.perplexity_skill import PerplexitySkill

logger = logging.getLogger(__name__)

class AIRouterSkill:
    """
    Intelligent AI router that selects the best model for each query
    - Research/Current Info → Perplexity (real-time web search)
    - Conversation/Help → ChatGPT (conversational AI)
    - Default/General → Gemini (balanced performance)
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize AI Router with all three AI models
        """
        self.config = config
        
        # Initialize all AI skills
        try:
            self.chatgpt = ChatGPTSkill(config)
            logger.info("ChatGPT skill initialized")
        except Exception as e:
            logger.warning(f"ChatGPT skill not available: {e}")
            self.chatgpt = None
            
        try:
            self.gemini = GeminiSkill(config)
            logger.info("Gemini skill initialized")
        except Exception as e:
            logger.warning(f"Gemini skill not available: {e}")
            self.gemini = None
            
        try:
            self.perplexity = PerplexitySkill(config)
            logger.info("Perplexity skill initialized")
        except Exception as e:
            logger.warning(f"Perplexity skill not available: {e}")
            self.perplexity = None
        
        # Research query keywords
        self.research_keywords = [
            'what is', 'who is', 'when did', 'where is', 'latest', 'current',
            'news', 'update', 'recent', 'today', 'now', 'find', 'search',
            'happening', 'price of', 'stock', 'weather', 'score'
        ]
        
        # Conversation query keywords
        self.conversation_keywords = [
            'help', 'how to', 'how do', 'explain', 'guide', 'tutorial',
            'teach', 'tell me about', 'can you', 'could you', 'please',
            'advice', 'recommend', 'suggest', 'think', 'opinion'
        ]
    
    def classify_query(self, message: str) -> str:
        """
        Classify the query type based on content
        Returns: 'research', 'conversation', or 'general'
        """
        message_lower = message.lower()
        
        # Check for research keywords
        for keyword in self.research_keywords:
            if keyword in message_lower:
                logger.info(f"Query classified as 'research' (keyword: {keyword})")
                return 'research'
        
        # Check for conversation keywords
        for keyword in self.conversation_keywords:
            if keyword in message_lower:
                logger.info(f"Query classified as 'conversation' (keyword: {keyword})")
                return 'conversation'
        
        # Default to general
        logger.info("Query classified as 'general'")
        return 'general'
    
    def route_query(self, message: str, context: Dict[str, Any]) -> Optional[str]:
        """
        Route the query to the most appropriate AI model
        Implements fallback strategy if primary model is unavailable
        """
        query_type = self.classify_query(message)
        
        # Route based on query type with fallbacks
        if query_type == 'research':
            # Research → Perplexity > ChatGPT > Gemini
            models = [
                ('Perplexity', self.perplexity),
                ('ChatGPT', self.chatgpt),
                ('Gemini', self.gemini)
            ]
        elif query_type == 'conversation':
            # Conversation → ChatGPT > Gemini > Perplexity
            models = [
                ('ChatGPT', self.chatgpt),
                ('Gemini', self.gemini),
                ('Perplexity', self.perplexity)
            ]
        else:
            # General → Gemini > ChatGPT > Perplexity
            models = [
                ('Gemini', self.gemini),
                ('ChatGPT', self.chatgpt),
                ('Perplexity', self.perplexity)
            ]
        
        # Try each model in priority order
        for model_name, model in models:
            if model is None:
                logger.debug(f"{model_name} not available, trying next")
                continue
                
            try:
                logger.info(f"Routing query to {model_name}")
                response = model.generate_response(message, context)
                if response:
                    logger.info(f"Successfully got response from {model_name}")
                    return f"[{model_name}] {response}"
            except Exception as e:
                logger.error(f"Error with {model_name}: {e}")
                continue
        
        # All models failed
        logger.error("All AI models failed to respond")
        return "I apologize, but I'm having trouble connecting to my AI services right now. Please try again in a moment."
    
    def generate_response(self, message: str, context: Dict[str, Any]) -> str:
        """
        Main entry point for generating AI responses
        """
        try:
            return self.route_query(message, context)
        except Exception as e:
            logger.error(f"Error in AI router: {e}")
            return "I encountered an error processing your request. Please try rephrasing your question."
