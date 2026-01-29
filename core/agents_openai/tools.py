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
    


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from agents import function_tool
import os

@function_tool
def send_email(body: str, caution_signs: str, doctor_email: str) -> str:
    # 1. Configuración de puertos para la nube (Paso 2)
    smtp_server = "173.194.76.108"
    smtp_port = 587  # El puerto 587 es el estándar para despliegues en Railway/Render
    sender_email = os.getenv("SMTP_EMAIL")
    sender_password = os.getenv("SMTP_PASSWORD") 

    if not sender_email or not sender_password:
        return "Error: Credenciales SMTP no configuradas."

    try:
        # Forzar IPv4 para evitar el error "Network is unreachable" en Railway
        # (Esto resuelve problemas de ruteo interno del servidor)
        socket.setdefaulttimeout(30)
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "Medical Report - TerapIA"
        message["From"] = f"TerapIA Assist <{sender_email}>"
        message["To"] = doctor_email

        # (Asumo que traes el template aquí)
        from core.templates.email_template import email_template
        html_content = email_template.format(body=body, caution_signs=caution_signs)
        message.attach(MIMEText(html_content, "html"))

        # 2. Conexión compatible con Railway (Paso 2 avanzado)
        # Usamos SMTP estándar + STARTTLS
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()            # Identificarse con el servidor
        server.starttls()        # Iniciar cifrado (obligatorio en puerto 587)
        server.ehlo()            # Volver a identificarse sobre conexión cifrada
        
        # 3. Autenticación (Paso 3)
        # IMPORTANTE: sender_password DEBE ser una "Contraseña de Aplicación"
        server.login(sender_email, sender_password)
        
        server.sendmail(sender_email, doctor_email, message.as_string())
        server.quit()

        return f"Email enviado con éxito a {doctor_email}."

    except Exception as e:
        print(f"Error detallado en Railway: {str(e)}")
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
            if isinstance(chat_id, str):
                clean_id = chat_id.strip()
                if clean_id.replace('-', '').isdigit():
                    target = int(clean_id)
                else:
                    target = clean_id  
            else:
                target = chat_id

            while count < counter:
                await asyncio.sleep(interval_seconds)
                await bot.send_message(target, message=message_text)
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