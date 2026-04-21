from enum import Enum
from .intent import Intent

class Mode(Enum):
    CONSULTANT = "Consultant"
    EXPERT = "Expert"
    PEER = "Peer"
    LEADFLOW = "LeadFlow"
    SUPPORT = "Support"
    FALLBACK = "Fallback"

def select_mode(intent: Intent) -> Mode:
    if intent == Intent.CAREER_QUERY:
        return Mode.CONSULTANT
    if intent == Intent.COURSE_QUERY:
        return Mode.EXPERT
    if intent == Intent.CASUAL:
        return Mode.PEER
    if intent == Intent.LEAD_CAPTURE:
        return Mode.LEADFLOW
    if intent == Intent.COMPLAINT:
        return Mode.SUPPORT
    return Mode.FALLBACK
