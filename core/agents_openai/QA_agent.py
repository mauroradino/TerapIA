from agents import Agent, set_trace_processors
from dotenv import load_dotenv
from agents_openai.prompts import QA_prompt
from agents_openai.tools import set_reminder, update_user_info, send_telegram_message
from opik.integrations.openai.agents import OpikTracingProcessor
load_dotenv()

set_trace_processors(processors=[OpikTracingProcessor()])




QA_agent = Agent(name="QA Agent", instructions=QA_prompt, tools=[set_reminder, update_user_info, send_telegram_message],)