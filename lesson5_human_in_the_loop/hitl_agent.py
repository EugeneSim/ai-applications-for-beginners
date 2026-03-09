"""
Lesson 5: Human-in-the-Loop (HITL) Agent

Implements human-in-the-loop patterns using the Strands interrupt system:
- Approval requests: pause before dangerous operations (e.g. delete_files) and ask for human approval.
- Task completion handoff: interrupt to hand control to the user with context and next steps.

Uses BeforeToolCallEvent hooks to intercept tool calls and event.interrupt() to request
human input; the run loop in run_example.py collects responses and resumes the agent.

API key: GROQ_API_KEY in repo root .env (same as other lessons).
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from strands import Agent, tool
from strands.hooks import BeforeToolCallEvent, HookProvider, HookRegistry
from strands.models.litellm import LiteLLMModel

_REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_REPO_ROOT / ".env")

# ---------------------------------------------------------------------------
# Model config (same as other lessons)
# ---------------------------------------------------------------------------
_MODEL_ID = "groq/llama-3.3-70b-versatile"
_MODEL_PARAMS = {"max_tokens": 1024, "temperature": 0.3}

# ---------------------------------------------------------------------------
# Tools: safe list vs. dangerous delete (approval required via hook)
# ---------------------------------------------------------------------------

# In-memory demo "filesystem" so we don't touch the real disk
_DEMO_FILES: set[str] = set()


@tool
def list_files(directory: str = "") -> list[str]:
    """List file paths in the demo workspace. directory is optional; use '' for root."""
    if not directory:
        return sorted(_DEMO_FILES)
    prefix = directory.rstrip("/") + "/"
    return sorted(p for p in _DEMO_FILES if p == directory or p.startswith(prefix))


@tool
def create_file(path: str, content: str = "") -> str:
    """Create a file in the demo workspace. path must not contain '..'. Returns the path created."""
    if ".." in path or path.startswith("/"):
        return "Error: path must be relative and must not contain '..'"
    _DEMO_FILES.add(path)
    return f"Created: {path}"


@tool
def delete_files(paths: list[str]) -> dict[str, Any]:
    """
    Delete one or more files from the demo workspace.
    This tool is intercepted by the approval hook; the agent will pause for human approval before it runs.
    """
    deleted = []
    for p in paths:
        if p in _DEMO_FILES:
            _DEMO_FILES.discard(p)
            deleted.append(p)
    return {"deleted": deleted, "requested": paths}


# ---------------------------------------------------------------------------
# Approval hook: interrupt before dangerous tools (human-in-the-loop)
# ---------------------------------------------------------------------------

INTERRUPT_NAME_APPROVAL = "hitl-approval"


class ApprovalHook(HookProvider):
    """
    Intercepts BeforeToolCallEvent for selected tools and raises an interrupt
    so the user can approve or deny the operation (e.g. delete_files).
    """

    def __init__(self, app_name: str = "lesson5") -> None:
        self.app_name = app_name
        self._approval_interrupt_name = f"{self.app_name}-{INTERRUPT_NAME_APPROVAL}"

    def register_hooks(self, registry: HookRegistry, **kwargs: Any) -> None:
        registry.add_callback(BeforeToolCallEvent, self._approve)

    def _approve(self, event: BeforeToolCallEvent) -> None:
        if event.tool_use["name"] != "delete_files":
            return

        tool_input = event.tool_use.get("input") or {}
        paths = tool_input.get("paths") or []

        approval = event.interrupt(
            self._approval_interrupt_name,
            reason={"tool": "delete_files", "paths": paths},
        )
        if approval is None:
            return
        # Normalize: allow "y", "yes", "true"; anything else denies
        normalized = str(approval).strip().lower() if approval else ""
        if normalized not in ("y", "yes", "true", "1"):
            event.cancel_tool = "User denied permission to delete files."


# ---------------------------------------------------------------------------
# Task completion handoff: tool that interrupts to hand off to the user
# ---------------------------------------------------------------------------

INTERRUPT_NAME_HANDOFF = "hitl-handoff"


class HandoffHook(HookProvider):
    """
    Optional: intercept a "submit_for_review" or similar tool to pause and
    hand off to the user with next steps (task completion handoff).
    This example uses a dedicated handoff tool that always interrupts.
    """

    def __init__(self, app_name: str = "lesson5") -> None:
        self.app_name = app_name
        self._handoff_interrupt_name = f"{self.app_name}-{INTERRUPT_NAME_HANDOFF}"

    def register_hooks(self, registry: HookRegistry, **kwargs: Any) -> None:
        registry.add_callback(BeforeToolCallEvent, self._handoff)

    def _handoff(self, event: BeforeToolCallEvent) -> None:
        if event.tool_use["name"] != "submit_for_review":
            return

        tool_input = event.tool_use.get("input") or {}
        title = tool_input.get("title", "")
        summary = tool_input.get("summary", "")

        # Interrupt to hand off: user acknowledges and can perform next steps
        event.interrupt(
            self._handoff_interrupt_name,
            reason={
                "tool": "submit_for_review",
                "title": title,
                "summary": summary,
                "next_steps": "Review the content above. Reply with 'ok' to confirm handoff, or add notes for the agent.",
            },
        )
        # We do not cancel the tool; after user responds, the tool runs (e.g. returns success)


@tool
def submit_for_review(title: str, summary: str) -> str:
    """
    Submit content for human review (task completion handoff).
    The agent will pause so you can review the title and summary; after you respond, the handoff is complete.
    """
    return f"Submitted for review: '{title}'. Summary: {summary}"


# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

HITL_SYSTEM_PROMPT = """You are a helpful file assistant with a demo workspace.

Your capabilities:
- list_files: list files in the demo workspace (optional directory argument).
- create_file: create a file with a path and optional content.
- delete_files: delete one or more files. Before this runs, the user will be asked to approve.
- submit_for_review: when the user wants to finalize or hand off (e.g. after drafting content), use this to pause and hand control to the user with the title and summary. After they respond, the handoff is complete.

When the user asks to delete files, use delete_files with the list of paths. The system will pause and ask for approval.
When the user says they want to submit, finalize, or hand off content, use submit_for_review with a title and short summary.
Be concise and clear."""


# ---------------------------------------------------------------------------
# Agent factory
# ---------------------------------------------------------------------------

def _get_api_key() -> str | None:
    key = os.environ.get("GROQ_API_KEY")
    return key.strip() if key else None


def create_hitl_agent() -> Agent:
    """Create a human-in-the-loop agent with approval and handoff hooks."""
    api_key = _get_api_key()
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not set. Add it to the repo root .env file. "
            "Free key at https://console.groq.com"
        )

    model = LiteLLMModel(
        client_args={"api_key": api_key},
        model_id=_MODEL_ID,
        params=_MODEL_PARAMS,
    )

    return Agent(
        model=model,
        system_prompt=HITL_SYSTEM_PROMPT,
        tools=[list_files, create_file, delete_files, submit_for_review],
        hooks=[ApprovalHook("lesson5"), HandoffHook("lesson5")],
    )


# ---------------------------------------------------------------------------
# Interactive loop with interrupt handling (used by run_example.py and main)
# ---------------------------------------------------------------------------

def run_interactive(agent: Agent) -> None:
    """
    Run an interactive chat loop. When the agent raises an interrupt (e.g. approval
    or handoff), prompt the user, collect responses, and resume the agent.
    """
    print(
        "HITL file assistant ready. Create/list/delete files; delete requires approval.\n"
        "Say 'submit for review' to trigger a handoff. Type 'quit' or 'exit' to stop.\n"
    )

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            break

        result = agent(user_input)

        while getattr(result, "stop_reason", None) == "interrupt":
            responses = []
            for interrupt in getattr(result, "interrupts", []) or []:
                name = getattr(interrupt, "name", "")
                reason = getattr(interrupt, "reason", None) or {}
                interrupt_id = getattr(interrupt, "id", "")

                if "lesson5-hitl-approval" in name:
                    paths = reason.get("paths") or []
                    user_response = input(
                        f"Approve delete of {paths!r}? (y/N): "
                    ).strip()
                elif "lesson5-hitl-handoff" in name:
                    next_steps = reason.get("next_steps", "")
                    print(f"\n[Handoff] {next_steps}\n")
                    user_response = input("Reply (e.g. 'ok' or your notes): ").strip()
                else:
                    user_response = input(f"Respond to interrupt '{name}': ").strip()

                responses.append({
                    "interruptResponse": {
                        "interruptId": interrupt_id,
                        "response": user_response,
                    }
                })

            result = agent(responses)

        # Final assistant message (AgentResult.__str__ returns text content or interrupt info)
        print(f"\nAssistant: {result}\n")


def main() -> None:
    """Run interactive HITL loop (interrupt-aware)."""
    agent = create_hitl_agent()
    run_interactive(agent)


if __name__ == "__main__":
    main()
