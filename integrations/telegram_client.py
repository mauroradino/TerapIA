from telethon import TelegramClient
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

bot = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)
