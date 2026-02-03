from agents import function_tool
import resend
import os 
from dotenv import load_dotenv
from pathlib import Path
import sys
import socket
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
    
import os
import requests
from dotenv import load_dotenv

load_dotenv()

@function_tool
def send_email(body: str, caution_signs: str, doctor_email: str) -> str:
    """
    Sends an email using the EmailJS service.
    Args:
        body (str): The main content of the email.
        caution_signs (str): Any caution signs to include.
        doctor_email (str): The recipient's email address.
    Returns:
        str: Confirmation message or error.
    """
    service_id = os.getenv("EMAILJS_SERVICE_ID")
    template_id = os.getenv("EMAILJS_TEMPLATE_ID")
    public_key = os.getenv("EMAILJS_PUBLIC_KEY")
    private_key = os.getenv("EMAILJS_PRIVATE_KEY") 
    if not all([service_id, template_id, public_key]):
        return "Error: Faltan variables de entorno de EmailJS."

    url = "https://api.emailjs.com/api/v1.0/email/send"

    data = {
        "service_id": service_id,
        "template_id": template_id,
        "accessToken": private_key,
        "user_id": public_key,
        "template_params": {
            "to_email": doctor_email,
            "body": body,
            "caution_signs": caution_signs
        }
    }

    try:
        response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            return f"Email enviado con éxito a {doctor_email} vía EmailJS."
        else:
            return f"Error de EmailJS ({response.status_code}): {response.text}"

    except Exception as e:
        print(f"Error de conexión con EmailJS: {str(e)}")
        return f"Error crítico al enviar email: {str(e)}"

        
@function_tool
async def set_reminder(interval_seconds: int, counter: int, chat_id: str, message_text: str) -> str:
    """
    Programa recordatorios para enviar mensajes en intervalos específicos.
    
    Args:
        interval_seconds (int): Segundos entre cada mensaje.
        counter (int): Cantidad total de mensajes a enviar.
        chat_id (str): ID del chat o Username del usuario.
        message_text (str): El contenido del recordatorio.
    """
    
    async def background_task():
        count = 0
        try:
            if not bot.is_connected():
                await bot.connect()

            target = chat_id
            if isinstance(chat_id, str):
                clean_id = chat_id.strip()
                if clean_id.lstrip('-').isdigit():
                    target = int(clean_id)
                else:
                    target = clean_id  
            
            entity = await bot.get_input_entity(target)
            while count < counter:
                await asyncio.sleep(interval_seconds)
                # Usar la entidad resuelta
                await bot.send_message(entity, message=message_text)
                count += 1
        except asyncio.CancelledError:
            print(f"⚠️ Tarea de recordatorio para {chat_id} cancelada.")
        except Exception as e:
            print(f"❌ Error crítico en recordatorio: {e}")

    asyncio.create_task(background_task())
    
    return f"Perfecto. He programado {counter} recordatorios cada {interval_seconds} segundos."



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