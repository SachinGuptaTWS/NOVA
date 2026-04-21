from enum import Enum

class Intent(Enum):
    CAREER_QUERY = "career_query"
    COURSE_QUERY = "course_query"
    DOUBT = "doubt"
    SCHEDULE_QUERY = "schedule_query"
    CASUAL = "casual"
    LEAD_CAPTURE = "lead_capture"
    COMPLAINT = "complaint"
    FALLBACK = "fallback"

RULES = {
    Intent.CAREER_QUERY: ["job", "career", "future", "salary", "work", "placement"],
    Intent.COURSE_QUERY: ["course", "program", "learn", "study", "tell me about", "tell me more about", "tell me more", "price", "cost", "fee", "expensive", "pay", "tuition", "how much"],
    Intent.LEAD_CAPTURE: ["enroll", "apply", "sign up", "join", "admission"],
    Intent.SCHEDULE_QUERY: ["time", "when", "schedule", "duration", "hours"],
    Intent.DOUBT: ["what is nova", "how does it work", "where is it", "question", "help"],
    Intent.COMPLAINT: ["bad", "wrong", "fix", "issue", "terrible", "slow"],
    Intent.CASUAL: ["nice", "cool", "wow", "thanks", "weather", "game", "hello", "hi", "hey"]
}

def classify(message: str) -> Intent:
    clean = message.lower()
    for intent, keywords in RULES.items():
        if any(k in clean for k in keywords):
            return intent
    return Intent.FALLBACK
