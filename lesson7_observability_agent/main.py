"""
Lesson 7: Observability Agent

Observability for monitoring and debugging AI agents in production using AWS Strands
with OpenTelemetry tracing and Langfuse integration.

- OpenTelemetry: distributed tracing, metrics, log correlation
- Langfuse: trace visualization, session tracking, performance metrics
- Trace attributes: session.id, user.id, tags for filtering in Langfuse
"""

from __future__ import annotations

import base64
import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from repo root (API keys and Langfuse config)
REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")


# ---------------------------------------------------------------------------
# Environment validation
# ---------------------------------------------------------------------------

def _require_env(name: str) -> str:
    value = (os.environ.get(name) or "").strip()
    if not value:
        raise ValueError(
            f"{name} is not set. Add it to the repo root .env file. "
            "See .env.example and Langfuse dashboard for keys."
        )
    return value


def _setup_langfuse_otel() -> None:
    """Configure OpenTelemetry to export traces to Langfuse OTLP endpoint."""
    public_key = _require_env("LANGFUSE_PUBLIC_KEY")
    secret_key = _require_env("LANGFUSE_SECRET_KEY")
    host = (os.environ.get("LANGFUSE_HOST") or "https://cloud.langfuse.com").strip().rstrip("/")
    endpoint = f"{host}/api/public/otel"
    auth_string = base64.b64encode(f"{public_key}:{secret_key}".encode()).decode()
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = endpoint
    os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {auth_string}"


def _get_model():
    """Return LiteLLM model: Nebius if NEBIUS_API_KEY set, else Groq (same as other lessons)."""
    from strands.models.litellm import LiteLLMModel

    nebius_key = (os.environ.get("NEBIUS_API_KEY") or "").strip()
    if nebius_key:
        return LiteLLMModel(
            client_args={"api_key": nebius_key},
            model_id="nebius/meta-llama/Llama-3.3-70B-Instruct",
            params={"max_tokens": 1024, "temperature": 0.3},
        )
    groq_key = (os.environ.get("GROQ_API_KEY") or "").strip()
    if not groq_key:
        raise ValueError(
            "Set NEBIUS_API_KEY or GROQ_API_KEY in the repo root .env. "
            "See .env.example."
        )
    return LiteLLMModel(
        client_args={"api_key": groq_key},
        model_id="groq/llama-3.3-70b-versatile",
        params={"max_tokens": 1024, "temperature": 0.3},
    )


# ---------------------------------------------------------------------------
# Restaurant Helper Agent with observability
# ---------------------------------------------------------------------------

RESTAURANT_SYSTEM_PROMPT = """You are a friendly restaurant helper for San Francisco and the Bay Area.

Your capabilities:
- Suggest restaurants by neighborhood, cuisine, or vibe.
- Give practical tips: reservations, parking, popular dishes.
- Keep answers concise and useful (a few sentences unless the user asks for more).

If the user asks about a different city or something off-topic, politely steer back to Bay Area dining or offer to help with that instead."""


def create_observability_agent():
    """Create agent with OpenTelemetry + Langfuse tracing and custom trace attributes."""
    # Ensure Langfuse OTLP env vars are set before Strands telemetry reads them
    _setup_langfuse_otel()

    from strands import Agent
    from strands.telemetry import StrandsTelemetry

    # Configure OpenTelemetry: export traces to Langfuse via OTLP
    strands_telemetry = StrandsTelemetry()
    strands_telemetry.setup_otlp_exporter()

    model = _get_model()

    # Trace attributes show up in Langfuse for filtering and session tracking
    agent = Agent(
        model=model,
        system_prompt=RESTAURANT_SYSTEM_PROMPT,
        tools=[],
        trace_attributes={
            "session.id": "lesson7-demo-session",
            "user.id": "lesson7-demo@example.com",
            "tags": ["production", "restaurant-bot"],
        },
    )
    return agent


def main():
    print("Initializing Restaurant Helper Agent with observability...")
    agent = create_observability_agent()
    print("🤖 Restaurant Helper Agent initialized with observability!")
    print("📊 All interactions will be traced and monitored in Langfuse.")
    print("-" * 60)

    demo_message = "Hi, where can I eat in San Francisco?"
    print(f"👤 User: {demo_message}")
    response = agent(demo_message)
    print(f"🤖 Restaurant Helper: {response}")
    print("-" * 60)
    print("The interaction was captured in Langfuse for monitoring and analysis.")


if __name__ == "__main__":
    main()
