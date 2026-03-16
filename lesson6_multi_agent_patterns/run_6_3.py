"""
Lesson 6.3: Graph-Based Workflow — run DAG.

Usage:
  python run_6_3.py                      # interactive
  python run_6_3.py "Your research task"  # one-shot
"""

import sys

from graph_workflow import build_example_graph


def main() -> None:
    graph = build_example_graph()

    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
        result = graph.run(task)
        print("\nExecution order:", result["order"])
        print("\nFinal report:\n", result["final"])
        return

    print("Lesson 6.3: Graph-Based Workflow. DAG: research -> analysis, fact_check -> report.")
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
        print("Running graph...")
        result = graph.run(user)
        print("\nExecution order:", result["order"])
        print("\nFinal report:\n", result["final"], "\n")


if __name__ == "__main__":
    main()
