from telethon import TelegramClient
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

# Aseguramos que exista (y esté registrada) una event loop antes de
# inicializar el cliente de Telethon. Esto evita errores cuando este
# módulo se importa desde scripts síncronos (ej. evaluaciones).
try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

bot = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)
