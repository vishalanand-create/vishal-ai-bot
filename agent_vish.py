# agent_vish.py
import logging
import re
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
    
    greet_phrases = [
        'hi', 'hello', 'hey', 'greetings', 'good morning', 
        'good afternoon', 'good evening', 'namaste', 'hola'
    ]
    
    if any(phrase in msg_lower for phrase in greet_phrases):
        return "Hello! I'm Agent Vish, here to help you. How can I assist you today?"

def faq_skill(message, memory):
    msg_lower = message.lower()
    
    faqs = {
        'what is your name': "Hey there! I'm Agent Vish, your personal AI assistant created for Vishal Anand. I'm here to share insights about Vishal's expertise in Customer Success, team leadership, client management, and SaaS operations. Whether you want to know about his renewals strategy, upselling approach, API integrations, reporting skills, or client wins—just ask! I can also help with analytics and business insights. How can I assist you today?",
        'who are you': "I'm Agent Vish, an AI assistant representing Vishal Anand—a Customer Success Team Lead with expertise in renewals, upselling, onboarding, analytics, and SaaS operations.",
        'how can you help': "I can share information about Vishal Anand's professional background, skills, client wins, and projects. I can also help with analytics and insights!"
    }
    
    for question, answer in faqs.items():
        if question in msg_lower:
            return answer

def about_me_skill(message, memory):
    msg_lower = message.lower()
    
    about_phrases = [
        'who is vishal anand',
        'tell me about vishal',
        'tell more about vishal',
        'more about him',
        'more about vishal',
        'about vishal',
        'what are his skills',
        'his skills',
        'vishal skills',
        'tell more about him'
    ]
    
    if any(phrase in msg_lower for phrase in about_phrases):
        return (
            "I'm Agent Vish, the AI assistant for Vishal Anand—a Customer Success Team Lead at MyOperator, skilled in renewals, upselling, onboarding, APIs, analytics, and SaaS operations.\n\n"
            "Here are Vishal's key skills: client lifecycle management, coaching, escalation handling, reporting, process improvement, automation, and tools like Salesforce, HubSpot, WhatsApp Business API, Zoho, and Excel. Want details about a specific project, client win, or tool? Just ask!"
        )

def insight_skill(message, memory):
    if 'insight' in message.lower():
        return "Here's an insight: Focus on customer value and retention!"

def report_skill(message, memory):
    if "report" in message.lower():
        return "Generating report for you..."

def knowledge_skill(message, memory):
    msg_lower = message.lower()
    
    knowledge_phrases = [
        'what all you know',
        'what do you know',
        'knowledge',
        'your expertise',
        'what is your knowledge',
        'tell me what you know',
        'your knowledge base',
        'know',
        'expertise'
    ]
    
    if any(phrase in msg_lower for phrase in knowledge_phrases):
        return (
            "I'm Agent Vish, the AI assistant for Vishal Anand—a Customer Success Team Lead at MyOperator, skilled in renewals, upselling, onboarding, APIs, analytics, and SaaS operations. "
            "Vishal leads teams, drives process improvement, and is skilled in client lifecycle management, reporting, automation, and tools like Salesforce, HubSpot, WhatsApp Business API, Zoho, and Excel. "
            "Want to know about Vishal's client wins, team leadership, performance coaching, or career insights? Just ask!"
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

# Main entry point
if __name__ == "__main__":
    bot = AgenticAIBot()
    print(bot.receive_message("Hello"))
    print(bot.receive_message("Tell me about yourself"))
    print(bot.receive_message("Show me analytics"))
