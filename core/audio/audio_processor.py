from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from integrations.supabase_client import save_transcription
load_dotenv()

client = OpenAI()
audio_path = Path(__file__).parent.parent.parent / "audios" / "audio_test.ogg"
audio_file = open(audio_path, "rb")

def transcribe_audio():
    try:
        transcription = client.audio.transcriptions.create(
            model="gpt-4o-transcribe", 
            file=audio_file
        )
        return transcription.text
    except Exception as e:
        return f"Error during transcription: {e}"
    