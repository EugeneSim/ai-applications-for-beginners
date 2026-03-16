"""
Lesson 6: End-to-end test — runs all four sub-lessons (6.1–6.4) with sample inputs.

Requires: GROQ_API_KEY in repo root .env (same as other lessons).

Usage:
  python run_all_e2e.py         # run all four patterns (takes a few minutes)
  python run_all_e2e.py --quick # shorter prompts, fewer handoffs (faster)
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Ensure we can import from this folder
sys.path.insert(0, str(Path(__file__).resolve().parent))

SEP = "=" * 60


def check_env() -> None:
    from _shared import REPO_ROOT
    from dotenv import load_dotenv
    load_dotenv(REPO_ROOT / ".env")
    if not (os.environ.get("GROQ_API_KEY") or "").strip():
        print("ERROR: GROQ_API_KEY not set. Copy repo root .env.example to .env and set your key.")
        sys.exit(1)


def run_6_1(query: str) -> str:
    """6.1 Agent as Tools: orchestrator delegates to research/product/travel."""
    from agent_as_tools import create_orchestrator_agent
    agent = create_orchestrator_agent()
    return str(agent(query))


def run_6_2(task: str, max_handoffs: int = 5) -> tuple[str, list[str], int]:
    """6.2 Swarm: decentralized handoffs. Returns (final_text, path, handoff_count)."""
    from swarm_agents import run_swarm
    result = run_swarm(task, entry_point="researcher", max_handoffs=max_handoffs)
    return result.final_text, result.path, result.handoff_count


def run_6_3(task: str) -> tuple[list[str], str]:
    """6.3 Graph: DAG research -> analysis, fact_check -> report. Returns (order, final)."""
    from graph_workflow import build_example_graph
    graph = build_example_graph()
    result = graph.run(task)
    return result["order"], result["final"]


def run_6_4_research(topic: str) -> str:
    """6.4 Workflow: research pipeline. Returns report text."""
    from workflow_agent import run_research_workflow
    result = run_research_workflow(topic)
    return result.get("report", "")


def run_6_4_factcheck(claim: str) -> str:
    """6.4 Workflow: fact-check pipeline. Returns report text."""
    from workflow_agent import run_fact_check_workflow
    result = run_fact_check_workflow(claim)
    return result.get("report", "")


def main() -> None:
    quick = "--quick" in sys.argv
    check_env()

    print("\nLesson 6 — End-to-end test (all four patterns)\n")

    # --- 6.1 Agent as Tools ---
    print(f"\n{SEP}\n6.1 Agent as Tools\n{SEP}")
    q1 = "What is IAM in AWS? One short paragraph." if quick else "What is IAM in AWS and when would I use it?"
    print(f"Query: {q1}\n")
    try:
        out1 = run_6_1(q1)
        print("Answer:", out1[:500] + ("..." if len(out1) > 500 else ""))
        print("\n[6.1 OK]")
    except Exception as e:
        print(f"[6.1 FAIL] {e}")

    # --- 6.2 Swarm ---
    print(f"\n{SEP}\n6.2 Swarm Intelligence\n{SEP}")
    q2 = "List 3 steps to design a simple REST API." if quick else "Outline a simple REST API for a todo list: main endpoints and one sentence each."
    print(f"Task: {q2}\n")
    try:
        text2, path2, handoffs2 = run_6_2(q2, max_handoffs=3 if quick else 5)
        print("Path:", " -> ".join(path2))
        print("Handoffs:", handoffs2)
        print("Answer:", text2[:500] + ("..." if len(text2) > 500 else ""))
        print("\n[6.2 OK]")
    except Exception as e:
        print(f"[6.2 FAIL] {e}")

    # --- 6.3 Graph ---
    print(f"\n{SEP}\n6.3 Graph-Based Workflow\n{SEP}")
    q3 = "Benefits of version control in 2 sentences." if quick else "What are the main benefits of version control for software teams?"
    print(f"Topic: {q3}\n")
    try:
        order3, final3 = run_6_3(q3)
        print("Execution order:", order3)
        print("Final report:", final3[:500] + ("..." if len(final3) > 500 else ""))
        print("\n[6.3 OK]")
    except Exception as e:
        print(f"[6.3 FAIL] {e}")

    # --- 6.4 Workflow (research + fact-check) ---
    print(f"\n{SEP}\n6.4 Workflow Agent\n{SEP}")
    q4_research = "Benefits of automated testing." if quick else "Key benefits of automated testing in software development."
    print(f"Research topic: {q4_research}\n")
    try:
        report4 = run_6_4_research(q4_research)
        print("Report:", report4[:500] + ("..." if len(report4) > 500 else ""))
        print("\n[6.4 research OK]")
    except Exception as e:
        print(f"[6.4 research FAIL] {e}")

    q4_claim = "Python was first released in 1991."
    print(f"\nFact-check claim: {q4_claim}\n")
    try:
        report4fc = run_6_4_factcheck(q4_claim)
        print("Fact-check report:", report4fc[:500] + ("..." if len(report4fc) > 500 else ""))
        print("\n[6.4 fact-check OK]")
    except Exception as e:
        print(f"[6.4 fact-check FAIL] {e}")

    print(f"\n{SEP}\nE2E run finished. Check [6.x OK] / [6.x FAIL] above.\n{SEP}\n")


if __name__ == "__main__":
    main()
