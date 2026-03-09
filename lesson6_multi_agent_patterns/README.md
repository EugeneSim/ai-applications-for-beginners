# Lesson 6: Orchestrating Multiple Agents

**Lesson 6** of [AI Applications for Beginners](../). You'll go beyond a single agent and learn how to **compose and orchestrate multiple agents** so they work together toward a goal. This lesson introduces patterns you can use to build more capable systems while keeping responsibilities clear and behaviour predictable.

## What You'll Learn

- How to **decompose a task** and assign sub-tasks to specialist agents (supervisor–worker pattern)
- Using **agents as tools**: one agent invokes another as a tool for specialised work
- Building **sequential pipelines** where agents run in a fixed order (e.g. draft → review → format)
- **Conditional routing**: choosing which agent(s) to run based on the request or previous output
- When to use each pattern and the **trade-offs** (centralised vs decentralised, fixed vs dynamic)

## Prerequisites

- Lessons 1–5 (especially agents, tools, sessions, and human-in-the-loop)
- Python 3.x with dependencies from this lesson
- `GROQ_API_KEY` in the repo root `.env`

## Patterns at a Glance

| Pattern | Idea | Best for | Trade-off |
|--------|------|----------|-----------|
| **Supervisor & workers** | One coordinator breaks the task into steps and delegates to specialist agents | Content pipelines, support triage, research workflows | Clear ownership; coordinator can be a bottleneck |
| **Agents as tools** | An agent has “tools” that are other agents; it decides when to call them | Research assistants that can “ask the code agent” or “ask the writer” | Flexible; need good tool descriptions so the caller chooses wisely |
| **Sequential pipeline** | Agents run in a fixed order (A → B → C) with explicit handoffs | Data pipelines, approval flows, repeatable workflows | Predictable and auditable; less adaptive |
| **Conditional routing** | A router inspects the request (or state) and invokes one or more agents accordingly | Triage, branching workflows, “send to expert” | Adaptive; routing logic must stay simple and maintainable |

## Concepts

| Concept | What it is |
|--------|------------|
| **Orchestrator** | An agent or small program that decides *which* agent runs next and passes context (e.g. user message, previous replies). |
| **Supervisor** | Orchestrator that decomposes a high-level task into sub-tasks and delegates each to a specialist (worker) agent. |
| **Agent as tool** | Wrapping an agent call in a Strands `@tool` so another agent can “invoke” it by name; the LLM chooses when to use the tool. |
| **Pipeline** | A fixed sequence of agent (or processing) steps; output of step N is input to step N+1. |
| **Router** | Logic (agent or code) that chooses which agent(s) to run based on input type, keywords, or structured rules. |

## Sub-Lessons

| Part | Topic | Description | Complexity | Example use case |
|------|--------|-------------|------------|------------------|
| **6.1** | Supervisor & workers | Build a coordinator that breaks a task into steps and delegates to specialist agents (e.g. researcher, writer) | ⭐⭐ | Content creation, support triage |
| **6.2** | Agents as tools | Implement an agent whose tools are other agents; the main agent decides when to call each specialist | ⭐⭐ | Research assistant with “code” and “writer” tools |
| **6.3** | Sequential pipeline | Chain agents in a fixed order with clear handoffs (e.g. draft → review → format) | ⭐⭐⭐ | Data pipelines, approval workflows |
| **6.4** | Conditional routing | Router that picks the right agent(s) based on the user request or previous output | ⭐⭐⭐ | Triage, branching workflows |

Each part includes runnable code, setup steps, and suggestions for extending the pattern.

## Quick Start

From the lesson folder:

```bash
cd lesson6_multi_agent_patterns
pip install -r requirements.txt
```

Then run the example for the part you’re on (e.g. 6.1):

```bash
python run_supervisor_workers.py
```

Details and one-shot vs interactive usage are in each sub-lesson section below.

## Demo (6.1 — Supervisor & workers)

1. **Interactive**  
   The supervisor agent receives a high-level request (e.g. “Explain how S3 encryption works and give a short example”). It plans steps, then delegates to a “researcher” agent and a “writer” agent, and combines the results.

2. **One-shot**  
   ```bash
   python run_supervisor_workers.py "What is IAM and how do I create a user?"
   ```

*(6.2–6.4 demos will be added as those parts are implemented.)*

## Files

| File | Description |
|------|-------------|
| `README.md` | This file — overview, concepts, and sub-lesson plan. |
| `requirements.txt` | Dependencies (Strands, LiteLLM, python-dotenv). |
| `run_supervisor_workers.py` | Entrypoint for 6.1: supervisor + worker agents. |
| `supervisor_agent.py` | Supervisor and worker agent definitions for 6.1. |

*(Additional files for 6.2–6.4 will appear as those sub-lessons are added.)*

## Setup

1. **Virtual environment** (recommended):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # source .venv/bin/activate   # macOS/Linux
   ```

2. **Dependencies** (from this folder):

   ```bash
   pip install -r requirements.txt
   ```

3. **API key**  
   Put `GROQ_API_KEY=...` in the **repo root** `.env` file. Do not commit `.env`.

## Choosing a Pattern

- **Single, open-ended question** → One agent (or agent with many tools) is often enough.
- **Clear steps (research then write, or draft then review)** → Supervisor & workers or a sequential pipeline.
- **“Sometimes I need a coder, sometimes a writer”** → Agents as tools, or conditional routing.
- **Strict, repeatable process (compliance, audits)** → Sequential pipeline with fixed stages.
- **Triage or branching by topic** → Conditional routing.

## Best Practices

- Give each specialist agent a **narrow, clear system prompt** so it stays on task.
- When using agents as tools, write **precise tool descriptions** so the caller agent knows when to invoke each specialist.
- Keep **orchestrator logic simple**: if the “router” or “supervisor” becomes too complex, consider splitting or simplifying.
- Reuse **session or conversation context** when passing work between agents so the next agent has enough background.

## Further Learning

- [Strands documentation](https://strandsagents.com/)
- [LiteLLM docs](https://docs.litellm.ai/)

## Navigation

| Previous | Next |
|----------|------|
| [Lesson 5: Human-in-the-Loop](../lesson5_human_in_the_loop/README.md) | Sub-lesson 6.1 (Supervisor & workers) |
