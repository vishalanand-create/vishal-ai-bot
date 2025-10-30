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
            
            # Agentic processing
            for skill in self.skills:
                result = skill(message, self.memory)
                if result is not None:
                    logger.info(f"Skill returned result: {result[:50]}..." if len(result) > 50 else f"Skill returned result: {result}")
                    return result
            
            logger.warning(f"No skill could handle message: {message}")
            return f"{self.name} could not understand your request."
        except Exception as e:
            logger.error(f"Error processing message: {message}. Error: {str(e)}", exc_info=True)
            return f"Sorry, an error occurred while processing your request."

# Sample skills
def greet_skill(message, memory):
    # Accept simple greetings like hi, hello, hey, etc.
    greetings = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"]
    if any(greeting in message.lower() for greeting in greetings):
        return "Hello! How can I assist you today?"

def faq_skill(message, memory):
    if "faq" in message.lower():
        return "Check out our FAQ at example.com/faq"

def about_me_skill(message, memory):
    msg_lower = message.lower()
    # Check for exact phrase matches (case-insensitive)
    phrases = [
        'who are you',
        'what is your name',
        'your name',
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
        'what\'s your skill',
        'what are your skills',
        'your skills',
        'abilities',
        'what can you do',
        'what are you good at',
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

def report_skill(message, memory):
    if "report" in message.lower():
        return "Generating report for you..."

# Main entry point
if __name__ == "__main__":
    bot = AgenticAIBot()
    print(bot.receive_message("Hello"))
    print(bot.receive_message("Tell me about yourself"))
    print(bot.receive_message("Show me analytics"))
