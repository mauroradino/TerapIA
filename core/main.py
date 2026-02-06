import sys
import os
from pathlib import Path
from telethon import events

sys.path.insert(0, str(Path(__file__).parent.parent))
import opik
from integrations.telegram_client import bot
from integrations.supabase_client import update_clinical_history, save_transcription
from agents import Runner
from agents_openai.QA_agent import QA_agent
from audio.audio_processor import transcribe_audio
from utils.registered_verification import is_registered
from utils.set_new_user import set_new_user

conversations = {}
user_transcriptions = {}
@bot.on(events.NewMessage(incoming=True, func=lambda e: e.voice or e.audio))
@opik.track("handler_audio")
async def handler_audio(event):
    user_id = str(event.sender_id)
    
    user_data = is_registered(user_id)
    if not user_data:
        set_new_user(user_id)
        user_data = {"name": "Unknown", "surname": "", "age": ""}

    await event.respond("🎙️ I've received your audio. I'm processing your consultation")

    audio_path = f"audios/audio_{user_id}.ogg"
    os.makedirs("audios", exist_ok=True)
    await event.download_media(file=audio_path)
    
    transcription = transcribe_audio() 
    user_transcriptions[user_id] = transcription
    
    update_clinical_history(transcription, user_id)
    save_transcription(transcription, user_id)

    conversations[user_id] = []

    prompt_audio = (
        f"MEDICAL PROTOCOL ACTIVATED\n"
        f"CURRENT PATIENT DATA: {user_data}\n" 
        f"TRANSCRIPTION: {transcription}\n"
        f"TASK: 1. Greet formally 2. Check if the PATIENT DATA is missing Name, Surname or Age."
        f"3. If they are complete, send the structured summary directly. "
        f"4. Offer to send an email to the doctor."
    )

    response = await Runner.run(QA_agent, prompt_audio)
    
    conversations[user_id].append({"role": "assistant", "content": response.final_output})
    await event.reply(response.final_output)

@bot.on(events.NewMessage(incoming=True, func=lambda e: e.text))
@opik.track("handler_text")
async def handler_text(event):
    user_id = str(event.sender_id)
    user_message = event.message.message
    
    user_data = is_registered(user_id)
    
    if not user_data:
        set_new_user(user_id)
        user_data = {"name": "Unknown", "surname": "", "age": ""}

    history = conversations.get(user_id, [])[-3:]

    last_transcription = user_transcriptions.get(user_id, "There are no recent transcripts.")

    prompt_text = (
        f"CONTEXT OF THE LAST CONSULTATION: {last_transcription}\n"
        f"CURRENT PATIENT DATA: {user_data}\n"
        f"USER MESSAGE: {user_message}\n"
        f"RECENT HISTORY: {history}\n\n"
        "INSTRUCTION: Respond naturally. If it's a greeting, be brief. "
        "If the user asks about the consultation, use the context. DO NOT generate a new summary "
        "unless the user specifically requests it."
    )

    response = await Runner.run(QA_agent, prompt_text)

    if user_id not in conversations:
        conversations[user_id] = []
    
    conversations[user_id].append({"role": "user", "content": user_message})
    conversations[user_id].append({"role": "assistant", "content": response.final_output})

    if len(conversations[user_id]) > 10:
        conversations[user_id] = conversations[user_id][-10:]

    await event.reply(response.final_output)


if __name__ == "__main__":
    print("🚀 TerapIA Bot is listening...")
    bot.run_until_disconnected()