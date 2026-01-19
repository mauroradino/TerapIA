from agents import Agent
from dotenv import load_dotenv
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from agents_openai.tools import send_email, IDC_codes
from agents_openai.prompts import doctor_agent_prompt as doctor_prompt

load_dotenv()

with open(Path(__file__).parent.parent / 'audio' / 'transcription.txt', "r", encoding="utf-8") as file:
    transcription = file.read()

doctor_agent = Agent(name="Doctor Agent", instructions=doctor_prompt, tools=[send_email, IDC_codes])
