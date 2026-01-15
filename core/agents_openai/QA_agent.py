from agents import Agent
from dotenv import load_dotenv
from agents_openai.prompts import QA_prompt
load_dotenv()


QA_agent = Agent(name="QA Agent", instructions=QA_prompt)
