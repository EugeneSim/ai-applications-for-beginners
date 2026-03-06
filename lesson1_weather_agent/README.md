# Lesson 1: Your First AI Agent — Weather Assistant

**Lesson 1** of [AI Applications for Beginners](../) (repo root). This folder implements the first lesson of the **AWS Strands course**: a simple but powerful AI agent that answers weather questions using live data from an external API. a simple but powerful AI agent that answers weather questions using live data from an external API.

## Concepts

| Concept | What it is |
|--------|------------|
| **System prompt** | `WEATHER_SYSTEM_PROMPT` — the agent’s instructions: personality, capabilities, and steps (e.g. use Open-Meteo, then summarize). |
| **Model** | `LiteLLMModel` — connects the agent to an LLM. Strands uses [LiteLLM](https://docs.litellm.ai/), so you can switch providers (OpenAI, Anthropic, Google, etc.) by changing `model_id` and `client_args`. |
| **Tools** | `http_request` from `strands_tools` — gives the agent the ability to make HTTP requests (e.g. to geocoding and weather APIs). |
| **Agent** | `Agent(system_prompt=..., model=..., tools=[...])` — ties prompt, model, and tools together. |
| **Invocation** | `agent(user_query)` — the agent uses the LLM and tools as needed and returns a final answer. |

## Setup

1. **Create a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # source .venv/bin/activate   # macOS/Linux
   ```

2. **Install dependencies** (from this folder, `lesson1_weather_agent`):
   ```bash
   pip install -r requirements.txt
   ```

3. **API key (shared by all lessons):** Put `GROQ_API_KEY=your-key` in the **repo root** `.env` file (copy root `.env.example` to `.env` once). Free key at [console.groq.com](https://console.groq.com). Never commit `.env`.

## Run

**Interactive chat:**
```bash
cd lesson1_weather_agent
python weather_agent.py
```

**Single question:**
```bash
cd lesson1_weather_agent
python run_example.py
python run_example.py "What's the weather in Berlin?"
```

## Files

- `weather_agent.py` — system prompt, `LiteLLMModel`, `Agent` with `http_request`, and interactive loop.
- `run_example.py` — one-shot run for a single question.
- `README.md` — this file. (API key: use repo root `.env`; see root `.env.example`.)

## Further learning

- [Strands documentation](https://strandsagents.com/)
- [LiteLLM docs](https://docs.litellm.ai/)
