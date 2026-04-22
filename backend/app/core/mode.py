from enum import Enum
from .intent import Intent

class Mode(Enum):
    """Operational persona styles applied to the LLM agent."""
    CONSULTANT = "Consultant"
    EXPERT = "Expert"
    PEER = "Peer"
    LEADFLOW = "LeadFlow"
    SUPPORT = "Support"
    FALLBACK = "Fallback"

INTENT_TO_MODE = {
    Intent.CAREER_QUERY: Mode.CONSULTANT,
    Intent.COURSE_QUERY: Mode.EXPERT,
    Intent.CASUAL: Mode.PEER,
    Intent.LEAD_CAPTURE: Mode.LEADFLOW,
    Intent.COMPLAINT: Mode.SUPPORT,
}

def select_mode(intent: Intent) -> Mode:
    """Map primary intent directly to conversational Mode personality."""
    return INTENT_TO_MODE.get(intent, Mode.FALLBACK)
