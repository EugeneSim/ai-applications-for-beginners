"""
Lesson 6.1: Agent as Tools.

Orchestrator agent has worker agents as @tool. It routes research, product, and travel
queries to the appropriate specialist and can chain multiple tools for complex questions.
"""

from __future__ import annotations

from strands import Agent, tool

from _shared import get_model

# ---------------------------------------------------------------------------
# Specialist agents (workers)
# ---------------------------------------------------------------------------

RESEARCH_PROMPT = """You are a specialized research assistant. Your sole purpose is to provide factual, well-sourced information. Be concise. Do not recommend products or plan trips—only research and facts."""

PRODUCT_PROMPT = """You are a product recommendation assistant. Give personalized suggestions based on the user's needs (e.g. use case, budget). Mention specific product types or features when helpful. Do not do travel planning or general research."""

TRAVEL_PROMPT = """You are a travel planning assistant. Help with itineraries, destinations, and travel tips. Be practical and concise. Do not recommend specific products to buy or do deep research—focus on travel."""


def _research_agent() -> Agent:
    return Agent(system_prompt=RESEARCH_PROMPT, model=get_model(), tools=[])


def _product_agent() -> Agent:
    return Agent(system_prompt=PRODUCT_PROMPT, model=get_model(), tools=[])


def _travel_agent() -> Agent:
    return Agent(system_prompt=TRAVEL_PROMPT, model=get_model(), tools=[])


# ---------------------------------------------------------------------------
# Expose workers as tools for the orchestrator
# ---------------------------------------------------------------------------


@tool
def research_assistant(query: str) -> str:
    """
    Use for research: factual information, definitions, how things work, technical or general knowledge. Use when the user asks 'what is', 'how does', 'explain', or needs verified facts.
    """
    print("  [Delegating to Research Assistant]")
    return str(_research_agent()(query))


@tool
def product_recommendation_assistant(query: str) -> str:
    """
    Use for product recommendations: what to buy, which product for a use case, gear suggestions (e.g. hiking boots, laptops). Use when the user wants suggestions or comparisons.
    """
    print("  [Delegating to Product Recommendation Assistant]")
    return str(_product_agent()(query))


@tool
def trip_planning_assistant(query: str) -> str:
    """
    Use for travel planning: itineraries, destinations, when to go, what to see, travel tips. Use when the user asks about trips, vacations, or visiting a place.
    """
    print("  [Delegating to Trip Planning Assistant]")
    return str(_travel_agent()(query))


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

ORCHESTRATOR_PROMPT = """You are a master assistant that routes queries to a team of specialized agents.

- For research questions (facts, definitions, how things work) → use research_assistant.
- For product recommendations (what to buy, gear, comparisons) → use product_recommendation_assistant.
- For travel planning (itineraries, destinations, tips) → use trip_planning_assistant.
- For simple general questions → you may answer directly in one sentence.
- If a query needs multiple steps (e.g. "I'm planning a hiking trip to Patagonia and need waterproof boots"), call the relevant assistants in sequence and combine the results.

Always respond with a helpful, combined answer for the user."""


def create_orchestrator_agent() -> Agent:
    """Orchestrator that delegates to research, product, and travel specialists via tools."""
    return Agent(
        system_prompt=ORCHESTRATOR_PROMPT,
        model=get_model(),
        tools=[research_assistant, product_recommendation_assistant, trip_planning_assistant],
    )
