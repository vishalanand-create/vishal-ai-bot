# agent_vish.py
import logging
import re
from typing import Callable, List
from skills.analytics_skill import analytics_skill

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CLEAN_PATTERN = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]")

def clean_text(s: str) -> str:
    if not isinstance(s, str):
        return ""
    return CLEAN_PATTERN.sub("", s).strip()

# Core content constants
BIO = (
    "I'm Agent Vish, the AI assistant for Vishal Anand — a product-focused AI/ML engineer "
    "with strengths in LLM apps, agentic workflows, data engineering, and pragmatic delivery."
)

SKILLS = (
    "Core skills: LLM apps, RAG/agents, prompt engineering, Python, FastAPI/Flask, vector DBs, "
    "GenAI evals, analytics, dashboards, systems thinking, and stakeholder communication."
)

PROJECTS = (
    "Vishal has built Agent Vish (this chatbot!), RAG pipelines, analytics dashboards, "
    "and agentic workflows. Ask about 'features' to learn more about this bot's capabilities."
)

FEATURES = (
    "This bot answers FAQs, provides insights about Vishal, and demonstrates agentic AI patterns. "
    "It uses skill-based routing and contextual memory. Try asking: 'about vishal', 'core skills', or 'projects'."
)

HELP_TEXT = (
    "Hi! I'm Agent Vish. Try these: 'about vishal', 'core skills', 'projects', 'features', or ask me anything!"
)

# Greeting skill
def greet_skill(message: str, memory: dict) -> str | None:
    msg = message.lower()
    if any(k in msg for k in ["hello", "hi", "hey", "start", "get started"]):
        return "Hi, I'm Agent Vish. Ask about Vishal, skills, projects, or features."
    return None

# FAQ skill with comprehensive triggers
FAQ_TRIGGERS = [
    "pricing", "contact", "email", "website", "portfolio", "case studies",
    "capabilities", "what can you do", "how it works"
]

def faq_skill(message: str, memory: dict) -> str | None:
    msg = message.lower()
    if any(k in msg for k in FAQ_TRIGGERS):
        return (
            "Quick answers: About Vishal, skills, projects, and how this bot works. "
            "Ask: 'about vishal', 'core skills', 'projects', or 'features'."
        )
    return None

# About/Bio skill with comprehensive triggers
ABOUT_TRIGGERS = [
    "about vishal", "about you", "who is vishal", "who are you", 
    "profile", "bio", "background", "tell me about"
]

def about_me_skill(message: str, memory: dict) -> str | None:
    msg = message.lower()
    # Handle explicit quick reply buttons
    if msg in ["about", "about vishal"]:
        return BIO
    # Handle natural language variations
    if any(trigger in msg for trigger in ABOUT_TRIGGERS):
        return BIO
    return None

# Skills skill with comprehensive triggers
SKILL_TRIGGERS = [
    "core skills", "key skills", "core competencies", "competencies", 
    "skills", "strengths", "expertise", "what are your skills", "your skills",
    "technical skills", "capabilities"
]

def skills_skill(message: str, memory: dict) -> str | None:
    msg = message.lower()
    # Handle explicit quick reply button
    if msg in ["skills", "core skills"]:
        return SKILLS
    # Handle natural language variations
    if any(trigger in msg for trigger in SKILL_TRIGGERS):
        return SKILLS
    return None

# Projects skill with comprehensive triggers
PROJECT_TRIGGERS = [
    "projects", "work", "portfolio", "case studies", "what have you built",
    "show me projects", "examples"
]

def projects_skill(message: str, memory: dict) -> str | None:
    msg = message.lower()
    # Handle explicit quick reply button
    if msg == "projects":
        return PROJECTS
    # Handle natural language variations
    if any(trigger in msg for trigger in PROJECT_TRIGGERS):
        return PROJECTS
    return None

# Features skill with comprehensive triggers
FEATURE_TRIGGERS = [
    "features", "capabilities", "what can you do", "bot features",
    "how does this work", "functionality"
]

def features_skill(message: str, memory: dict) -> str | None:
    msg = message.lower()
    # Handle explicit quick reply button
    if msg == "features":
        return FEATURES
    # Handle natural language variations
    if any(trigger in msg for trigger in FEATURE_TRIGGERS):
        return FEATURES
    return None

# Help skill
HELP_TRIGGERS = ["help", "what can i ask", "options", "menu"]

def help_skill(message: str, memory: dict) -> str | None:
    msg = message.lower()
    if msg == "help" or any(trigger in msg for trigger in HELP_TRIGGERS):
        return HELP_TEXT
    return None

# Insight skill placeholder
def insight_skill(message: str, memory: dict) -> str | None:
    msg = message.lower()
    if any(k in msg for k in ["insight", "analysis", "data", "metrics"]):
        return "Insights coming soon! For now, try asking about Vishal's skills or projects."
    return None

# Report skill placeholder
def report_skill(message: str, memory: dict) -> str | None:
    msg = message.lower()
    if "report" in msg:
        return "Reports coming soon! For now, try asking about Vishal's skills or projects."
    return None

# Knowledge skill placeholder
def knowledge_skill(message: str, memory: dict) -> str | None:
    msg = message.lower()
    if "knowledge" in msg or "learn" in msg:
        return "Knowledge base coming soon! For now, try asking about Vishal's skills or projects."
    return None

# Upsell skill placeholder
def upsell_skill(message: str, memory: dict) -> str | None:
    msg = message.lower()
    if any(k in msg for k in ["hire", "work with", "collaborate", "consulting"]):
        return "Interested in working with Vishal? Ask about his 'core skills' and 'projects' to learn more!"
    return None

# Main Agent class
class AgenticAIBot:
    def __init__(self, name: str = "Agent Vish"):
        self.name = name
        self.skills: List[Callable[[str, dict], str | None]] = []
        self.memory = {}
        
        # Register core skills in priority order
        # Quick reply handlers first for exact matches
        self.add_skill(help_skill)
        self.add_skill(greet_skill)
        self.add_skill(about_me_skill)
        self.add_skill(skills_skill)
        self.add_skill(projects_skill)
        self.add_skill(features_skill)
        self.add_skill(faq_skill)
        # Then advanced skills
        self.add_skill(insight_skill)
        self.add_skill(report_skill)
        self.add_skill(knowledge_skill)
        self.add_skill(upsell_skill)
        # Wrap analytics_skill to match (message, memory) signature
        self.add_skill(lambda msg, mem: analytics_skill(msg))
        
        logger.info(f"{self.name} initialized with {len(self.skills)} skills")

    def add_skill(self, skill_fn: Callable[[str, dict], str | None]):
        self.skills.append(skill_fn)

    def receive_message(self, message: str) -> str:
        try:
            msg = clean_text(message)
            logger.info("Received message: %s", msg)
            
            # Route to skills in priority order
            for skill in self.skills:
                try:
                    resp = skill(msg, self.memory)
                    if resp:
                        logger.info("Skill matched. Response: %s", resp[:120] + ("..." if len(resp) > 120 else ""))
                        return resp
                except Exception as e:
                    logger.exception("Skill error: %s", e)
                    continue
            
            # Final fallback for unmatched queries
            return (
                "I'm not sure how to respond to that. Try asking about Vishal, skills, projects, or features. "
                "Or type 'help' for suggestions!"
            )
        except Exception as e:
            logger.exception("Agent error: %s", e)
            return "Sorry, something went wrong. Please try again."
