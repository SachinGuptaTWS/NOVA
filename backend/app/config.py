import os
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR.parent / ".env"

if not ENV_PATH.exists() and not Path(".env").exists():
    raise FileNotFoundError("Critical: .env file is missing")

class Settings(BaseSettings):
    API_KEY: str = Field(...)
    GROQ_API_KEY: str = Field(...)
    DATA_PATH: str = str(BASE_DIR / "data" / "data.json")
    LEADS_PATH: str = str(BASE_DIR / "data" / "leads.json")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def validate_setup(self):
        if not self.API_KEY.strip() or self.API_KEY == "your_gemini_api_key_here":
            raise ValueError("API_KEY is missing or uses placeholder")
        if not self.GROQ_API_KEY.strip():
            raise ValueError("GROQ_API_KEY is missing or empty")

        data_dir = BASE_DIR / "data"
        if not data_dir.exists():
            data_dir.mkdir(parents=True)
            
        if not Path(self.DATA_PATH).exists():
            raise FileNotFoundError("Static data.json is missing")

settings = Settings()
settings.validate_setup()
