from agents import function_tool
import resend
import os 
from dotenv import load_dotenv
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from integrations.telegram_client import bot
sys.path.insert(0, str(Path(__file__).parent.parent))
from templates.email_template import email_template
from datetime import datetime, timedelta
import asyncio
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from integrations.supabase_client import supabase
import requests
from opik import track
load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

@function_tool
async def send_telegram_message(message: str) -> str:
    """
    Sends a Telegram message to the specified recipient.

    Args:
        message (str): The message content to send.
    
    Returns:
        str: Confirmation message or error.
    """
    try:
        await bot.send_message("mauroradino", message)
        return "Mensaje enviado con éxito!"
    except Exception as e:
        return f"Error al enviar mensaje: {e}"

@function_tool
def send_email(body: str, caution_signs: str) -> str:
    """
    Sends an email using the configured email service.

    Args:
        body (str): The body content of the email.
        caution_signs (str): The caution signs to include in the email.
    
    Returns:
        str: Confirmation message with email ID or error.
    """
    try:
        if not resend.api_key:
            return "Error: RESEND_API_KEY no está configurada"
        
        params = {
            "from": "onboarding@resend.dev",
            "to": ["mauroradino22@gmail.com"],
            "subject": "Medical Report - TerapIA",
            "html": email_template.format(body=body, caution_signs=caution_signs),
        }
        
        resend.Emails.send(params)
        return "Email sent successfully."
    except Exception as e:
        return f"Error al enviar email: {str(e)}"
    
from apscheduler.schedulers.background import BackgroundScheduler
from integrations.telegram_client import bot 
scheduler = BackgroundScheduler()
scheduler.start()

# Esta es la función que se ejecutará cuando suene la alarma
def send_message(chat_id, mensaje):
    loop_del_bot = bot._loop 

    if loop_del_bot and loop_del_bot.is_running():
        asyncio.run_coroutine_threadsafe(
            bot.send_message(chat_id, mensaje),
            loop_del_bot
        )
    else:
        print("Error: El bot no está conectado o el loop murió.")
        
@function_tool
def set_reminder(mensaje: str, minutos: int) -> str:
    # 1. Calculamos cuándo debe enviarse
    fecha_ejecucion = datetime.now() + timedelta(minutes=minutos)
    
    try:
        # 2. Agregamos la tarea al planificador
        # Le decimos: "Ejecuta 'tarea_enviar_mensaje' en la fecha X con estos argumentos"
        scheduler.add_job(
            send_message, 
            'date', 
            run_date=fecha_ejecucion, 
            args=["mauroradino", mensaje] # Argumentos para la función
        )
        
        return f"Listo. He programado el recordatorio internamente para las {fecha_ejecucion.strftime('%H:%M')}."
        
    except Exception as e:
        return f"Error al programar internamente: {str(e)}"


@function_tool
def update_user_info(key: str, value: str, telegram_id: str) -> str:
    """
    Updates user information in the database.
    Args:
        key (str): The field to update.
        value (str): The new value for the field.
        telegram_id (str): The Telegram ID of the user.
        Returns:
        str: Confirmation message or error.
    """
    try:
        res = supabase.table("Users").update({key: value}).eq("telegram_id", telegram_id).execute()
        
        if len(res.data) > 0:
            return f"Éxito: Se actualizó {key} a '{value}'."
        else:
            return "Aviso: No se encontró ningún usuario con ese ID para actualizar."

    except Exception as e:
        return f"Error crítico: {str(e)}"
    

@function_tool
def IDC_codes(disease: str):
    """
    Provides ICD codes for a given disease.
    
    Args:
        disease (str): The name of the disease.
    Returns:
        str: ICD codes or error message.
    """
    res = requests.get(f"https://clinicaltables.nlm.nih.gov/api/icd11_codes/v3/search?terms={disease}")
    if res.status_code == 200:
        data = res.json()
        return data[3]
    else:
        return "Error al obtener los códigos IDC."