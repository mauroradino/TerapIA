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
    
