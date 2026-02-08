from agents import Agent
from dotenv import load_dotenv
from core.agents_openai.tools import (
    set_reminder,
    update_user_info,
    send_telegram_message,
    send_email,
    search_emergency_contacts,
    set_emergency_contact,
    confirm_emergency_contact,
)
from core.agents_openai.prompts import QA_prompt

load_dotenv()


QA_agent = Agent(
    name="QA Agent",
    model="gpt-4o",
    instructions=QA_prompt,
    tools=[set_reminder, update_user_info, send_telegram_message, send_email, search_emergency_contacts, confirm_emergency_contact, set_emergency_contact],
)
