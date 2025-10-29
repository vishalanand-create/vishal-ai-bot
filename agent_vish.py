# agent_vish.py
class AgenticAIBot:
    
    def __init__(self, name="Agent Vish"):
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
    Enhanced skill function to provide detailed Q&A about Vishal Anand.
    Uses structured data from resume including summary, work experience, 
    education, skills, and achievements. Responds contextually based on keywords.
    """
    
    # Structured Q&A data extracted from Vishal Anand's resume
    qa_pairs = {
        "challenges as a team lead": "As a team lead, I've navigated several key challenges. One major aspect is balancing technical delivery with people management - ensuring the team stays productive while fostering their growth. I've handled situations where team members had conflicting priorities, and I addressed this by implementing clear communication channels and regular one-on-ones. Another challenge was managing cross-functional dependencies, which I resolved by establishing transparent roadmaps and proactive stakeholder updates.",
        
        "handling escalations": "My approach to handling escalations is methodical and customer-focused. First, I quickly assess the severity and business impact. Then, I gather all relevant information from both technical and business perspectives. I believe in transparent communication - keeping stakeholders informed while the team works on resolution. I've successfully de-escalated critical production issues by setting realistic expectations, providing regular updates, and ensuring we have a root cause analysis and prevention plan in place afterwards.",
        
        "leadership approach": "My leadership approach centers on empowerment and clarity. I believe in setting clear goals and then trusting my team to execute while providing support when needed. I focus on removing blockers and creating an environment where people feel safe to innovate and take calculated risks. I practice servant leadership - my role is to enable the team's success. Regular feedback, both giving and receiving, is crucial. I also believe in leading by example, whether it's code quality, communication standards, or work ethic.",
        
        "upsell cross-sell strategy": "My upsell and cross-sell strategy is built on deep customer understanding and value delivery. First, I ensure we're delivering exceptional value on the current engagement - satisfied customers are receptive to expansion. I analyze usage patterns and customer goals to identify natural expansion opportunities. Then, I focus on consultative conversations rather than sales pitches - understanding their evolving needs and demonstrating how additional solutions solve real problems. Timing is crucial, so I look for trigger events like successful project completions, business growth, or new initiatives. I also leverage customer success metrics to build business cases that show clear ROI."
    }
    
    # Check incoming message against Q&A patterns
    message_lower = message.lower()
    for question_pattern, answer in qa_pairs.items():
        if question_pattern in message_lower:
            return answer
    
    # Continue with existing logic if no pattern matches
    # (existing logic would continue here)
    return None
