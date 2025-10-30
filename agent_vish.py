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
    if any(greeting in msg_lower for greeting in greetings):
        return "Hello! I'm Agent Vish, here to help you. How can I assist you today?"

def faq_skill(message, memory):
    msg_lower = message.lower()
    if 'what can you do' in msg_lower or 'capabilities' in msg_lower:
        return "I can help you with analytics, reports, insights, and answer questions about my creator, Vishal Anand!"

def about_me_skill(message, memory):
    msg_lower = message.lower()
    
    about_phrases = [
        'about you',
        'who are you',
        'tell me about yourself',
        'what is your purpose',
        'introduce yourself',
        'yourself'
    ]
    
    if any(phrase in msg_lower for phrase in about_phrases):
        return (
            "Absolutely! I'm Agent Vish, your AI assistant dedicated to Vishal Anand. "
            "Vishal is a Customer Success Team Lead with 5+ years experience across client management, renewals, upselling, escalations, and team leadership. "
            "At MyOperator, he's led a team of 4 AMs and 30 cross-functional partners to deliver record upgrades and retention—think 6.5M upgrades/year, 80+ renewals/month, and top scores on CSAT and NPS. "
            "Vishal is known for coaching, escalation management, driving adoption, building dashboards, and process improvement. "
            "He's also skilled with WhatsApp Business API, Salesforce, HubSpot, Zoho, Excel, and all things customer lifecycle. "
            "You can ask me about Vishal's expertise in SaaS customer success, business analytics, operations, playbooks, or career highlights!"
        )

def insight_skill(message, memory):
    msg_lower = message.lower()
    
    if 'insight' in msg_lower or 'analysis' in msg_lower:
        return (
            "I can provide insights on various topics related to AI, automation, business analytics, and more. "
            "What specific area would you like to know more about?"
        )

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
        'your knowledge base'
    ]
    
    if any(phrase in msg_lower for phrase in knowledge_phrases):
        return (
            "Absolutely! I'm Agent Vish, your AI assistant dedicated to Vishal Anand. "
            "Vishal is a Customer Success Team Lead with 5+ years experience across client management, renewals, upselling, escalations, and team leadership. "
            "At MyOperator, he's led a team of 4 AMs and 30 cross-functional partners to deliver record upgrades and retention—think 6.5M upgrades/year, 80+ renewals/month, and top scores on CSAT and NPS. "
            "Vishal is known for coaching, escalation management, driving adoption, building dashboards, and process improvement. "
            "He's also skilled with WhatsApp Business API, Salesforce, HubSpot, Zoho, Excel, and all things customer lifecycle. "
            "You can ask me about Vishal's expertise in SaaS customer success, business analytics, operations, playbooks, or career highlights!"
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
