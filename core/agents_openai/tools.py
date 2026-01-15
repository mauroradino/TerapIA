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
def send_email(body: str) -> str:
    """
    Sends an email using the configured email service.

    Args:
        body (str): The body content of the email.
    
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
            "html": email_template.format(body=body),
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
