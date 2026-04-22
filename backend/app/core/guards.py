import json
import logging
from types import MappingProxyType
from ..config import settings
from .context import Session
from .intent import Intent

logger = logging.getLogger(__name__)

def load_data():
    """Loads system data payload synchronously at app boot."""
    try:
        with open(settings.DATA_PATH) as f:
            raw_data = json.load(f)
            
        if "static_responses" not in raw_data:
            logger.warning("Missing 'static_responses' in data.json")
            raw_data["static_responses"] = {}
            
        if "courses" not in raw_data:
            logger.warning("Missing 'courses' in data.json")
            raw_data["courses"] = []
            
        return MappingProxyType(raw_data)
    except Exception as e:
        logger.error(f"Failed to load required data.json: {e}")
        return MappingProxyType({"static_responses": {}, "courses": []})

DATA = load_data()

def is_drifting(history: list) -> bool:
    """Evaluates trailing conversational memory for three consecutive casual intents."""
    casual_count = 0
    for turn in reversed(history[-5:]):
        if not isinstance(turn, dict):
            break
        if turn.get("intent") == Intent.CASUAL.value:
            casual_count += 1
        else:
            break
    return casual_count >= 3

def get_static_response(key: str) -> str:
    """Retrieve hardcoded fallback responses."""
    return DATA["static_responses"].get(key, "")
