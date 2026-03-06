"""
Lesson 1: Your First AI Agent — Weather Assistant

This script demonstrates the core concepts of the AWS Strands SDK:
- Agent creation and system prompt
- Model configuration (LiteLLM → any supported LLM)
- Tool usage (http_request for live weather API)

API key: set GROQ_API_KEY in the repo root .env (shared by all lessons) or in your
environment. Free key at https://console.groq.com. Never commit .env.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

from strands import Agent
from strands.models.litellm import LiteLLMModel
from strands_tools import http_request

# Load .env from repo root only (same key reused across all lessons)
_repo_root = Path(__file__).resolve().parent.parent
load_dotenv(_repo_root / ".env")

# ---------------------------------------------------------------------------
# System prompt: the agent's "constitution"
# Defines personality, capabilities, and step-by-step behavior.
# ---------------------------------------------------------------------------
WEATHER_SYSTEM_PROMPT = """You are a friendly, accurate weather assistant.

Your capabilities:
- You can fetch live weather data using the http_request tool.
- Use the free Open-Meteo API (no API key required).

When the user asks about weather:

1. If they mention a city or place:
   - First get coordinates: GET https://geocoding-api.open-meteo.com/v1/search?name=PLACE&count=1
   - From the JSON response, take latitude and longitude of the first result.
   - Then get weather: GET https://api.open-meteo.com/v1/forecast?latitude=LAT&longitude=LON&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m
   - weather_code can be looked up at https://open-meteo.com/en/docs (e.g. 0=clear, 1–3=clouds, 61–67=rain).

2. If they give latitude and longitude, call the forecast URL directly with those values.

3. Summarize the current conditions in a short, helpful reply (temperature, humidity, wind, and a brief description of the weather).
   Use Celsius and km/h unless the user asks otherwise.

If the user's message is not about weather, politely say you are a weather assistant and offer to help with a location.
"""


def _get_api_key():
    """Read Groq API key from environment (loaded from .env if present). Never commit .env."""
    key = os.environ.get("GROQ_API_KEY")
    if key:
        key = key.strip()
    return key or None


def create_weather_agent():
    """Create and return a weather agent with model and tools."""
    api_key = _get_api_key()
    if not api_key:
        raise ValueError(
            "Groq API key not set. Add GROQ_API_KEY=... to the repo root .env file. "
            "Free key at https://console.groq.com"
        )

    # Llama 3.3 70B via Groq (free tier). Fast inference, 14,400 req/day.
    model = LiteLLMModel(
        client_args={"api_key": api_key},
        model_id="groq/llama-3.3-70b-versatile",
        params={"max_tokens": 1024, "temperature": 0.3},
    )

    # Agent: system prompt + model + tools (http_request = ability to call APIs)
    agent = Agent(
        model=model,
        system_prompt=WEATHER_SYSTEM_PROMPT,
        tools=[http_request],
    )
    return agent


def main():
    agent = create_weather_agent()
    print("Weather assistant ready. Ask about the weather (e.g. 'What's the weather in Paris?').")
    print("Type 'quit' or 'exit' to stop.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            break

        # Invocation: agent(query) → LLM reasons, uses tools, returns answer
        response = agent(user_input)
        print(f"\nAssistant: {response}\n")


if __name__ == "__main__":
    main()
