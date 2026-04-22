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
    Intent.CAREER_QUERY: ["job", "career", "future", "salary", "work", "placement", "hire", "hiring", "interview", "resume", "opportunities", "earnings", "role", "position", "career path", "outcome", "outcomes", "companies", "alumni"],
    Intent.COURSE_QUERY: ["course", "program", "learn", "study", "tell me about", "tell me more about", "tell me more", "price", "cost", "fee", "expensive", "pay", "tuition", "how much", "full-stack", "full stack", "fullstack", "engineering", "data science", "data", "science", "ai", "ui", "ux", "design", "curriculum", "syllabus", "topics", "skills", "technologies", "frameworks", "what will i learn", "pricing", "money", "afford", "costly", "cheap", "scholarship", "financial aid", "bootcamp"],
    Intent.LEAD_CAPTURE: ["enroll", "apply", "sign up", "join", "admission", "register", "enrollment", "begin", "start", "get started", "registration", "application", "onboard", "admissions", "reserve", "book", "participate", "i'm in"],
    Intent.SCHEDULE_QUERY: ["time", "when", "schedule", "duration", "hours", "dates", "deadline", "timeline", "classes", "part-time", "full-time", "morning", "evening", "weeks", "months", "how long", "weekend", "weekdays"],
    Intent.DOUBT: ["what is nova", "how does it work", "where is it", "question", "help", "faq", "what do you do", "explain", "confused", "not sure", "don't understand", "lost", "location", "online", "remote", "campus", "location"],
    Intent.COMPLAINT: ["bad", "wrong", "fix", "issue", "terrible", "slow", "broken", "error", "sucks", "awful", "not working", "worst", "hate", "frustrated", "annoying", "bug", "mistake"],
    Intent.CASUAL: ["nice", "cool", "wow", "thanks", "weather", "game", "hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening", "howdy", "sup", "what's up", "awesome", "great", "excellent", "bye", "goodbye", "see ya", "sweet", "amazing"]
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
