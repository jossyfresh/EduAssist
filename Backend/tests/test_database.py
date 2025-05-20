import os
import pytest
from app.core.config import settings

def test_database_config():
    assert settings.DATABASE_URL is not None
    assert settings.DATABASE_URL.startswith("sqlite:///")

def test_sqlite_connection():
    # This is a placeholder test. In a real scenario, you would use SQLAlchemy to connect to the SQLite database.
    # For now, we just check that the DATABASE_URL is set.
    assert settings.DATABASE_URL is not None 