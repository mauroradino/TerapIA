from agents import Agent, set_trace_processors
from dotenv import load_dotenv
from opik.integrations.openai.agents import OpikTracingProcessor
import opik

from core.agents_openai.tools import (
    set_reminder,
    update_user_info,
    send_telegram_message,
    send_email,
)

load_dotenv()

client = opik.Opik()
prompt = client.get_prompt(name="QA_agent_prompt")

set_trace_processors(processors=[OpikTracingProcessor()])

QA_agent = Agent(
    name="QA Agent",
    model="gpt-4o",
    instructions=prompt.prompt,
    tools=[set_reminder, update_user_info, send_telegram_message, send_email],
)
