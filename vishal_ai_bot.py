# vishal_ai_bot.py
class AgenticAIBot:
    def __init__(self, name="Vishal AI Bot"):
        self.name = name
        self.skills = []
        self.memory = {}

    def add_skill(self, skill_fn):
        self.skills.append(skill_fn)

    def receive_message(self, message):
        # Agentic processing
        for skill in self.skills:
            result = skill(message, self.memory)
            if result is not None:
                return result
        return f"{self.name} could not understand your request."

# Sample skills
def greet_skill(message, memory):
    if "hello" in message.lower():
        return "Hello! How can I assist you today?"

def faq_skill(message, memory):
    if "what is agentic ai" in message.lower():
        return "Agentic AI refers to autonomous, goal-directed AI systems that can perform tasks and learn independently."

def about_me_skill(message, memory):
    """
    Skill function to provide comprehensive professional summary about Vishal Anand.
    Triggers when user asks about 'Vishal Anand' or 'me'.
    """
    message_lower = message.lower()
    if "vishal anand" in message_lower or ("about" in message_lower and "me" in message_lower) or "who is vishal" in message_lower:
        return """Vishal Anand - Professional Summary:

Vishal Anand is an accomplished technology professional with expertise in AI, machine learning, and software development. 
He specializes in building agentic AI systems and intelligent automation solutions. 

Key Areas of Expertise:
- Agentic AI and Autonomous Systems
- Machine Learning and Deep Learning
- Software Engineering and Architecture
- Python Development and Automation
- AI Bot Development and Deployment

Vishal is passionate about creating innovative AI solutions that can autonomously perform complex tasks, 
learn from interactions, and provide intelligent assistance. His work focuses on pushing the boundaries 
of what's possible with artificial intelligence while maintaining practical, real-world applications.

Professional Philosophy:
Vishal believes in building AI systems that are not just reactive but proactive - systems that can 
understand context, make decisions, and take actions to achieve goals independently. His approach 
combines technical excellence with user-centric design to create AI solutions that truly make a difference."""
    return None

# Usage example
if __name__ == "__main__":
    bot = AgenticAIBot()
    bot.add_skill(greet_skill)
    bot.add_skill(faq_skill)
    bot.add_skill(about_me_skill)  # Register the new about_me_skill
    
    print(bot.receive_message("Hello!"))  # Outputs greeting
    print(bot.receive_message("What is agentic AI?"))  # Outputs FAQ response
    print(bot.receive_message("Tell me about Vishal Anand"))  # Outputs professional summary
