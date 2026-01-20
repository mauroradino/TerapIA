from telethon import events
import sys
from pathlib import Path
from agents import Runner
from utils.registered_verification import is_registered
from utils.set_new_user import set_new_user
from agents_openai.QA_agent import QA_agent
sys.path.insert(0, str(Path(__file__).parent.parent))
from integrations.telegram_client import bot
from integrations.supabase_client import update_clinical_history
transcription_path = Path(__file__).parent/ 'audio' / 'transcription.txt'
with open(transcription_path, "r", encoding="utf-8") as file:
    transcription = file.read()

@bot.on(events.NewMessage(incoming=True, func=lambda e: e.voice or e.audio))
async def handler_audio(event):
    await event.download_media(file=f"audios/audio_test.ogg")
    await event.reply("Hi! I hope everything went well at your medical appointment. I'm processing the information and will contact you soon.")
    #Ahora el envio de mail al medico es opcional
    #await Runner.run(doctor_agent, f"Generate a medical report based on the transcription provided: {transcription}")
    #Ahora el envio de mail al medico es opcional
    await Runner.run(QA_agent, f"Acabas de recibir un audio, enviale por telegram al usuario un resumen amigable cálido y sencillo basado en la siguiente transcripción: {transcription} y este es el id de telegram del usuario: {event.sender_id}")
    update_clinical_history(transcription, str(event.sender_id))

@bot.on(events.NewMessage(incoming=True, func=lambda e: e.text))
async def handler_text(event):
    sender = await event.get_sender()
    usuario_id = sender.id
    user_data = is_registered(usuario_id) 
    if not user_data:
        set_new_user(str(usuario_id)) 
        user_data = [{"telegram_id": usuario_id, "name": "", "surname": "", "age": ""}]
    user_message = event.message.message
    response = await Runner.run(QA_agent, f"El usuario dice: {user_message}. Esta es la transcripción de la consulta médica: {transcription} y este el id de telegram del usuario: {usuario_id}. La informacion del usuario es: {user_data}")
    await event.reply(response.final_output)

print("Bot listening audios...")
bot.run_until_disconnected()