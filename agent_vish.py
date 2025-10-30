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
    # Collapse whitespace and remove control chars to enforce single-line
    s = CLEAN_PATTERN.sub("", s)
    s = re.sub(r"\s+", " ", s).strip()
    # Ensure no newlines remain
    return s.replace("\n", " ")

# Core content constants (single-line enforced)
BIO = (
    "Vishal Anand: Customer Success Team Lead at MyOperator; renewals, client lifecycle, upsell, analytics, onboarding, escalation, leadership; keen on LLMs & agentic workflows. You can connect with Vishal on LinkedIn (linkedin.com/in/vishalanand797) or drop him an email at vishalanand.work@gmail.com."
)
SKILLS = (
    "Skills: Renewals, upsell/cross-sell, onboarding, client lifecycle, dashboarding, coaching, escalation, Salesforce, HubSpot, Zoho, WhatsApp API, Excel, analytics. You can connect with Vishal on LinkedIn (linkedin.com/in/vishalanand797) or drop him an email at vishalanand.work@gmail.com."
)
PROJECTS = (
    "Projects: Agent Vish bot, CS upgrades (6.5M/yr), dashboards, agentic tools. You can connect with Vishal on LinkedIn (linkedin.com/in/vishalanand797) or drop him an email at vishalanand.work@gmail.com."
)
FEATURES = (
    "Features: FAQ, analytics, project tracking, workflows. You can connect with Vishal on LinkedIn (linkedin.com/in/vishalanand797) or drop him an email at vishalanand.work@gmail.com."
)
HELP = (
    "Try: about vishal, skills, projects, or features. You can connect with Vishal on LinkedIn (linkedin.com/in/vishalanand797) or drop him an email at vishalanand.work@gmail.com."
)
FALLBACK = (
    "Try: about vishal, skills, projects, or features. You can connect with Vishal on LinkedIn (linkedin.com/in/vishalanand797) or drop him an email at vishalanand.work@gmail.com."
)
DEBUG_SUMMARY_PREFIX = "Debug: "

# Response helpers to force single-line outputs everywhere
def single_line(text: str) -> str:
    return clean_text(text)

def debug_summary(info: Any) -> str:
    # Truncate any debug output to one concise line
    try:
        s = str(info)
    except Exception:
        s = repr(info)
    s = clean_text(s)
    if len(s) > 180:
        s = s[:177] + "..."
    return f"{DEBUG_SUMMARY_PREFIX}{s}"

class AgentVish:
    """Main agent class for Vishal's bot."""

    def __init__(self):
        # Intents map to response constants
        self.intents: Dict[str, Callable[[], str]] = {
            "bio": lambda: single_line(BIO),
            "skills": lambda: single_line(SKILLS),
            "projects": lambda: single_line(PROJECTS),
            "features": lambda: single_line(FEATURES),
            "help": lambda: single_line(HELP),
            "fallback": lambda: single_line(FALLBACK),
        }

    def receive_message(self, msg: str) -> str:
        """
        Process incoming messages and route to correct intent.
        
        Args:
            msg: User input text
            
        Returns:
            Single-line response string
        """
        if not msg:
            return self.handle_intent("fallback")
        
        # Normalize message
        msg_lower = msg.lower().strip()
        
        # Intent keyword matching
        # Analytics intent - route to analytics_skill
        if any(kw in msg_lower for kw in ["analytics", "google analytics", "sheets", "myoperator"]):
            try:
                result = analytics_skill(msg)
                result_str = str(result) if result else "No analytics data available."
                # Truncate to 250 chars if needed
                if len(result_str) > 250:
                    result_str = result_str[:247] + "..."
                return single_line(result_str)
            except Exception as e:
                logger.exception("Analytics skill failed")
                error_msg = f"Analytics error: {str(e)}"
                if len(error_msg) > 250:
                    error_msg = error_msg[:247] + "..."
                return single_line(error_msg)
        elif any(kw in msg_lower for kw in ["bio", "about", "who", "vishal"]):
            intent = "bio"
        elif any(kw in msg_lower for kw in ["skill", "expertise", "experience"]):
            intent = "skills"
        elif any(kw in msg_lower for kw in ["project", "work", "portfolio"]):
            intent = "projects"
        elif any(kw in msg_lower for kw in ["feature", "capability", "can you"]):
            intent = "features"
        elif any(kw in msg_lower for kw in ["help", "how", "what"]):
            intent = "help"
        else:
            intent = "fallback"
        
        return self.handle_intent(intent)
    
    def handle_intent(self, intent: str, debug: Any | None = None) -> str:
        """Handle intent routing and return appropriate response."""
        key = (intent or "").strip().lower()
        fn = self.intents.get(key, self.intents["fallback"])  # default to fallback
        resp = fn()
        if debug is not None:
            # Append concise debug summary separated by ' | '
            dbg = debug_summary(debug)
            return single_line(f"{resp} | {dbg}")
        return resp
    
    def analyze_performance(self, data: Dict[str, Any]) -> str:
        """Analyze performance data using analytics skill."""
        try:
            result = analytics_skill(data)
            return debug_summary(result)
        except Exception as e:
            logger.exception("analytics failed")
            return debug_summary({"error": str(e)})

# Backwards compatibility: keep module-level function
def handle_intent(intent: str, debug: Any | None = None) -> str:
    """Module-level function for backwards compatibility."""
    agent = AgentVish()
    return agent.handle_intent(intent, debug)

def analyze_performance(data: Dict[str, Any]) -> str:
    """Module-level function for backwards compatibility."""
    agent = AgentVish()
    return agent.analyze_performance(data)
