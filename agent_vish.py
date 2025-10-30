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

BIO = (
    "I'm Agent Vish, the AI assistant for Vishal Anand — a product-focused AI/ML engineer "
    "with strengths in LLM apps, agentic workflows, data engineering, and pragmatic delivery."
)

SKILLS = (
    "Core skills: LLM apps, RAG/agents, prompt engineering, Python, FastAPI/Flask, vector DBs, "
    "GenAI evals, analytics, dashboards, systems thinking, and stakeholder communication."
)

def greet_skill(message: str, memory: dict) -> str | None:
    msg = message.lower()
    if any(k in msg for k in ["hello", "hi", "hey", "start", "get started", "help"]):
        return (
            "Hi, I'm Agent Vish. Ask about Vishal, skills, projects, or features."
        )
    return None

FAQ_TRIGGERS = [
    "pricing", "contact", "email", "website", "portfolio", "projects", "case studies",
    "features", "capabilities", "what can you do", "how it works"
]

def faq_skill(message: str, memory: dict) -> str | None:
    msg = message.lower()
    if any(k in msg for k in FAQ_TRIGGERS):
        return (
            "Quick answers: About Vishal, skills, projects, and how this bot works. "
            "Ask: 'about vishal', 'core skills', 'projects', or 'features'."
        )
    return None

ABOUT_TRIGGERS = [
    "about vishal", "about you", "who is vishal", "who are you", "profile", "bio"
]

SKILL_TRIGGERS = [
    "core skills", "key skills", "core competencies", "competencies", "skills", "strengths",
    "expertise", "what are your skills", "your skills"
]

QUICK_REPLY_TARGETS = [
    "about", "skills", "projects", "features", "contact", "help"
]

def about_me_skill(message: str, memory: dict) -> str | None:
    msg = message.lower()
    if any(k in msg for k in ABOUT_TRIGGERS) or any(k == msg.strip() for k in QUICK_REPLY_TARGETS if k in ["about"]):
        return BIO
    if any(k in msg for k in SKILL_TRIGGERS) or msg.strip() in ["skills", "core skills", "competencies"]:
        return SKILLS
    return None

def insight_skill(message: str, memory: dict) -> str | None:
    return None

def report_skill(message: str, memory: dict) -> str | None:
    return None

def knowledge_skill(message: str, memory: dict) -> str | None:
    return None

def upsell_skill(message: str, memory: dict) -> str | None:
    return None

class AgenticAIBot:
    def __init__(self, name: str = "Agent Vish"):
        self.name = name
        self.skills: List[Callable[[str, dict], str | None]] = []
        self.memory = {}

        # Register core skills
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

    def add_skill(self, skill_fn: Callable[[str, dict], str | None]):
        self.skills.append(skill_fn)

    def receive_message(self, message: str) -> str:
        try:
            msg = clean_text(message)
            logger.info("Received message: %s", msg)

            # Route to skills
            for skill in self.skills:
                try:
                    resp = skill(msg, self.memory)
                    if resp:
                        logger.info("Skill matched. Response: %s", resp[:120] + ("..." if len(resp) > 120 else ""))
                        return resp
                except Exception as e:
                    logger.exception("Skill error: %s", e)
                    continue

            # Default responses for common intents
            if any(k in msg for k in SKILL_TRIGGERS):
                return SKILLS
            if any(k in msg for k in ABOUT_TRIGGERS):
                return BIO
            if msg in QUICK_REPLY_TARGETS:
                if msg == "skills":
                    return SKILLS
                if msg == "about":
                    return BIO

            return (
                "I'm not sure how to respond to that. Try asking about Vishal, skills, projects, or features."
            )
        except Exception as e:
            logger.exception("Agent error: %s", e)
            return "Sorry, something went wrong. Please try again."
