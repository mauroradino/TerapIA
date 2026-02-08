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

# Create the Telegram client but DO NOT start it at import time.
# Starting the client can trigger network calls (authorization) and
# cause FloodWait errors if repeated during imports or restarts.
bot = TelegramClient("bot", api_id, api_hash)

async def start_bot():
    """Start the Telegram client. Call this from your main runtime.
    This function catches FloodWaitError and re-raises after logging
    so the caller can decide how to handle restarts/delays.
    """
    from telethon.errors import rpcerrorlist
    try:
        await bot.start(bot_token=bot_token)
    except rpcerrorlist.FloodWaitError as e:
        print(f"Telethon FloodWaitError: must wait {e.seconds} seconds before retrying")
        raise
