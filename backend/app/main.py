from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .schemas import ChatRequest, ChatResponse, LeadRequest, LeadResponse
from .core.response import generate
from .core.context import store
from .core.lead import save_lead
from .core.guards import get_static_response

app = FastAPI(title="NexPath NOVA API")

# Restrict CORS to development frontend ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    reply, intent, mode = await generate(request.session_id, request.message)
    session = store.get(request.session_id)
    return ChatResponse(
        reply=reply,
        intent=intent.value,
        mode=mode.value,
        lead_flow_active=session.lead_active,
        handoff=session.handoff
    )

@app.post("/lead", response_model=LeadResponse)
async def lead(request: LeadRequest):
    lead_id = save_lead(request)
    return LeadResponse(
        status="saved", 
        message=get_static_response("lead_success"),
        lead_id=lead_id
    )
