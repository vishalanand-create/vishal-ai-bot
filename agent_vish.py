# agent_vish.py
import logging
from skills.analytics_skill import analytics_skill

# Configure logging
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AgenticAIBot:
    def __init__(self, name="Agent Vish"):
        self.name = name
        self.skills = []
        self.memory = {}
        
        # Always register core skills so they're available for API/backends
        self.add_skill(greet_skill)
        self.add_skill(faq_skill)
        self.add_skill(about_me_skill)
        self.add_skill(insight_skill)
        self.add_skill(report_skill)
        self.add_skill(knowledge_skill)
        self.add_skill(upsell_skill)
        
        # Wrap analytics_skill to match (message, memory) signature
        self.add_skill(lambda msg, mem: analytics_skill(msg))
        
        logger.info(f"{self.name} initialized with {len(self.skills)} skills")
    
    def add_skill(self, skill_fn):
        self.skills.append(skill_fn)
    
    def receive_message(self, message):
        try:
            # Accept any non-empty string as valid input
            if not message or not isinstance(message, str) or not message.strip():
                return "Please provide a valid message."
            
            logger.info(f"Received message: {message}")
            
            # Try each skill in sequence
            for skill in self.skills:
                response = skill(message, self.memory)
                if response:
                    logger.info(f"Skill matched. Response: {response[:50]}...")
                    return response
            
            return "I'm not sure how to respond to that. Try asking about my skills or analytics!"
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return "Sorry, I encountered an error processing your message."

def greet_skill(message, memory):
    msg_lower = message.lower()
    greetings = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']
    
    if any(greet in msg_lower for greet in greetings):
        return "Hello! I'm Agent Vish. How can I assist you today?"

def faq_skill(message, memory):
    msg_lower = message.lower()
    
    if 'help' in msg_lower or 'faq' in msg_lower or 'question' in msg_lower:
        return "Here are some things I can help with: greetings, analytics, reports, and general questions!"

def about_me_skill(message, memory):
    msg_lower = message.lower()
    
    phrases = [
        'who are you',
        'what are you',
        'tell me about you',
        'about you',
        'introduce yourself',
        'name please',
        'who r u'
    ]
    
    if any(phrase in msg_lower for phrase in phrases):
        return "I am Agent Vish, your AI assistant."
    
    # Fallback to substring match for 'about'
    if 'about' in msg_lower:
        return "I am Agent Vish, your AI assistant."

def insight_skill(message, memory):
    msg_lower = message.lower()
    
    # Check for natural language variations asking about skills/capabilities
    skill_phrases = [
        'skill',
        'skills',
        "what's your skill",
        'what are your skills',
        'your skills',
        'abilities',
        'what can you do',
        'what are you good at',
        'capabilities',
        'your capabilities',
        'what do you do',
        'tell me your skills',
        'list your skills',
        'what are your abilities',
        'show me your skills',
        'your capability',
        'what can you help with',
        'what do you know',
        'insight'
    ]
    
    if any(phrase in msg_lower for phrase in skill_phrases):
        return (
            "I'm Agent Vish, and here's what I can do for you:\n"
            "✨ Greet and chat with you\n"
            "📊 Provide analytics and insights\n"
            "📝 Generate reports\n"
            "❓ Answer FAQs\n"
            "💬 Have natural conversations\n"
            "Feel free to ask me anything!"
        )

def knowledge_skill(message, memory):
    msg_lower = message.lower()
    
    knowledge_phrases = [
        'what all you know',
        'what do you know',
        'knowledge',
        'your expertise',
        'what is your knowledge',
        'tell me what you know',
        'your knowledge base'
    ]
    
    if any(phrase in msg_lower for phrase in knowledge_phrases):
        return (
            "I have expertise in:\n"
            "🤖 Conversational AI and natural language understanding\n"
            "📈 Analytics and data insights\n"
            "📊 Report generation and summarization\n"
            "💼 Business automation and workflow assistance\n"
            "🔍 Information retrieval and FAQ handling\n"
            "I'm continuously learning to serve you better!"
        )

def upsell_skill(message, memory):
    msg_lower = message.lower()
    
    upsell_phrases = [
        'how do you upsell',
        'upsell',
        'upselling',
        'cross-sell',
        'upgrade',
        'premium features'
    ]
    
    if any(phrase in msg_lower for phrase in upsell_phrases):
        return (
            "Great question! Here's how I can help with upselling:\n"
            "💎 Identify customer needs and recommend premium features\n"
            "📊 Analyze usage patterns to suggest relevant upgrades\n"
            "🎯 Personalize upgrade recommendations based on user behavior\n"
            "📈 Highlight value propositions and ROI of premium tiers\n"
            "💬 Engage customers with targeted messaging at the right time\n"
            "Let me know if you'd like to explore specific upselling strategies!"
        )

def report_skill(message, memory):
    if "report" in message.lower():
        return "Generating report for you..."

# Main entry point
if __name__ == "__main__":
    bot = AgenticAIBot()
    print(bot.receive_message("Hello"))
    print(bot.receive_message("Tell me about yourself"))
    print(bot.receive_message("Show me analytics"))
