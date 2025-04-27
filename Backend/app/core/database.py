from supabase import create_client, Client
from typing import Generator
from sqlalchemy.orm import Session
from app.core.config import settings

# Initialize Supabase client
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)

def get_db() -> Generator[Session, None, None]:
    """
    Get database session
    """
    try:
        yield supabase
    finally:
        pass  # Supabase client doesn't need explicit closing 