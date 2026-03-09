"""
Lesson 6.1: Supervisor & workers

Orchestrator (Python code) delegates to two specialist agents:
- Researcher: answers factual / technical questions.
- Writer: turns the research into a short, clear answer for the user.

The "supervisor" here is the run loop that calls researcher then writer in sequence.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from strands import Agent
from strands.models.litellm import LiteLLMModel

_REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_REPO_ROOT / ".env")

_MODEL_ID = "groq/llama-3.3-70b-versatile"
_MODEL_PARAMS = {"max_tokens": 1024, "temperature": 0.3}

RESEARCHER_PROMPT = """You are a researcher. Your job is to gather accurate, factual information on the user's topic.

- Answer based on general knowledge and best practices.
- Be concise but complete. Output a short research note (a few sentences or bullets) that a writer can use to draft a final answer.
- Do not add intros like "Here is the research" — just the content."""

WRITER_PROMPT = """You are a writer. You receive a research note and turn it into a clear, friendly answer for the end user.

- Write in a helpful, conversational tone.
- Keep the final answer short (a few sentences).
- Do not repeat the raw research; synthesize it into a coherent reply."""


def _model() -> LiteLLMModel:
    api_key = os.environ.get("GROQ_API_KEY") or ""
    if not api_key.strip():
        raise ValueError("GROQ_API_KEY not set. Add it to the repo root .env file.")
    return LiteLLMModel(
        client_args={"api_key": api_key.strip()},
        model_id=_MODEL_ID,
        params=_MODEL_PARAMS,
    )


def create_researcher_agent() -> Agent:
    """Specialist agent: research only, no tools."""
    return Agent(
        system_prompt=RESEARCHER_PROMPT,
        model=_model(),
        tools=[],
    )


def create_writer_agent() -> Agent:
    """Specialist agent: write from research note, no tools."""
    return Agent(
        system_prompt=WRITER_PROMPT,
        model=_model(),
        tools=[],
    )


def run_supervisor_workers(user_query: str) -> str:
    """
    Supervisor pattern: orchestrate researcher and writer.
    1. Researcher produces a research note from the user query.
    2. Writer produces the final answer from the research note.
    """
    researcher = create_researcher_agent()
    writer = create_writer_agent()

    research_result = researcher(user_query)
    research_text = str(research_result).strip()
    if not research_text:
        research_text = "(No research content returned.)"

    writer_input = f"Research note:\n{research_text}\n\nWrite a short answer for the user based on this."
    writer_result = writer(writer_input)
    return str(writer_result).strip()
