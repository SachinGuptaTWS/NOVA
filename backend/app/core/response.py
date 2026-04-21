import re
import httpx
from google import genai
from ..config import settings
from .intent import Intent, classify
from .mode import Mode, select_mode
from .context import store
from .guards import is_drifting, get_static_response, DATA

client = genai.Client(api_key=settings.API_KEY)

async def call_llm(system: str, history: str, user: str) -> str:
    prompt = f"System: {system}\n\nRecent History:\n{history}\n\nUser: {user}"
    
    # Try primary LLM
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception:
        pass  # Fall through to fallback
        
    # Try Fallback LLM
    try:
        async with httpx.AsyncClient() as hc:
            res = await hc.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"},
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": f"Recent History:\n{history}\n\nUser: {user}"}
                    ]
                },
                timeout=10.0
            )
            res.raise_for_status()
            return res.json()["choices"][0]["message"]["content"].strip()
    except Exception as groq_error:
        error_msg = str(groq_error).lower()
        if "429" in error_msg or "rate limit" in error_msg:
            return "Rate limit exceeded. Try again soon."
        elif "401" in error_msg or "unauthorized" in error_msg:
            return "Service configuration error. Contact support."
        elif "503" in error_msg or "unavailable" in error_msg:
            return "Service temporarily overloaded. Try again shortly."
        elif "timeout" in error_msg:
            return "Request took too long. Please try again."
        return "Unable to process your request. Please try again."

async def generate(session_id: str, message: str):
    session = store.get(session_id)
    
    # Handle auto-greeting/initialization
    if not message.strip() or message.upper() == "GREETING":
        return get_static_response("greeting"), Intent.CASUAL, Mode.PEER

    intent = classify(message)
    mode = select_mode(intent)
    
    # Update session flags based on audit
    if intent == Intent.LEAD_CAPTURE:
        session.lead_active = True
    if intent == Intent.COMPLAINT:
        session.handoff = True

    if is_drifting(session.history):
        return get_static_response("drift_guard"), intent, Mode.PEER
    
    if intent == Intent.FALLBACK:
        return get_static_response("fallback"), intent, mode

    # Single source of truth for history
    recent = session.history[-3:]
    history_str = "\n".join([f"{t['role']}: {t['content']}" for t in recent])
    
    courses = "\n".join([f"{c['name']}: {c['price']}" for c in DATA["courses"]])
    system_prompt = (
        f"You are NOVA, a NexPath admissions assistant. Mode: {mode.value}. "
        f"Courses:\n{courses}\n"
        "Rules: "
        "IF Mode is Support: Be clean, direct, helpful. No personality. No pushes. "
        "ELSE: Hook -> Value -> Push -> Closing. "
        "No emoji. Forbidden: 'cheap', 'best price', 'affordable'. "
        "NEVER SAY: 'Thanks for asking', 'Great question!', 'How can I assist you today?'"
    )
    
    reply = await call_llm(system_prompt, history_str, message)
    
    # Post-generation filter for forbidden phrases
    pricing_patterns = [r"(?i)\bcheap\b", r"(?i)\bbest price\b", r"(?i)\baffordable\b"]
    for pattern in pricing_patterns:
        reply = re.sub(pattern, "value-driven", reply)

    # For conversational phrases, remove them entirely including trailing punctuation/spaces
    chat_patterns = [
        r"(?i)thanks for asking[\s.!?,;:—\-]*",
        r"(?i)great question[\s.!?,;:—\-]*",
        r"(?i)how can I assist you today[\s.!?,;:—\-]*"
    ]
    for pattern in chat_patterns:
        reply = re.sub(pattern, "", reply)
        reply = reply.strip()

    session.history.append({"role": "user", "content": message, "intent": intent.value})
    session.history.append({"role": "bot", "content": reply})
    
    return reply, intent, mode
