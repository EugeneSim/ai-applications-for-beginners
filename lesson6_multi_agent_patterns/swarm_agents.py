"""
Lesson 6.2: Swarm Intelligence.

Decentralized collaboration: no central orchestrator. Each agent can hand off to another.
We use a simple protocol: agent may end with "HANDOFF:agent_id:message" to pass to the next specialist.
"""

from __future__ import annotations

import re
from typing import NamedTuple

from strands import Agent

from _shared import get_model

# Handoff format: last line "HANDOFF:agent_id:rest of line is message"
HANDOFF_PATTERN = re.compile(r"\nHANDOFF:(\w+):(.+)$", re.DOTALL)

# ---------------------------------------------------------------------------
# Swarm members: distinct roles, can hand off to each other
# ---------------------------------------------------------------------------

SWARM_INSTRUCTION = """
If the task is complete, reply with your final answer and do not add HANDOFF.
If another specialist should continue, end your reply with exactly one line:
HANDOFF:agent_id:your message for them
where agent_id is one of: researcher, architect, coder, reviewer.
"""

RESEARCHER_PROMPT = """You are a Researcher. You discover requirements, gather information, and identify constraints. Output a short research note. When design or implementation is needed, hand off to architect or coder.""" + SWARM_INSTRUCTION

ARCHITECT_PROMPT = """You are an Architect. You design structure, APIs, and high-level approach. Output a short design. When implementation or review is needed, hand off to coder or reviewer.""" + SWARM_INSTRUCTION

CODER_PROMPT = """You are a Coder. You implement concrete steps or code. Output concise implementation notes or code snippets. When review or more research is needed, hand off to reviewer or researcher.""" + SWARM_INSTRUCTION

REVIEWER_PROMPT = """You are a Reviewer. You check quality, suggest improvements, and summarize. Output a short review. Prefer to complete the task; only hand off if significant rework or another step is clearly needed.""" + SWARM_INSTRUCTION


def _make_agent(name: str, system_prompt: str) -> Agent:
    return Agent(system_prompt=system_prompt, model=get_model(), tools=[])


def create_swarm_agents() -> dict[str, Agent]:
    return {
        "researcher": _make_agent("researcher", RESEARCHER_PROMPT),
        "architect": _make_agent("architect", ARCHITECT_PROMPT),
        "coder": _make_agent("coder", CODER_PROMPT),
        "reviewer": _make_agent("reviewer", REVIEWER_PROMPT),
    }


class HandoffResult(NamedTuple):
    """Result of running the swarm."""
    final_text: str
    path: list[str]  # agent ids in order
    handoff_count: int


def run_swarm(
    task: str,
    *,
    entry_point: str = "researcher",
    max_handoffs: int = 5,
) -> HandoffResult:
    """
    Run the swarm: start at entry_point, then follow HANDOFF:agent_id:message until
    no handoff or max_handoffs.
    """
    agents = create_swarm_agents()
    if entry_point not in agents:
        raise ValueError(f"Unknown entry_point: {entry_point}. Choose from {list(agents.keys())}")

    path: list[str] = []
    current_agent_id = entry_point
    current_input = task
    handoff_count = 0

    last_text = ""
    for _ in range(max_handoffs + 1):
        agent = agents[current_agent_id]
        path.append(current_agent_id)
        print(f"  [{current_agent_id}] running...")
        result = agent(current_input)
        text = str(result).strip()
        last_text = text

        match = HANDOFF_PATTERN.search(text)
        if not match:
            return HandoffResult(final_text=text, path=path, handoff_count=handoff_count)

        next_id = match.group(1).lower()
        next_message = match.group(2).strip()
        if next_id not in agents:
            return HandoffResult(final_text=text[: match.start()].strip() if match else text, path=path, handoff_count=handoff_count)

        handoff_count += 1
        current_agent_id = next_id
        current_input = next_message
        print(f"  -> handoff to {next_id}")

    # Max handoffs reached; return last agent output (strip HANDOFF line if present)
    if HANDOFF_PATTERN.search(last_text):
        last_text = HANDOFF_PATTERN.sub("", last_text).strip()
    return HandoffResult(final_text=last_text, path=path, handoff_count=handoff_count)
