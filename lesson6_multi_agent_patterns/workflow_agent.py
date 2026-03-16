"""
Lesson 6.4: Workflow Agent.

Stateful sequential workflow: Researcher -> Analyst -> Writer.
Two modes: research pipeline (topic research + report) and fact-check pipeline (claim verification).
"""

from __future__ import annotations

from strands import Agent

from _shared import get_model

# ---------------------------------------------------------------------------
# Specialized agents for the workflow
# ---------------------------------------------------------------------------

RESEARCHER_PROMPT = """You are a Researcher Agent that gathers information.
1. Determine if the input is a research query (broad topic) or a factual claim to verify.
2. For research: find key facts and concepts; keep under 400 words.
3. For fact-check: find evidence for or against the claim; include source-like references; keep under 400 words.
Do not add verdicts or final conclusions—only gathered information."""

ANALYST_PROMPT = """You are an Analyst Agent that verifies and interprets information.
1. For factual claims: rate accuracy (1-5), note corrections if needed, summarize evidence.
2. For research queries: identify 3-5 key insights and evaluate reliability.
Keep analysis under 300 words."""

WRITER_PROMPT = """You are a Report Writer. Create a structured, readable report.
1. For research: intro, key points, brief conclusion.
2. For fact-check: claim, verdict (TRUE/FALSE/PARTIALLY TRUE), confidence, evidence summary.
Keep under 400 words. Be clear and concise."""


def _agent(system_prompt: str) -> Agent:
    return Agent(system_prompt=system_prompt, model=get_model(), tools=[])


def _researcher() -> Agent:
    return _agent(RESEARCHER_PROMPT)


def _analyst() -> Agent:
    return _agent(ANALYST_PROMPT)


def _writer() -> Agent:
    return _agent(WRITER_PROMPT)


# ---------------------------------------------------------------------------
# Workflows
# ---------------------------------------------------------------------------

def run_research_workflow(user_input: str) -> dict[str, str]:
    """Research pipeline: topic -> research -> analysis -> report."""
    researcher = _researcher()
    analyst = _analyst()
    writer = _writer()

    research_msg = f"Research: '{user_input}'. Gather key facts and concepts."
    print("  [Researcher] running...")
    research_response = researcher(research_msg)

    analysis_msg = f"Analyze these findings about '{user_input}':\n\n{research_response}"
    print("  [Analyst] running...")
    analyst_response = analyst(analysis_msg)

    report_msg = f"Create a report on '{user_input}' based on:\n\n{analyst_response}"
    print("  [Writer] running...")
    report_response = writer(report_msg)

    return {
        "query": user_input,
        "research": str(research_response),
        "analysis": str(analyst_response),
        "report": str(report_response),
    }


def run_fact_check_workflow(claim: str) -> dict[str, str]:
    """Fact-check pipeline: claim -> research evidence -> analysis -> fact-check report."""
    researcher = _researcher()
    analyst = _analyst()
    writer = _writer()

    research_msg = f"Fact-check: '{claim}'. Find evidence for and against this claim."
    print("  [Researcher] running...")
    research_response = researcher(research_msg)

    analysis_msg = f"Analyze evidence for: '{claim}'\n\nResearch: {research_response}\n\nProvide verdict (TRUE/FALSE/PARTIALLY TRUE), confidence level, and evidence summary."
    print("  [Analyst] running...")
    analyst_response = analyst(analysis_msg)

    report_msg = f"Create fact-check report for: '{claim}'\n\nAnalysis: {analyst_response}"
    print("  [Writer] running...")
    report_response = writer(report_msg)

    return {
        "claim": claim,
        "research": str(research_response),
        "analysis": str(analyst_response),
        "report": str(report_response),
    }


def run_workflow(user_input: str) -> dict[str, str]:
    """
    Conditional routing: if input looks like a fact claim, run fact-check; else research.
    """
    lower = user_input.lower().strip()
    if "fact-check" in lower or "fact check" in lower or "is it true that" in lower or lower.startswith("claim:"):
        return run_fact_check_workflow(user_input)
    return run_research_workflow(user_input)
