"""
Lesson 6.2: Swarm Intelligence — run decentralized handoff.

Usage:
  python run_6_2.py                     # interactive
  python run_6_2.py "Your task"        # one-shot
"""

import sys

from swarm_agents import run_swarm


def main() -> None:
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
        result = run_swarm(task)
        print("\nPath:", " -> ".join(result.path))
        print("Handoffs:", result.handoff_count)
        print("\nAnswer:", result.final_text)
        return

    print("Lesson 6.2: Swarm. Agents (researcher, architect, coder, reviewer) hand off with no central orchestrator.")
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
        print("Running swarm...")
        result = run_swarm(user)
        print("\nPath:", " -> ".join(result.path))
        print("Handoffs:", result.handoff_count)
        print("\nAnswer:", result.final_text, "\n")


if __name__ == "__main__":
    main()
