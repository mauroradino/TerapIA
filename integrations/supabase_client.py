from supabase import create_client 
from dotenv import load_dotenv
load_dotenv()
import os
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
TABLE = "Users"
  