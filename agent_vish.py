# agent_vish.py
import logging
from skills.analytics_skill import analytics_skill

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
    if "hello" in message.lower():
        return "Hello! How can I assist you today?"

def faq_skill(message, memory):
    if "faq" in message.lower():
        return "Check out our FAQ at example.com/faq"

def about_me_skill(message, memory):
    if "about" in message.lower():
        return "I am Agent Vish, your AI assistant."

def insight_skill(message, memory):
    if "insight" in message.lower():
        return "Here are some insights based on your data..."

def report_skill(message, memory):
    if "report" in message.lower():
        return "Generating report for you..."

# Main entry point
if __name__ == "__main__":
    bot = AgenticAIBot()
    print(bot.receive_message("Hello"))
    print(bot.receive_message("Tell me about yourself"))
    print(bot.receive_message("Show me analytics"))
