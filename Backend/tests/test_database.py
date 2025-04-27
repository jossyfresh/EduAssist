import os
import pytest
import requests
from app.core.config import settings
from app.core.supabase import get_supabase
from postgrest.exceptions import APIError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_database_config():
    assert settings.SUPABASE_URL is not None
    assert settings.SUPABASE_URL.startswith("https://")
    assert settings.SUPABASE_SERVICE_KEY is not None
    assert len(settings.SUPABASE_SERVICE_KEY) > 0

def test_supabase_connection():
    # Try to make a request using the Supabase client
    supabase = get_supabase()
    try:
        response = supabase.table("learning_paths").select("*").execute()
        assert response.status_code == 200
    except APIError as e:
        # Table doesn't exist yet, which is fine for this test
        assert "relation" in str(e) and "does not exist" in str(e) 