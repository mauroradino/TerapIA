import sys
import os
from pathlib import Path
from telethon import events

sys.path.insert(0, str(Path(__file__).parent.parent))

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
async def handler_audio(event):
    user_id = str(event.sender_id)
    
    user_data = is_registered(user_id)
    if not user_data:
        set_new_user(user_id)
        user_data = {"name": "Desconocido", "surname": "", "age": "N/A"}

    await event.respond("🎙️ He recibido tu audio. Estoy procesando la consulta...")

    audio_path = f"audios/audio_{user_id}.ogg"
    os.makedirs("audios", exist_ok=True)
    await event.download_media(file=audio_path)
    
    transcription = transcribe_audio() 
    user_transcriptions[user_id] = transcription
    
    update_clinical_history(transcription, user_id)
    save_transcription(transcription, user_id)

    conversations[user_id] = []

    prompt_audio = (
        f"PROTOCOLO MÉDICO ACTIVADO.\n"
        f"DATOS DEL PACIENTE ACTUAL: {user_data}\n" 
        f"TRANSCRIPCIÓN: {transcription}\n"
        f"TAREA: 1. Saluda formalmente. 2. Valida si en DATOS DEL PACIENTE faltan Nombre, Apellido o Edad. "
        f"3. Si están completos, envía el resumen estructurado directamente. "
        f"4. Ofrece enviar mail al médico."
    )

    response = await Runner.run(QA_agent, prompt_audio)
    
    conversations[user_id].append({"role": "assistant", "content": response.final_output})
    await event.reply(response.final_output)

@bot.on(events.NewMessage(incoming=True, func=lambda e: e.text))
async def handler_text(event):
    user_id = str(event.sender_id)
    user_message = event.message.message
    
    user_data = is_registered(user_id)
    
    if not user_data:
        set_new_user(user_id)
        user_data = {"name": "Desconocido", "surname": "", "age": "N/A"}

    history = conversations.get(user_id, [])

    last_transcription = user_transcriptions.get(user_id, "No hay transcripciones recientes.")

    prompt_text = (
        f"CONTEXTO DE LA ÚLTIMA CONSULTA: {last_transcription}\n"
        f"DATOS DEL PACIENTE: {user_data}\n"
        f"MENSAJE DEL USUARIO: {user_message}\n"
        f"HISTORIAL RECIENTE: {history}\n\n"
        "INSTRUCCIÓN: Responde de forma natural. Si es un saludo, sé breve. "
        "Si pregunta sobre la consulta, usa el contexto. NO generes el resumen de nuevo "
        "a menos que el usuario lo pida específicamente."
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
    print("🚀 TerapIA Bot está escuchando...")
    bot.run_until_disconnected()