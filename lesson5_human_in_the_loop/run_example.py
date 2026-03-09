"""
Run the Human-in-the-Loop agent: interactive only.

  python run_example.py

When you ask the agent to delete files, it will pause and ask for your approval (y/N).
When you say "submit for review" (or similar), it will hand off to you with next steps.

Requires GROQ_API_KEY in repo root .env.
"""

import sys

from hitl_agent import create_hitl_agent, run_interactive


def main() -> None:
    try:
        agent = create_hitl_agent()
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    run_interactive(agent)


if __name__ == "__main__":
    main()
