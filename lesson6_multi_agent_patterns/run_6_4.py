"""
Lesson 6.4: Workflow Agent — research pipeline and fact-check.

Usage:
  python run_6_4.py                         # interactive
  python run_6_4.py "Research topic"       # research workflow
  python run_6_4.py "Claim: ..."           # fact-check workflow
"""

import sys

from workflow_agent import run_workflow


def main() -> None:
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        result = run_workflow(user_input)
        report = result.get("report", result.get("query", ""))
        print("\n--- Report ---\n")
        print(report)
        return

    print("Lesson 6.4: Workflow Agent. Research pipeline or fact-check (say 'fact-check: ...' or a topic).")
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
        print("Running workflow...")
        result = run_workflow(user)
        print("\n--- Report ---\n")
        print(result.get("report", ""), "\n")


if __name__ == "__main__":
    main()
