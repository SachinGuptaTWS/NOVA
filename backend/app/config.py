import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")
    API_KEY: str = os.getenv("API_KEY") # No default, makes it required
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    DATA_PATH: str = str(BASE_DIR / "data" / "data.json")
    LEADS_PATH: str = str(BASE_DIR / "data" / "leads.json")

    def validate(self):
        if not self.API_KEY or self.API_KEY == "your_gemini_api_key_here":
            raise ValueError("API_KEY is missing or using placeholder in .env")
        if not self.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is missing in .env")

settings = Settings()
settings.validate()
