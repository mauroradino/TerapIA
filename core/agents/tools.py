from agents import function_tool
import resend
import os 
from dotenv import load_dotenv
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from templates.email_template import email_template

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")


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