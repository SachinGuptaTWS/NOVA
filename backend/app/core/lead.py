import json
import os
import tempfile
import logging
from ..config import settings
from ..schemas import LeadRequest

logger = logging.getLogger(__name__)

def save_lead(lead: LeadRequest) -> str:
    path = settings.LEADS_PATH
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    leads = []
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                leads = json.load(f)
        except (json.JSONDecodeError, PermissionError) as e:
            logger.error(f"Failed to load valid leads payload: {e}. Defaulting to empty.")
            leads = []
    
    lead_id = str(len(leads) + 1)
    
    # Store clean dumped dictionary
    leads.append(lead.model_dump())
    
    # Atomic write pattern to minimize concurrency collisions and corruption
    try:
        fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(path), text=True)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(leads, f, separators=(',', ':'))
            
        os.replace(temp_path, path)
        logger.info(f"Lead securely persisted. ID: {lead_id}")
    except Exception as e:
        logger.error(f"Critical write failure for {lead_id}: {e}")
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception:
            pass
        raise RuntimeError("Lead storage unavailable. Try again later.")
        
    return lead_id
