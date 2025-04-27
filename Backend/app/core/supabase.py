from supabase import create_client, Client
from app.core.config import settings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client with the correct URL
url = settings.SUPABASE_URL.replace(".com", ".co") if settings.SUPABASE_URL.endswith(".com") else settings.SUPABASE_URL
supabase: Client = create_client(url, settings.SUPABASE_SERVICE_KEY)

def get_supabase():
    return supabase 