"""
Lesson 3: Getting Structured Output

One of the most powerful features of the Strands SDK: extracting structured data
(like JSON) from unstructured text. We use a Pydantic model to define the exact
schema we want, and pass it as structured_output_model when invoking the agent.
The LLM's response is forced into that schema and returned as a validated object.

- Define a Pydantic model (e.g. PersonInfo) with Field(description=...) for clarity.
- Call agent(prompt, structured_output_model=PersonInfo).
- Access the result via result.structured_output (a typed PersonInfo instance).

API key: GROQ_API_KEY in repo root .env (same as Lessons 1–2).
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from strands import Agent
from strands.models.litellm import LiteLLMModel

_repo_root = Path(__file__).resolve().parent.parent
load_dotenv(_repo_root / ".env")

# ---------------------------------------------------------------------------
# Pydantic models: define the exact data schema you want from the LLM
# ---------------------------------------------------------------------------

class PersonInfo(BaseModel):
    """Structured information about a person extracted from text."""

    name: str = Field(description="Full name of the person")
    age: int | None = Field(default=None, description="Age in years when mentioned (0-150)")
    occupation: str | None = Field(default=None, description="Job or occupation when mentioned")
    location: str | None = Field(default=None, description="City or place if mentioned")


class MeetingSummary(BaseModel):
    """Structured summary of a meeting or event from a description."""

    title: str = Field(description="Short title of the meeting or event")
    date: str = Field(description="Date mentioned (e.g. 'March 6, 2025' or 'tomorrow')")
    participants: list[str] = Field(description="Names of people involved", default_factory=list)
    action_items: list[str] = Field(description="Action items or next steps", default_factory=list)


# ---------------------------------------------------------------------------
# System prompt: instruct the agent to extract information accurately
# ---------------------------------------------------------------------------
EXTRACTION_SYSTEM_PROMPT = """You are a precise information-extraction assistant.

Given the user's text, extract only the requested structured information.
Do not invent or assume details that are not clearly stated. Use null or empty
lists for missing optional fields. Be concise and accurate."""


def _get_api_key() -> str | None:
    """Read Groq API key from environment. Never commit .env."""
    key = os.environ.get("GROQ_API_KEY")
    return (key or "").strip() or None


def create_agent() -> Agent:
    """
    Create an agent configured for structured output extraction.

    Example:
        result = agent(
            "Eugene Sim, 28, is an aspiring data engineer based in Singapore.",
            structured_output_model=PersonInfo,
        )
        person = result.structured_output  # PersonInfo instance
    """
    api_key = _get_api_key()
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not set. Add it to the repo root .env file. "
            "Free key at https://console.groq.com"
        )

    model = LiteLLMModel(
        client_args={"api_key": api_key},
        model_id="groq/llama-3.3-70b-versatile",
        params={"max_tokens": 512, "temperature": 0.2},
    )

    return Agent(
        model=model,
        system_prompt=EXTRACTION_SYSTEM_PROMPT,
        callback_handler=None,
    )


def extract_person(text: str) -> PersonInfo:
    """Extract PersonInfo from unstructured text. Missing fields become None or empty."""
    agent = create_agent()
    result = agent(
        f"Extract the person's name, age, occupation, and location (if any) from this text:\n\n{text}",
        structured_output_model=PersonInfo,
    )
    return result.structured_output


def extract_meeting(text: str) -> MeetingSummary:
    """Extract MeetingSummary from unstructured text. Missing fields become empty lists."""
    agent = create_agent()
    result = agent(
        f"Extract a meeting or event summary from this text:\n\n{text}",
        structured_output_model=MeetingSummary,
    )
    return result.structured_output


if __name__ == "__main__":
    sample = "Eugene Sim, 28, is an aspiring data engineer based in Singapore."
    print("Sample text:", sample, "\n")
    person = extract_person(sample)
    print("Structured output (PersonInfo):")
    print(f"  name: {person.name}")
    print(f"  age: {person.age}")
    print(f"  occupation: {person.occupation}")
    print(f"  location: {person.location}")
