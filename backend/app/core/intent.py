import re
import logging
from enum import Enum

logger = logging.getLogger(__name__)

class Intent(Enum):
    CAREER_QUERY = "career_query"
    COURSE_QUERY = "course_query"
    DOUBT = "doubt"
    SCHEDULE_QUERY = "schedule_query"
    CASUAL = "casual"
    LEAD_CAPTURE = "lead_capture"
    COMPLAINT = "complaint"
    FALLBACK = "fallback"

# First matching intent wins; order matters.
RULES = {
    Intent.CAREER_QUERY: ["job", "career", "future", "salary", "work", "placement"],
    Intent.COURSE_QUERY: ["course", "program", "learn", "study", "tell me about", "tell me more about", "tell me more", "price", "cost", "fee", "expensive", "pay", "tuition", "how much"],
    Intent.LEAD_CAPTURE: ["enroll", "apply", "sign up", "join", "admission", "register", "enrollment", "begin", "start"],
    Intent.SCHEDULE_QUERY: ["time", "when", "schedule", "duration", "hours"],
    Intent.DOUBT: ["what is nova", "how does it work", "where is it", "question", "help"],
    Intent.COMPLAINT: ["bad", "wrong", "fix", "issue", "terrible", "slow"],
    Intent.CASUAL: ["nice", "cool", "wow", "thanks", "weather", "game", "hello", "hi", "hey"]
}

def classify(message: str) -> Intent:
    clean = (message or "").strip().lower()
    for intent, keywords in RULES.items():
        for k in keywords:
            if re.search(r'\b' + re.escape(k) + r'\b', clean):
                logger.debug(f"classify: message={len(message or '')}chars, intent={intent.value}")
                return intent
                
    logger.debug(f"classify: message={len(message or '')}chars, intent={Intent.FALLBACK.value}")
    return Intent.FALLBACK
