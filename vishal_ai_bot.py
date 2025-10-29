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

# Usage example
if __name__ == "__main__":
    bot = AgenticAIBot()
    bot.add_skill(greet_skill)
    bot.add_skill(faq_skill)
    
    print(bot.receive_message("Hello!"))  # Outputs greeting
    print(bot.receive_message("What is agentic AI?"))  # Outputs FAQ response
