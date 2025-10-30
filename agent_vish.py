# agent_vish.py
import logging
import re
from typing import Callable, List, Dict, Any, Tuple
from skills.analytics_skill import analytics_skill

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

CLEAN_PATTERN = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]")

def clean_text(s: str) -> str:
    if not isinstance(s, str):
        return ""
    return CLEAN_PATTERN.sub("", s).strip()

# Core content constants
BIO = (
    "I'm Agent Vish, the AI assistant for Vishal Anand — a Customer Success Team Lead "
    "with 5+ years' experience in client lifecycle management, renewals, upsell/cross-sell, "
    "team leadership (4 AMs, coordination across 30 stakeholders), onboarding, escalations, "
    "and performance analytics at MyOperator. Vishal is keen on learning LLMs, agentic workflows, "
    "and prompt engineering. He drives GRR, NRR uplift, 6.5M upgrades/year, and consistently "
    "scores 95 CSAT/30 NPS for SMB/Enterprise. Tools: Salesforce, HubSpot, Zoho, WhatsApp Business API, MyOperator, Excel."
)

SKILLS = (
    "Core skills: Client lifecycle management, renewals, upsell/cross-sell strategies, renewal playbooks, "
    "metrics & KPIs (GRR, NRR, CSAT, NPS), performance analytics, dashboarding, stakeholder coaching, "
    "onboarding, escalation management, team leadership, Salesforce, HubSpot, Zoho, Excel, "
    "and learning LLMs, agentic workflows, and prompt engineering."
)

PROJECTS = (
    "Vishal has built Agent Vish (this chatbot!), led customer success initiatives driving 6.5M upgrades/year, "
    "created analytics dashboards, and is exploring agentic workflows. Ask about 'features' to learn more about this bot's capabilities."
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
    "title": "Customer Success Team Lead",
    "company": "MyOperator",
    "experience": "5+ years",
    "skills_keywords": [
        "client lifecycle management", "renewals", "upsell", "cross-sell", "team leadership",
        "onboarding", "escalations", "analytics", "dashboards", "CSAT", "NPS", "GRR", "NRR",
        "Salesforce", "HubSpot", "Zoho", "Excel", "learning LLMs", "agentic workflows", "prompt engineering"
    ],
    "projects_keywords": [
        "Agent Vish", "customer success", "6.5M upgrades", "analytics dashboards", "agentic workflows"
    ],
}

def hallucination_check(answer: str, user_query: str) -> Tuple[bool, float, str]:
    """
    Basic hallucination check: ensure key facts match KNOWN_FACTS.
    Return: (pass_flag, score, reason)
    """
    lower_ans = answer.lower()
    # Check for incorrect role descriptions
    if "ai/ml engineer" in lower_ans or "product-focused ai/ml" in lower_ans:
        return False, 0.0, "hallucination: incorrect role (AI/ML engineer)"
    
    # If answer mentions Vishal, ensure it doesn't contradict known facts
    if "vishal" in lower_ans:
        # Check for correct title
        if any(phrase in lower_ans for phrase in ["customer success", "team lead"]):
            return True, 1.0, "facts match"
        # If a role is mentioned but incorrect
        if any(phrase in lower_ans for phrase in ["engineer", "developer"]) and "learning" not in lower_ans:
            return False, 0.0, "hallucination: incorrect professional role"
    
    return True, 1.0, "no hallucination detected"

def moderation_check(answer: str) -> Tuple[bool, float, str]:
    """
    Moderation: flag inappropriate content.
    Return: (pass_flag, score, reason)
    """
    lower_ans = answer.lower()
    for category, words in MODERATION_BADWORDS.items():
        for w in words:
            if w in lower_ans:
                return False, 0.0, f"moderation fail: {category}"
    return True, 1.0, "clean"

def answer_relevance(query: str, answer: str) -> Tuple[bool, float, str]:
    """
    Check if answer is relevant to query.
    Return: (pass_flag, score, reason)
    """
    # Simple keyword overlap heuristic
    query_words = set(query.lower().split())
    answer_words = set(answer.lower().split())
    
    # Remove common stop words
    stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
    query_words -= stop_words
    answer_words -= stop_words
    
    if not query_words:
        return True, 1.0, "query too short to judge"
    
    overlap = len(query_words & answer_words)
    score = overlap / len(query_words) if query_words else 0.0
    
    # Relaxed threshold
    if score >= 0.2 or len(answer) > 50:  # If answer is substantial, give benefit of doubt
        return True, score, "relevant"
    return False, score, "not relevant"

def context_recall(memory: dict, answer: str) -> Tuple[bool, float, str]:
    """
    Check if answer properly recalls context from memory.
    Return: (pass_flag, score, reason)
    """
    # If no context, pass
    if not memory.get("history"):
        return True, 1.0, "no prior context"
    
    # Basic check: answer should not contradict memory
    # For now, just pass
    return True, 1.0, "context ok"

def context_precision(answer: str) -> Tuple[bool, float, str]:
    """
    Check if answer is precise and not overly verbose.
    Return: (pass_flag, score, reason)
    """
    # Simple length check
    if len(answer) > 1500:
        return False, 0.5, "too verbose"
    if len(answer) < 10:
        return False, 0.5, "too short"
    return True, 1.0, "precise"

# ============ Fallback Message ============
FALLBACK_MSG = (
    "I'm here to help! Try asking: 'about vishal', 'core skills', 'projects', or 'features'."
)

# ============ Skills Import ============
from skills.faq_skill import faq_skill
from skills.insight_skill import insight_skill
from skills.report_skill import report_skill
from skills.knowledge_skill import knowledge_skill
from skills.upsell_skill import upsell_skill

# ============ Agent Class ============
class AgentVish:
    def __init__(self, name: str = "Agent Vish"):
        self.name = name
        self.memory: Dict[str, Any] = {"history": [], "debug": False}
        self.skills: List[Callable[[str, dict], str | None]] = []
        
        # Register skills in priority order
        self.add_skill(faq_skill)
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
        """Apply all quality filters to candidate response."""
        h_ok, h_score, h_reason = hallucination_check(candidate, user_query)
        m_ok, m_score, m_reason = moderation_check(candidate)
        r_ok, r_score, r_reason = answer_relevance(user_query, candidate)
        cr_ok, cr_score, cr_reason = context_recall(self.memory, candidate)
        cp_ok, cp_score, cp_reason = context_precision(candidate)
        
        all_ok = all([h_ok, m_ok, r_ok, cr_ok, cp_ok])
        
        if not all_ok:
            return False, FALLBACK_MSG
        
        # Debug mode diagnostics
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
        """Main entry point for handling user messages."""
        try:
            msg = clean_text(message)
            logger.info("Received message: %s", msg)
            
            # Route to skills in priority order and capture first candidate
            for skill in self.skills:
                try:
                    resp = skill(msg, self.memory)
                    if resp:
                        logger.info(
                            "Skill matched. Candidate: %s",
                            resp[:120] + ("..." if len(resp) > 120 else "")
                        )
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

if __name__ == "__main__":
    agent = AgentVish()
    print(f"{agent.name} is ready!")
    
    # Test messages
    test_queries = [
        "about vishal",
        "core skills",
        "projects",
        "features",
    ]
    
    for q in test_queries:
        print(f"\nQ: {q}")
        print(f"A: {agent.receive_message(q)}")
