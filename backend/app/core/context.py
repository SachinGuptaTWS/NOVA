import threading
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Dict, List, TypedDict

class HistoryEntry(TypedDict, total=False):
    role: str
    content: str
    intent: str

@dataclass
class Session:
    history: List[HistoryEntry] = field(default_factory=list)
    lead_active: bool = False
    handoff: bool = False

class SessionStore:
    """In-memory session store. Note: Limited to a single uvicorn worker process."""
    def __init__(self, max_sessions: int = 100):
        self.max_sessions = max_sessions
        self.sessions: OrderedDict[str, Session] = OrderedDict()
        self._lock = threading.Lock()

    def get(self, session_id: str) -> Session:
        with self._lock:
            if session_id not in self.sessions:
                self.sessions[session_id] = Session()
                self._cleanup()
            
            # Move to end
            self.sessions.move_to_end(session_id)
            return self.sessions[session_id]

    def _cleanup(self):
        """Thread-safe safe eviction of the oldest sessions by LRU logic."""
        while len(self.sessions) > self.max_sessions:
            self.sessions.popitem(last=False)

store: SessionStore = SessionStore()

