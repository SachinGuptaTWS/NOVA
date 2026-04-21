from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class Session:
    history: List[dict] = field(default_factory=list)
    lead_active: bool = False
    handoff: bool = False

class SessionStore:
    def __init__(self):
        self.sessions: Dict[str, Session] = {}

    def get(self, session_id: str) -> Session:
        if session_id not in self.sessions:
            self.sessions[session_id] = Session()
            self._cleanup()
        return self.sessions[session_id]

    def _cleanup(self):
        # Basic cleanup: keep only last 100 sessions
        if len(self.sessions) > 100:
            oldest_keys = list(self.sessions.keys())[:-100]
            for k in oldest_keys:
                del self.sessions[k]

store = SessionStore()
