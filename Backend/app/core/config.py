from typing import Any, Dict, List, Optional, Union
import os
from dotenv import load_dotenv
from pydantic import BaseModel, validator
import secrets

# Load environment variables from .env file
load_dotenv()

class Settings(BaseModel):
    # Application
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = secrets.token_urlsafe(32)
    PORT: int = int(os.getenv("PORT", "8000"))
    API_V1_STR: str = "/api/v1"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ALGORITHM: str = "HS256"
    PROJECT_NAME: str = "EduAssist"
    
    # Database Configuration (SQLite only)
    SQLITE_URL: str = os.getenv("SQLITE_URL", "sqlite:///./eduassist.db")
    SQLALCHEMY_DATABASE_URI: str = SQLITE_URL
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", None)
    
    # Google AI
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY", None)
    
    # Storage Configuration
    STORAGE_BUCKET: str = os.getenv("STORAGE_BUCKET", "eduassist-files")
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB in bytes
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 