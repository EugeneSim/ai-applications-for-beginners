"""
Lesson 6.3: Graph-Based Workflows.

Structured DAG: nodes are agents, edges are dependencies. Run in topological order;
each node receives the combined output of its predecessor nodes.
"""

from __future__ import annotations

from collections import deque
from typing import Any

from strands import Agent

from _shared import get_model

# ---------------------------------------------------------------------------
# Example agents for the graph (research -> analysis, fact_check -> report)
# ---------------------------------------------------------------------------

RESEARCHER_PROMPT = """You are a research specialist. Gather concise, factual information on the given topic. Output a short research note (key facts, sources or claims). No opinions."""

ANALYST_PROMPT = """You are a data analysis specialist. You receive research notes. Process and interpret the data; identify 3–5 key insights. Output a short analysis."""

FACT_CHECKER_PROMPT = """You are a fact-checking specialist. You receive research notes. Validate accuracy; note any unsupported claims. Output a short validation note."""

REPORT_WRITER_PROMPT = """You are a report writer. You receive both an analysis and a fact-check note. Produce a short, structured report (intro, key points, caveats). Keep it under 300 words."""


def _agent(system_prompt: str) -> Agent:
    return Agent(system_prompt=system_prompt, model=get_model(), tools=[])


def create_graph_agents() -> dict[str, Agent]:
    return {
        "research": _agent(RESEARCHER_PROMPT),
        "analysis": _agent(ANALYST_PROMPT),
        "fact_check": _agent(FACT_CHECKER_PROMPT),
        "report": _agent(REPORT_WRITER_PROMPT),
    }


# ---------------------------------------------------------------------------
# DAG builder and runner
# ---------------------------------------------------------------------------

class GraphWorkflow:
    """
    DAG of agents: add_node(agent, id), add_edge(from_id, to_id), set_entry_point(id).
    run(task) executes in topological order; each node gets predecessors' outputs as input.
    """

    def __init__(self) -> None:
        self._nodes: dict[str, Agent] = {}
        self._edges: list[tuple[str, str]] = []  # (from, to)
        self._entry_point: str | None = None

    def add_node(self, agent: Agent, node_id: str) -> None:
        self._nodes[node_id] = agent

    def add_edge(self, from_id: str, to_id: str) -> None:
        self._edges.append((from_id, to_id))

    def set_entry_point(self, node_id: str) -> None:
        self._entry_point = node_id

    def _topological_order(self) -> list[str]:
        """Return node ids in topological order (entry first when possible)."""
        in_degree = {n: 0 for n in self._nodes}
        for from_id, to_id in self._edges:
            in_degree[to_id] = in_degree.get(to_id, 0) + 1
        queue = deque([self._entry_point] if self._entry_point else [n for n, d in in_degree.items() if d == 0])
        if self._entry_point and in_degree.get(self._entry_point, 0) != 0:
            queue = deque([n for n, d in in_degree.items() if d == 0])
        order: list[str] = []
        while queue:
            n = queue.popleft()
            if n in order:
                continue
            order.append(n)
            for from_id, to_id in self._edges:
                if from_id == n:
                    in_degree[to_id] -= 1
                    if in_degree[to_id] == 0:
                        queue.append(to_id)
        return order

    def run(self, task: str) -> dict[str, Any]:
        """
        Execute the graph. Returns dict with node_id -> output text, and "report" or final node output.
        """
        order = self._topological_order()
        outputs: dict[str, str] = {}

        for node_id in order:
            agent = self._nodes[node_id]
            # Input = task for entry; else concatenation of all predecessors' outputs
            pred_outputs = [outputs[f] for f, t in self._edges if t == node_id]
            if not pred_outputs:
                input_text = task
            else:
                input_text = "\n\n".join(f"--- {f} ---\n{outputs[f]}" for f, t in self._edges if t == node_id)

            print(f"  [{node_id}] running...")
            result = agent(input_text)
            outputs[node_id] = str(result).strip()

        return {
            "outputs": outputs,
            "order": order,
            "final": outputs.get(order[-1], "") if order else "",
        }


def build_example_graph() -> GraphWorkflow:
    """Build the reference example: research -> analysis, fact_check -> report."""
    agents = create_graph_agents()
    g = GraphWorkflow()
    for nid, ag in agents.items():
        g.add_node(ag, nid)
    g.add_edge("research", "analysis")
    g.add_edge("research", "fact_check")
    g.add_edge("analysis", "report")
    g.add_edge("fact_check", "report")
    g.set_entry_point("research")
    return g
