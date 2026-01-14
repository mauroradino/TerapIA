from agents import Agent, Runner
from dotenv import load_dotenv
from pathlib import Path
from tools import send_email
from prompts import doctor_agent_prompt as doctor_prompt
load_dotenv()

transcription_path = Path(__file__).parent.parent / 'audio' / 'transcription.txt'
with open(transcription_path, "r", encoding="utf-8") as file:
    transcription = file.read()

agent = Agent(name="Doctor Agent", instructions=doctor_prompt, tools=[send_email])

def generate_report():
    result = Runner.run_sync(agent, "Generate a medical report based on the transcription provided.")

generate_report()    