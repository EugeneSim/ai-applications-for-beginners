"""
Lesson 6.1: Run supervisor & workers demo.

Usage:
  python run_supervisor_workers.py              # interactive loop
  python run_supervisor_workers.py "Your question"   # one-shot
"""

import sys
from supervisor_agent import run_supervisor_workers

def main() -> None:
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print("Answer:", run_supervisor_workers(query))
        return

    print("Lesson 6.1: Supervisor & workers. Ask anything; the coordinator will use researcher then writer.")
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
        answer = run_supervisor_workers(user)
        print("Answer:", answer, "\n")

if __name__ == "__main__":
    main()
