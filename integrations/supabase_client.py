from supabase import create_client 
from dotenv import load_dotenv
load_dotenv()
import os
import datetime
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
TABLE = "Users"
  
def update_clinical_history(clinical_history: str, telegram_id: str):
    # 1. Obtener la historia actual
    response = supabase.table(TABLE).select("clinical_history").eq("telegram_id", telegram_id).single().execute()
    current_history = response.data.get("clinical_history")
    
    # Si es nulo o no es una lista, inicializarla
    if not isinstance(current_history, list):
        current_history = []
        
    # 2. Crear la nueva entrada
    new_entry = {
        "transcription": clinical_history,
        "date": datetime.datetime.now().isoformat()
    }
    
    # 3. Agregar a la lista local
    current_history.append(new_entry)
    
    # 4. Actualizar en la base de datos
    supabase.table(TABLE).update({"clinical_history": current_history}).eq("telegram_id", telegram_id).execute()

    return "Clinical history updated successfully."