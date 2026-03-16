# AI Applications for Beginners

This repo contains multiple lessons from the **AWS Strands course**, each in its own folder. Every lesson is self-contained with its own code and dependencies.

## Security (safe for public GitHub)

This repo is designed to be shared publicly. **Secrets must never be committed.**

- **Secrets only in `.env`.** All API keys and credentials are read from the **repo root** `.env` file, which is **gitignored**. Only [`.env.example`](.env.example) (placeholders, no real values) is tracked.
- **No keys in code.** Every lesson uses `os.environ.get(...)` only; there are no hardcoded API keys, tokens, or passwords in the codebase.
- **Environment variables used** (set in `.env` at repo root; see `.env.example`):
  - `GROQ_API_KEY` — used by Lessons 1–6 (and Lesson 7 fallback). [Get a key](https://console.groq.com).
  - `TAVILY_API_KEY` — Lesson 4 only (multi-server / web search). [Get a key](https://tavily.com).
  - `NEBIUS_API_KEY` — optional; Lesson 7 (and others) can use Nebius instead of Groq.
  - `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST` — Lesson 7 only (observability). [Get keys](https://cloud.langfuse.com).

**Before every push (especially before making the repo public):**

1. Run `git status` and confirm **`.env` is not staged**.
2. Run `git diff --cached` and ensure no real keys or secrets appear in staged files.
3. Do not run `git add -f .env` or force-add any ignored file that might contain secrets.

## Repo structure

| Lesson | Folder | Description |
|--------|--------|-------------|
| **Lesson 1** | [lesson1_weather_agent/](lesson1_weather_agent/) | Your first AI agent — weather assistant (system prompt, model, `http_request` tool). |
| **Lesson 2** | [lesson2_sessions_state/](lesson2_sessions_state/) | Sessions & state — agent with memory via `FileSessionManager` (`session_id`, `storage_dir`). |
| **Lesson 3** | [lesson3_structured_output/](lesson3_structured_output/) | Structured output — extract typed data (Pydantic) from text via `structured_output_model`. |
| **Lesson 4** | [lesson4_mcp_tools/](lesson4_mcp_tools/) | Extending agents with external tools (MCP) — dynamic tool discovery, AWS docs server, error handling. |
| **Lesson 5** | [lesson5_human_in_the_loop/](lesson5_human_in_the_loop/) | Human-in-the-loop (HITL) — approval requests and task handoffs via Strands interrupts and hooks. |
| **Lesson 6** | [lesson6_multi_agent_patterns/](lesson6_multi_agent_patterns/) | Multi-agent patterns: 6.1 Agent as Tools, 6.2 Swarm, 6.3 Graph-Based Workflows, 6.4 Workflow Agent. |
| **Lesson 7** | [lesson7_observability_agent/](lesson7_observability_agent/) | Observability — OpenTelemetry + Langfuse tracing, monitoring, and debugging for production agents. |
| **Lesson 8** | [lesson8_safety_guardrails/](lesson8_safety_guardrails/) | Safety guardrails — input validation and blocking via Strands hooks (BeforeInvocationEvent), configurable rules, risk assessment. |

Each lesson folder has its own **`requirements.txt`**, **code**, and **README** — install and run from inside that folder.

## Quick start (Lesson 1)

```bash
# Once: copy .env.example to .env at repo root and set GROQ_API_KEY (get one at https://console.groq.com)
copy .env.example .env
# Then run Lesson 1:
cd lesson1_weather_agent
pip install -r requirements.txt
python weather_agent.py
```

- **Lesson 1:** [README](lesson1_weather_agent/README.md) — weather agent
- **Lesson 2:** [README](lesson2_sessions_state/README.md) — sessions & state (agent memory)
- **Lesson 3:** [README](lesson3_structured_output/README.md) — structured output (Pydantic schemas)
- **Lesson 4:** [README](lesson4_mcp_tools/README.md) — extending agents with MCP (external tools)
- **Lesson 5:** [README](lesson5_human_in_the_loop/README.md) — human-in-the-loop (approval & handoff)
- **Lesson 6:** [README](lesson6_multi_agent_patterns/README.md) — multi-agent patterns (Agent as Tools, Swarm, Graph, Workflow)
- **Lesson 7:** [README](lesson7_observability_agent/README.md) — observability (OpenTelemetry, Langfuse)
- **Lesson 8:** [README](lesson8_safety_guardrails/README.md) — safety guardrails (hooks, input validation)

## Further learning

- [Strands documentation](https://strandsagents.com/)
- [LiteLLM docs](https://docs.litellm.ai/)
