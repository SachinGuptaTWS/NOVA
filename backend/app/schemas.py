from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str
    intent: str
    mode: str
    lead_flow_active: bool
    handoff: bool

class LeadRequest(BaseModel):
    session_id: str
    name: str
    email: str
    phone: str

class LeadResponse(BaseModel):
    status: str
    message: str
    lead_id: str
