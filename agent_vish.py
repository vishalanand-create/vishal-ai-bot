# agent_vish.py
import logging
import re
from typing import Callable, List, Dict, Any, Tuple
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

# ============ Quality Filters (System-level) ============
MODERATION_BADWORDS = {
    # minimal placeholder rules; extend as needed
    "hate speech": ["hate", "racist", "nazi"],
    "violence": ["kill", "murder", "shoot"],
    "sexual": ["explicit", "porn"],
}

KNOWN_FACTS = {
    "name": "Vishal Anand",
    "assistant": "Agent Vish",
    "skills_keywords": [
        "LLM", "RAG", "agents", "Python", "FastAPI", "Flask", "vector", "GenAI", "analytics", "dashboards"
    ],
    "projects_keywords": ["Agent Vish", "RAG", "dashboards", "agentic workflows"],
}

def hallucination_check(answer: str, user_query: str) -> Tuple[bool, float, str]:
    a = answer.lower()
    # Rule 1: wild claims without any known keywords for this bot's domain
    domain_hits = sum(1 for k in KNOWN_FACTS["skills_keywords"] if k.lower() in a)
    project_hits = sum(1 for k in KNOWN_FACTS["projects_keywords"] if k.lower() in a)
    # Heuristic: if it mentions external concrete facts (years, amounts) without context, flag
    has_numbers = bool(re.search(r"\b\d{2,}\b", a))
    score = 0.7 + 0.1 * (domain_hits > 0) + 0.1 * (project_hits > 0) - (0.2 if has_numbers and domain_hits == 0 else 0)
    ok = score >= 0.7
    reason = "ok" if ok else "possible unsupported specifics"
    return ok, max(min(score, 1.0), 0.0), reason

def moderation_check(answer: str) -> Tuple[bool, float, str]:
    a = answer.lower()
    hits: Dict[str, list[str]] = {}
    for cat, words in MODERATION_BADWORDS.items():
        found = [w for w in words if w in a]
        if found:
            hits[cat] = found
    ok = len(hits) == 0
    score = 1.0 if ok else 0.0
    reason = "ok" if ok else f"flags: {hits}"
    return ok, score, reason

def answer_relevance(user_query: str, answer: str) -> Tuple[bool, float, str]:
    q = user_query.lower()
    a = answer.lower()
    # simple substring overlap heuristic
    tokens_q = set(re.findall(r"\w+", q))
    tokens_a = set(re.findall(r"\w+", a))
    overlap = len(tokens_q & tokens_a)
    score = overlap / max(1, len(tokens_q))
    ok = score >= 0.2 or any(t in a for t in tokens_q)
    return ok, min(max(score, 0.0), 1.0), f"overlap={overlap}"

def context_recall(memory: Dict[str, Any], answer: str) -> Tuple[bool, float, str]:
    # Does the answer reference any memory or background constants
    a = answer.lower()
    recall_hits = 0
    for key in [KNOWN_FACTS["name"], KNOWN_FACTS["assistant"]]:
        recall_hits += 1 if key.lower() in a else 0
    score = 0.5 + 0.25 * (recall_hits > 0)
    return score >= 0.5, min(score, 1.0), f"hits={recall_hits}"

def context_precision(answer: str) -> Tuple[bool, float, str]:
    a = answer.lower()
    # verify certain details are not contradicted
    ok_name = (KNOWN_FACTS["name"].lower() in a) or ("vishal" in a) or ("agent vish" in a) or ("vishal" not in a and "agent" not in a)
    # penalize if claims unrelated brands/names
    unrelated = bool(re.search(r"elon|openai ceo|google ceo|sundar pichai|bill gates", a))
    score = 0.8 - (0.5 if not ok_name else 0) - (0.5 if unrelated else 0)
    return score >= 0.5, max(min(score, 1.0), 0.0), ("ok" if score >= 0.5 else "names/details mismatch")

FALLBACK_MSG = "Sorry, I could not answer with high enough reliability or fact-match."

DEBUG_MODE = True

# ============ Skills ============
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
    if msg in ["about", "about vishal"]:
        return BIO
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
    if msg in ["skills", "core skills"]:
        return SKILLS
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
    if msg == "projects":
        return PROJECTS
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
    if msg == "features":
        return FEATURES
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

# ============ Main Agent with System-level Filters ============
class AgenticAIBot:
    def __init__(self, name: str = "Agent Vish"):
        self.name = name
        self.skills: List[Callable[[str, dict], str | None]] = []
        self.memory: Dict[str, Any] = {"debug": DEBUG_MODE}

        # Register core skills in priority order
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

    def _apply_filters(self, user_query: str, candidate: str) -> Tuple[bool, str]:
        h_ok, h_score, h_reason = hallucination_check(candidate, user_query)
        m_ok, m_score, m_reason = moderation_check(candidate)
        r_ok, r_score, r_reason = answer_relevance(user_query, candidate)
        cr_ok, cr_score, cr_reason = context_recall(self.memory, candidate)
        cp_ok, cp_score, cp_reason = context_precision(candidate)

        all_ok = all([h_ok, m_ok, r_ok, cr_ok, cp_ok])
        if not all_ok:
            return False, FALLBACK_MSG

        if self.memory.get("debug"):
            diag = (
                f"\n\n[diag] hallucination={h_ok} ({h_score:.2f}, {h_reason}); "
                f"moderation={m_ok} ({m_score:.2f}, {m_reason}); "
                f"relevance={r_ok} ({r_score:.2f}, {r_reason}); "
                f"context_recall={cr_ok} ({cr_score:.2f}, {cr_reason}); "
                f"context_precision={cp_ok} ({cp_score:.2f}, {cp_reason})"
            )
            return True, candidate + diag
        return True, candidate

    def receive_message(self, message: str) -> str:
        try:
            msg = clean_text(message)
            logger.info("Received message: %s", msg)

            # Route to skills in priority order and capture first candidate
            for skill in self.skills:
                try:
                    resp = skill(msg, self.memory)
                    if resp:
                        logger.info("Skill matched. Candidate: %s", resp[:120] + ("..." if len(resp) > 120 else ""))
                        ok, final = self._apply_filters(msg, resp)
                        if ok:
                            return final
                        # If filters fail, continue trying next skills for a better candidate
                except Exception as e:
                    logger.exception("Skill error: %s", e)
                    continue

            # Final fallback if no candidate passes filters
            return FALLBACK_MSG
        except Exception as e:
            logger.exception("Agent error: %s", e)
            return "Sorry, something went wrong. Please try again."
