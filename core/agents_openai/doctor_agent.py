from agents import Agent
from dotenv import load_dotenv
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from agents_openai.tools import send_email, send_telegram_message
from agents_openai.prompts import doctor_agent_prompt as doctor_prompt
load_dotenv()


doctor_agent = Agent(name="Doctor Agent", instructions=doctor_prompt, tools=[send_email, send_telegram_message])
""" 
def generate_report():
    result = Runner.run_sync(doctor_agent, "Generate a medical report based on the transcription provided.")

generate_report()       """