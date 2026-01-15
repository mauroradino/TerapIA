import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from integrations.supabase_client import supabase

def is_registered(id_val):
    try:
        res = supabase.table("Users").select("*").eq("telegram_id", id_val).execute()
        if res.data and len(res.data) > 0:
            return res.data
        else:
            return False

    except Exception as e:
        # 3. Aquí capturamos el error si ocurre
        print(f"Error al obtener datos: {e}")
        return None

# Prueba
print(is_registered("5464564564"))