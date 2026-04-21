import json
import os
from ..config import settings
from ..schemas import LeadRequest

def save_lead(lead: LeadRequest):
    path = settings.LEADS_PATH
    leads = []
    if os.path.exists(path):
        with open(path, "r") as f:
            leads = json.load(f)
    
    leads.append(lead.model_dump())
    
    with open(path, "w") as f:
        json.dump(leads, f, indent=2)
    
    return str(len(leads))
