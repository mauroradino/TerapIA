import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from integrations.supabase_client import supabase

def set_new_user(telegram_id: str):
    try:
        res = supabase.table("Users").insert({"telegram_id": telegram_id}).execute()
        
        return res.data, None

    except Exception as e:
        print(f"Error al crear usuario: {e}")
        
        return None, str(e)