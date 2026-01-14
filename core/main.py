from telethon import events
import sys
from pathlib import Path
from audio.audio_processor import transcribe_audio
from agents import Runner
from agents_openai.doctor_agent import doctor_agent
sys.path.insert(0, str(Path(__file__).parent.parent))
from integrations.telegram_client import bot

@bot.on(events.NewMessage(incoming=True, func=lambda e: e.voice or e.audio))
async def handler_audio(event):
    sender = await event.get_sender()
    usuario_id = sender.id
    
    print(f"Receiving audio from: {usuario_id}...")

    ruta_archivo = await event.download_media(file=f"audios/audio_test.ogg")
    
    print(f"Audio saved in: {ruta_archivo}")
    
    await event.reply("Hi! I hope everything went well at your medical appointment. I'm processing the information and will contact you soon.")
    transcription = transcribe_audio()
    
    response = await Runner.run(doctor_agent, f"Generate a medical report based on the transcription provided: {transcription}")
    print(response.final_output)

print("Bot listening audios...")
bot.run_until_disconnected()