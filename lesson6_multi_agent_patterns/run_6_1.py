"""
Lesson 6.1: Agent as Tools — run orchestrator.

Usage:
  python run_6_1.py                    # interactive
  python run_6_1.py "Your question"   # one-shot
"""

import sys

from agent_as_tools import create_orchestrator_agent


def main() -> None:
    agent = create_orchestrator_agent()

    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print("Answer:", agent(query))
        return

    print("Lesson 6.1: Agent as Tools. Orchestrator routes to Research / Product / Travel assistants.")
    print("Type 'quit' or 'exit' to stop.\n")
    while True:
        try:
            user = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user:
            continue
        if user.lower() in ("quit", "exit", "q"):
            break
        print("Thinking...")
        print("Answer:", agent(user), "\n")


if __name__ == "__main__":
    main()
