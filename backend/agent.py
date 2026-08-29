import json
import os

from dotenv import load_dotenv
from google import genai

from backend.models import Session
from backend.prompts import SYSTEM_PROMPT
from backend.tools import (
    BOOK_SITE_VISIT_TOOL,
    UPDATE_LEAD_TOOL,
    book_site_visit,
)


load_dotenv()


class SessionManager:
    """Simple in-memory session manager."""

    def __init__(self):
        self.sessions: dict[str, Session] = {}

    def get_or_create(self, session_id: str) -> Session:
        if session_id not in self.sessions:
            self.sessions[session_id] = Session()

        return self.sessions[session_id]

    def save(self, session_id: str, session: Session) -> None:
        self.sessions[session_id] = session

    def delete(self, session_id: str) -> None:
        self.sessions.pop(session_id, None)


class NorthstarAgent:
    """Gemini-powered sales agent."""

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        model = os.getenv("GEMINI_MODEL")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set")

        if not model:
            raise ValueError("GEMINI_MODEL is not set")

        self.client = genai.Client(api_key=api_key)
        self.model = model

    def chat(self, session: Session, user_message: str) -> str:
        request = {
            "model": self.model,
            "input": user_message,
            "system_instruction": SYSTEM_PROMPT,
            "tools": [
                BOOK_SITE_VISIT_TOOL,
                UPDATE_LEAD_TOOL,
            ],
        }

        if session.gemini_interaction_id:
            request["previous_interaction_id"] = (
                session.gemini_interaction_id
            )

        interaction = self.client.interactions.create(**request)

        session.gemini_interaction_id = interaction.id

        function_calls = [
            step
            for step in interaction.steps
            if step.type == "function_call"
        ]

        if not function_calls:
            return interaction.output_text

        function_results = []

        for function_call in function_calls:
            arguments = function_call.arguments

            if isinstance(arguments, str):
                arguments = json.loads(arguments)

            if function_call.name == "update_lead":
                for field, value in arguments.items():
                    if value is not None:
                        setattr(session.lead, field, value)

                result = {
                    "status": "success",
                    "message": "Lead information updated.",
                }

            elif function_call.name == "book_site_visit":
                result = book_site_visit(
                    date=arguments["date"],
                    time=arguments["time"],
                )

                if result["status"] == "success":
                    session.lead.site_visit_status = "booked"
                    session.lead.site_visit_date = arguments["date"]
                    session.lead.site_visit_time = arguments["time"]
                else:
                    session.lead.site_visit_status = "unavailable"

            else:
                continue

            function_results.append(
                {
                    "type": "function_result",
                    "name": function_call.name,
                    "call_id": function_call.id,
                    "result": [
                        {
                            "type": "text",
                            "text": json.dumps(result),
                        }
                    ],
                }
            )

        if not function_results:
            return interaction.output_text

        final_interaction = self.client.interactions.create(
            model=self.model,
            previous_interaction_id=interaction.id,
            input=function_results,
        )

        session.gemini_interaction_id = final_interaction.id

        return final_interaction.output_text