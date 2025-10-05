from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "SoundTrack"
    VERSION: str = "1.0.0"

    # Firebase
    FIREBASE_CREDENTIALS_PATH: str = ""  # Path to service account JSON
    FIREBASE_PROJECT_ID: str = ""

    # CORS - simple list that works with env vars
    ALLOWED_HOSTS: str = "http://localhost:3000,http://127.0.0.1:3000"

    def get_allowed_hosts_list(self) -> List[str]:
        """Parse ALLOWED_HOSTS into a list"""
        return [host.strip() for host in self.ALLOWED_HOSTS.split(",")]

    # Storage (Firebase Storage)
    STORAGE_BUCKET: str = "soundtrack-media"

    # External APIs
    SPOTIFY_CLIENT_ID: str = ""
    SPOTIFY_CLIENT_SECRET: str = ""
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""

    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"

    class Config:
        env_file = ".env"

settings = Settings()