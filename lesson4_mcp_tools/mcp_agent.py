"""
Lesson 4: Extending Agents with External Tools (MCP)

Connect a Strands agent to external MCP servers so it discovers and uses tools
at runtime without code changes.

- create_mcp_agent() — single server: AWS Documentation (via uvx).
- create_multi_mcp_agent() — real-time web search via Tavily MCP.

API keys: GROQ_API_KEY (required); TAVILY_API_KEY (required for --multi). Use repo root .env.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from mcp import StdioServerParameters, stdio_client
from mcp.client.streamable_http import streamablehttp_client

from strands import Agent
from strands.models.litellm import LiteLLMModel
from strands.tools.mcp import MCPClient

_REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_REPO_ROOT / ".env")

# Shared model config (Groq Llama 3.3 70B via LiteLLM)
_MODEL_ID = "groq/llama-3.3-70b-versatile"
_MODEL_PARAMS = {"max_tokens": 1024, "temperature": 0.3}

# --- System prompts --------------------------------------------------------

MCP_SYSTEM_PROMPT = """You are a helpful assistant with access to AWS documentation via tools.

Your capabilities:
- Search and read AWS documentation using the tools provided by the MCP server.
- Use these tools when the user asks about AWS services, APIs, or concepts (e.g. Lambda, S3, IAM).

When the user asks about AWS:
1. Use the appropriate documentation tool to find current, accurate information.
2. Summarize clearly and concisely. Cite the documentation when helpful.
3. If the question is not about AWS, politely say you are focused on AWS documentation and offer to help with an AWS-related question."""

MULTI_MCP_SYSTEM_PROMPT = """You are a helpful travel and accommodation assistant with access to real-time web search.

Your capabilities:
- Use the web search tools to find current information from the live web: travel options, routes, accommodation, prices, and news.

When the user asks about travel (e.g. "fastest way from London to Barcelona"):
1. Use web search for current transport options, routes, and tips.
2. Summarize clearly with real, up-to-date information.

When the user asks about accommodation (e.g. "listings in Cape Town for 2 people for 3 nights"):
1. Use web search for real accommodation options, booking sites, or recent results for that city and criteria.
2. Present the findings in a friendly, readable way; cite sources when helpful.

Answer using real-world search results only. If the question is outside travel or accommodation, say you are focused on travel and accommodation and offer to help with that."""


def _get_env(key: str) -> str | None:
    """Read an environment variable; return stripped value or None."""
    value = os.environ.get(key)
    return value.strip() if value else None


def _aws_docs_server_params() -> StdioServerParameters:
    """Build stdio parameters for the AWS Documentation MCP server. Windows uses different args."""
    if sys.platform == "win32":
        return StdioServerParameters(
            command="uvx",
            args=[
                "--from",
                "awslabs.aws-documentation-mcp-server@latest",
                "awslabs.aws-documentation-mcp-server.exe",
            ],
        )
    return StdioServerParameters(
        command="uvx",
        args=["awslabs.aws-documentation-mcp-server@latest"],
    )


def _create_model(api_key: str) -> LiteLLMModel:
    """Build the shared LiteLLM model (Groq)."""
    return LiteLLMModel(
        client_args={"api_key": api_key},
        model_id=_MODEL_ID,
        params=_MODEL_PARAMS,
    )


def create_mcp_agent() -> Agent:
    """Create an agent with the AWS Documentation MCP server as its tool provider."""
    api_key = _get_env("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "Groq API key not set. Add GROQ_API_KEY=... to the repo root .env file. "
            "Free key at https://console.groq.com"
        )

    aws_docs_client = MCPClient(lambda: stdio_client(_aws_docs_server_params()))
    model = _create_model(api_key)

    return Agent(
        model=model,
        system_prompt=MCP_SYSTEM_PROMPT,
        tools=[aws_docs_client],
    )


def create_multi_mcp_agent() -> Agent:
    """Create an agent with real-time web search via Tavily MCP.

    Uses Tavily for live web search (travel, accommodation, current information).
    Requires TAVILY_API_KEY in the repo root .env.
    """
    api_key = _get_env("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "Groq API key not set. Add GROQ_API_KEY=... to the repo root .env file. "
            "Free key at https://console.groq.com"
        )
    tavily_key = _get_env("TAVILY_API_KEY")
    if not tavily_key:
        raise ValueError(
            "Tavily API key not set. Add TAVILY_API_KEY=... to the repo root .env for web search. "
            "Get a key at https://tavily.com"
        )

    tavily_url = f"https://mcp.tavily.com/mcp/?tavilyApiKey={tavily_key}"
    web_client = MCPClient(
        lambda: streamablehttp_client(tavily_url),
        prefix="web",
    )
    model = _create_model(api_key)

    return Agent(
        model=model,
        system_prompt=MULTI_MCP_SYSTEM_PROMPT,
        tools=[web_client],
    )


def main() -> None:
    """Run interactive loop with the AWS docs agent."""
    agent = create_mcp_agent()
    print("AWS docs assistant ready (MCP). Ask about AWS (e.g. 'What is AWS Lambda?').")
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
        print(f"\nAssistant: {agent(user_input)}\n")


if __name__ == "__main__":
    main()
