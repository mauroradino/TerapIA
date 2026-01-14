from telethon import TelegramClient
import os
from dotenv import load_dotenv
load_dotenv()

api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)


async def main():
    destinatario = 'mauroradino' 
    mensaje = 'Hola! Este es un mensaje enviado desde mi script en Python con Telethon.'

    try:
        await bot.send_message(destinatario, mensaje)
        print("Mensaje enviado con éxito!")
    except Exception as e:
        print(f"Error al enviar mensaje: {e}")

with bot:
    bot.loop.run_until_complete(main())