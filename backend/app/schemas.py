from typing import Literal
from pydantic import BaseModel, Field, EmailStr, ConfigDict

class ChatRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    session_id: str = Field(min_length=1, max_length=64, pattern=r"^[a-zA-Z0-9\-_]+$")
    message: str = Field(max_length=5000)

class ChatResponse(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    reply: str = Field(max_length=10000)
    intent: str
    mode: str
    lead_flow_active: bool
    handoff: bool

class LeadRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    session_id: str = Field(min_length=1, max_length=64, pattern=r"^[a-zA-Z0-9\-_]+$")
    name: str = Field(min_length=3, max_length=100)
    email: EmailStr
    phone: str = Field(pattern=r"^\d{10,}$")

class LeadResponse(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    status: Literal["saved", "error"]
    message: str
    lead_id: str

