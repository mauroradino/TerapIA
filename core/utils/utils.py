from core.allowed_domains import allowed_domains
from integrations.supabase_client import supabase

def verify_email(email: str) -> bool:
    if "@" not in email:
        return False
    
    domain = email.split("@")[1]
    return domain in allowed_domains


def is_registered(id_val):
    try:
        res = supabase.table("Users").select("*").eq("telegram_id", id_val).execute()
        if res.data and len(res.data) > 0:
            return res.data
        else:
            return False

    except Exception as e:
        print(f"Error getting user data: {e}")
        return None


def set_new_user(telegram_id: str):
    try:
        res = supabase.table("Users").insert({"telegram_id": telegram_id}).execute()
        return res.data, None

    except Exception as e:
        print(f"Error creating user: {e}")
        return None, str(e)