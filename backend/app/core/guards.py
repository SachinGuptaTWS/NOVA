import json
from ..config import settings
from .context import Session
from .intent import Intent

def load_data():
    with open(settings.DATA_PATH) as f:
        return json.load(f)

DATA = load_data()

def is_drifting(history: list) -> bool:
    casual_count = 0
    for turn in reversed(history[-5:]):
        if turn.get("intent") == Intent.CASUAL.value:
            casual_count += 1
        else:
            break
    return casual_count >= 3

def get_static_response(key: str) -> str:
    return DATA["static_responses"].get(key, "")
