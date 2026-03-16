# Lesson 6: Advanced Multi-Agent Patterns

**Lesson 6** of [AI Applications for Beginners](../). You'll move beyond a single agent and use four patterns for multi-agent systems: **Agent as Tools**, **Swarm Intelligence**, **Graph-Based Workflows**, and **Workflow Agent**.

## What You'll Learn

- **6.1 Agent as Tools**: An orchestrator agent that delegates to specialist workers exposed as `@tool`
- **6.2 Swarm Intelligence**: Decentralized agents that hand off to each other with no central controller
- **6.3 Graph-Based Workflows**: A DAG of agents with explicit dependencies and execution order
- **6.4 Workflow Agent**: Stateful sequential workflows (research pipeline and fact-check) with conditional routing

## Prerequisites

- Lessons 1–5 (agents, tools, sessions, human-in-the-loop)
- Python 3.x
- **API key:** Copy the repo root `.env.example` to `.env` and set `GROQ_API_KEY`. Never commit `.env`.

## Sub-Lessons Overview

| Part | Topic | Run script | Description |
|------|--------|------------|-------------|
| **6.1** | Agent as Tools | `run_6_1.py` | Orchestrator with research, product, and travel assistants as tools |
| **6.2** | Swarm Intelligence | `run_6_2.py` | Researcher, architect, coder, reviewer hand off via `HANDOFF:id:msg` |
| **6.3** | Graph-Based Workflows | `run_6_3.py` | DAG: research → analysis & fact_check → report |
| **6.4** | Workflow Agent | `run_6_4.py` | Researcher → Analyst → Writer; research vs fact-check routing |

---

## 6.1 Agent as Tools

**Architecture:** User query → **Orchestrator** → (Research Agent | Product Agent | Travel Agent) → combined response.

**Key ideas:**

- Worker agents are experts in one domain (research, product recommendations, travel).
- Each worker is wrapped in a `@tool` so the orchestrator can call it by name.
- The orchestrator’s system prompt describes when to use each tool and can chain multiple tools.

**Run** (from `lesson6_multi_agent_patterns` after `pip install -r requirements.txt`):

```bash
python run_6_1.py "I need hiking boots for a mountain trip"
python run_6_1.py   # interactive
```

**Example use cases:** Simple question (orchestrator answers directly); single delegation (e.g. product or travel); multi-step (e.g. “Plan a hiking trip to Patagonia and recommend waterproof boots” → trip_planning_assistant then product_recommendation_assistant).

**Files:** `agent_as_tools.py` (workers + orchestrator), `run_6_1.py`.

---

## 6.2 Swarm Intelligence

**Architecture:** User task → **Entry-point agent** (e.g. researcher) → dynamic **handoffs** between researcher, architect, coder, reviewer → final solution.

**Key ideas:**

- No central orchestrator; any agent can hand off to another.
- Handoff protocol: an agent ends its reply with `HANDOFF:agent_id:message` to pass control.
- `max_handoffs` limits the chain to avoid runaway loops.

**Run:**

```bash
python run_6_2.py "Outline a simple web API for customer orders"
python run_6_2.py   # interactive
```

**Example use cases:** Software design (researcher → architect → coder → reviewer); research and report (researcher → analyst → writer → reviewer).

**Files:** `swarm_agents.py` (agents + `run_swarm()`), `run_6_2.py`.

---

## 6.3 Graph-Based Workflows

**Architecture:** User task → **DAG entry** (research) → **analysis** and **fact_check** in parallel (both depend on research) → **report** (depends on both) → final result.

**Key ideas:**

- Nodes are agents; edges are dependencies. Execution follows a topological order.
- Parallelism: analysis and fact_check both run after research; report runs after both.
- Good for repeatable, auditable pipelines.

**Run:**

```bash
python run_6_3.py "Impact of AI on healthcare"
python run_6_3.py   # interactive
```

**Example use cases:** Research + report; content pipeline (research → writer & fact_check → editor); QA pipeline (requirements → architect & tester → developer → QA).

**Files:** `graph_workflow.py` (`GraphWorkflow`, `build_example_graph()`), `run_6_3.py`.

---

## 6.4 Workflow Agent

**Architecture:** User input → **conditional routing** → either **research workflow** (topic → Researcher → Analyst → Writer) or **fact-check workflow** (claim → Researcher → Analyst → Writer with verdict).

**Key ideas:**

- Same three agents (Researcher, Analyst, Writer); different prompts and flow for “research a topic” vs “fact-check a claim”.
- Context is passed step by step; full workflow is stateful.
- Conditional routing: e.g. “fact-check” in input or “Claim:” prefix triggers fact-check.

**Run:**

```bash
python run_6_4.py "Latest developments in AI safety"
python run_6_4.py "Claim: OpenAI's GPT-4 was released in March 2023"
python run_6_4.py   # interactive
```

**Example use cases:** Research automation; fact-checking claims; structured reports with sources.

**Files:** `workflow_agent.py` (`run_research_workflow`, `run_fact_check_workflow`, `run_workflow`), `run_6_4.py`.

---

## End-to-end test

Run all four patterns with sample inputs (use `--quick` for shorter prompts and faster run):

```bash
python run_all_e2e.py
python run_all_e2e.py --quick
```

## Files

| File | Description |
|------|-------------|
| `_shared.py` | Shared model config; reads `GROQ_API_KEY` from env only |
| `requirements.txt` | Strands, LiteLLM, python-dotenv |
| `agent_as_tools.py` | 6.1: workers + orchestrator |
| `run_6_1.py` | Run 6.1 |
| `swarm_agents.py` | 6.2: swarm agents + handoff loop |
| `run_6_2.py` | Run 6.2 |
| `graph_workflow.py` | 6.3: DAG builder and example graph |
| `run_6_3.py` | Run 6.3 |
| `workflow_agent.py` | 6.4: research and fact-check workflows |
| `run_6_4.py` | Run 6.4 |
| `run_all_e2e.py` | E2E test: runs 6.1–6.4 with sample inputs |

## Setup

1. **API key (required):** From the repo root, copy `.env.example` to `.env` and set `GROQ_API_KEY`. Do not commit `.env`. See the root [README](../README.md) security section.

2. **Virtual environment** (recommended):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # source .venv/bin/activate   # macOS/Linux
   ```

3. **Dependencies** (from this folder):

   ```bash
   pip install -r requirements.txt
   ```

## Choosing a Pattern

- **Single domain, need routing** → 6.1 Agent as Tools (orchestrator picks specialist).
- **Open-ended, collaborative task** → 6.2 Swarm (agents hand off as needed).
- **Fixed, auditable pipeline** → 6.3 Graph-Based (explicit DAG).
- **Research or fact-check with fixed steps** → 6.4 Workflow Agent (sequential + conditional).

## Best Practices

- **Clear roles:** One main responsibility per agent; avoid overlap.
- **Tool docstrings (6.1):** Describe when the orchestrator should call each tool.
- **Handoff protocol (6.2):** Keep format simple and document it in agent prompts.
- **Graph design (6.3):** Prefer acyclic dependencies; add entry point and timeouts if you extend.
- **Context (6.4):** Pass full prior output into the next agent so the workflow stays coherent.

## Troubleshooting

- **Orchestrator not calling the right tool (6.1):** Tighten the orchestrator system prompt and tool docstrings.
- **Swarm loops or no handoff (6.2):** Check for `HANDOFF:agent_id:message` in prompts; reduce `max_handoffs` if it loops.
- **Graph order wrong (6.3):** Verify edges and entry point; ensure no cycles.
- **Wrong workflow branch (6.4):** Adjust the condition in `run_workflow()` (e.g. “fact-check”, “Claim:”) to match your use case.

## Further Learning

- [Strands documentation](https://strandsagents.com/)
- [LiteLLM docs](https://docs.litellm.ai/)

## Navigation

| Previous | Next |
|----------|------|
| [Lesson 5: Human-in-the-Loop](../lesson5_human_in_the_loop/README.md) | Sub-lesson 6.1 (Agent as Tools) |
