"""
Lesson 2: Session state and agent memory

Traditionally agents are stateless: each request has no memory of past turns.
This lesson gives the agent memory by persisting conversation history per session.

- FileSessionManager creates a folder per session_id; each message is saved
  as a separate JSON file in that folder.
- With an existing session_id, the manager loads those JSON files to reconstruct
  the conversation before processing the new query.

Demo: say "I am Eugene Sim", then in a later run (same session_id) ask
"Do you know who I am?" — the agent should remember.

API key: GROQ_API_KEY in repo root .env (same as Lesson 1).
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from strands import Agent
from strands.models.litellm import LiteLLMModel
from strands.session.file_session_manager import FileSessionManager

_repo_root = Path(__file__).resolve().parent.parent
load_dotenv(_repo_root / ".env")

# ---------------------------------------------------------------------------
# System prompt: agent that remembers who the user is (and other facts)
# ---------------------------------------------------------------------------
MEMORY_SYSTEM_PROMPT = """You are a friendly assistant with a good memory.

When the user tells you their name or other facts about themselves, remember it.
If they ask "Do you know who I am?" or similar, use what they told you earlier
in this conversation to answer. Be concise and natural."""


def _get_api_key():
    """Read Groq API key from environment (from .env if present). Never commit .env."""
    key = os.environ.get("GROQ_API_KEY")
    return (key or "").strip() or None


def create_session_agent(session_id: str, storage_dir: str | Path | None = None) -> Agent:
    """
    Create an agent with persistent session state.

    Args:
        session_id: Unique id for this conversation (e.g. user or chat id).
        storage_dir: Directory for session folders; defaults to ./sessions
            next to this script.

    Returns:
        An Agent that loads existing messages for this session_id and
        persists new messages as JSON files.
    """
    if storage_dir is None:
        storage_dir = Path(__file__).resolve().parent / "sessions"
    storage_dir = Path(storage_dir)
    storage_dir.mkdir(parents=True, exist_ok=True)

    session_manager = FileSessionManager(
        session_id=session_id,
        storage_dir=str(storage_dir),
    )

    api_key = _get_api_key()
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not set. Add it to the repo root .env file. "
            "Free key at https://console.groq.com"
        )

    model = LiteLLMModel(
        client_args={"api_key": api_key},
        model_id="groq/llama-3.3-70b-versatile",
        params={"max_tokens": 512, "temperature": 0.3},
    )

    # callback_handler=None so we print the response once ourselves (avoids duplicate output)
    agent = Agent(
        model=model,
        system_prompt=MEMORY_SYSTEM_PROMPT,
        session_manager=session_manager,
        callback_handler=None,
    )
    return agent


def main() -> None:
    """Interactive chat loop; session_id from argv or default."""
    session_id = sys.argv[1] if len(sys.argv) > 1 else "default-session"
    agent = create_session_agent(session_id)
    print(f"Session: {session_id}. Your messages are saved so I can remember you.")
    print("Try: 'I am Eugene Sim', then later ask 'Do you know who I am?'")
    print("Type 'quit' or 'exit' to stop.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            break

        response = agent(user_input)
        print(f"\nAssistant: {response}\n")


if __name__ == "__main__":
    main()
