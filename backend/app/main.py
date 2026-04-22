import logging
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from .schemas import ChatRequest, ChatResponse, LeadRequest, LeadResponse
from .core.response import generate
from .core.context import store
from .core.lead import save_lead
from .core.guards import get_static_response, DATA

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing NexPath NOVA API...")
    if "static_responses" not in DATA or "courses" not in DATA:
        logger.warning("Core data dependencies missing from payload.")
    yield
logger.info("Shutting down NexPath NOVA API...")

app = FastAPI(title="NexPath NOVA", lifespan=lifespan)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.middleware("http")
async def enforce_payload_limit(request: Request, call_next):
    content_length = request.headers.get("content-length")
    # Enforce an absolute 1MB cutoff to prevent buffering DOS memory starvation
    if content_length and int(content_length) > 1048576:
        return JSONResponse(status_code=413, content={"detail": "Payload Too Large"})
    return await call_next(request)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    logger.info(f"Method={request.method} Path={request.url.path} Status={response.status_code} Latency={process_time:.2f}ms")
    return response

@app.post("/chat", response_model=ChatResponse)
@limiter.limit("20/minute")
async def chat(request: Request, payload: ChatRequest):
    try:
        reply, intent, mode = await generate(payload.session_id, payload.message)
        session = store.get(payload.session_id)
        return ChatResponse(
            reply=reply,
            intent=intent.value,
            mode=mode.value,
            lead_flow_active=session.lead_active,
            handoff=session.handoff
        )
    except Exception as e:
        logger.error(f"Chat failed for {payload.session_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal processing error")

@app.post("/lead", response_model=LeadResponse)
@limiter.limit("5/minute")
async def lead(request: Request, payload: LeadRequest):
    try:
        lead_id = save_lead(payload)
        return LeadResponse(
            status="saved", 
            message=get_static_response("lead_success"),
            lead_id=lead_id
        )
    except Exception as e:
        logger.error(f"Lead persistence failed for {payload.session_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Storage processing error")
