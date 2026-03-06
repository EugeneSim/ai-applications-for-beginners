"""
Lesson 2 demo: agent memory via session state.

Shows that the agent remembers across runs when using the same session_id.
Run once with "I am Eugene Sim", then run again with "Do you know who I am?"
using the same session_id — the agent recalls your name from stored JSON.

Usage:
  python run_example.py
  python run_example.py "I am Eugene Sim"
  python run_example.py "Do you know who I am?"
  python run_example.py --session my-session "Do you know who I am?"
"""

import argparse

from session_agent import create_session_agent

DEMO_SESSION_ID = "eugene-demo"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the session agent (memory demo). Same session_id = same conversation.",
    )
    parser.add_argument(
        "message",
        nargs="?",
        default=None,
        help="Single message to send (optional; without it, runs interactive).",
    )
    parser.add_argument(
        "--session",
        "-s",
        default=DEMO_SESSION_ID,
        help=f"Session ID (default: {DEMO_SESSION_ID}). Same ID = shared memory.",
    )
    args = parser.parse_args()

    agent = create_session_agent(args.session)

    if args.message is not None:
        print(f"Session: {args.session}")
        print(f"You: {args.message}\n")
        response = agent(args.message)
        print(f"Assistant: {response}\n")
        return

    print(f"Session: {args.session}. Messages persisted as JSON in sessions/.")
    print("Example: say 'I am Eugene Sim', exit, then run again and ask 'Do you know who I am?'\n")
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
