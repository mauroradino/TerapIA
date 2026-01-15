from agents import Agent
from dotenv import load_dotenv
from agents_openai.prompts import QA_prompt
from agents_openai.tools import set_reminder, update_user_info
load_dotenv()


QA_agent = Agent(name="QA Agent", instructions=QA_prompt, tools=[set_reminder, update_user_info])
