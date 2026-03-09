"""
Run the MCP-backed agent: one-shot (with a question) or interactive.

  python run_example.py                    # interactive, AWS docs
  python run_example.py "What is AWS Lambda?"
  python run_example.py --multi            # interactive, real-time web search
  python run_example.py --multi "What's the fastest way to Barcelona from London?"

Requires GROQ_API_KEY in repo root .env; TAVILY_API_KEY for --multi. uv required for AWS docs server.
"""

import sys

from mcp_agent import create_mcp_agent, create_multi_mcp_agent

try:
    from strands.tools.mcp.mcp_client import MCPClientInitializationError
except ImportError:
    MCPClientInitializationError = None  # not exported from package __init__


def _parse_args(argv: list[str]) -> tuple[bool, str | None]:
    """Return (use_multi, question). --multi consumes one arg."""
    rest = list(argv)
    use_multi = rest and rest[0] == "--multi"
    if use_multi:
        rest = rest[1:]
    return use_multi, rest[0] if rest else None


def _connection_error_message(use_multi: bool) -> str:
    """User-facing message when agent creation fails due to connection."""
    if use_multi:
        return (
            "Connection error: could not connect to Tavily MCP (real-time web search). "
            "Check TAVILY_API_KEY in the repo root .env and network access."
        )
    return (
        "Could not connect to the MCP server. Is uv installed (https://docs.astral.sh/uv/)? "
        "On Windows, uvx may need different arguments for the AWS docs server."
    )


def _run_one_shot(agent, question: str) -> None:
    """Run agent on a single question and print response; exit 0 on success, 1 on error."""
    print(f"Question: {question}\n")
    try:
        print(f"Assistant: {agent(question)}")
    except Exception as e:
        if MCPClientInitializationError and isinstance(e, MCPClientInitializationError):
            print("Could not connect to the MCP server. Ensure uv is installed and the server can run via uvx.")
        else:
            print("Tool or connection error:", e)
        print(f"Details: {e}")
        sys.exit(1)
    sys.exit(0)  # MCP client background thread would otherwise keep process alive


def _run_interactive(agent, use_multi: bool) -> None:
    """Run interactive chat loop until quit/exit."""
    if use_multi:
        print(
            "Travel & accommodation assistant ready (real-time web search via Tavily).\n"
            "Try: \"What's the fastest way to Barcelona from London?\" or\n"
            "     \"What accommodation is available in Cape Town for 2 people for 3 nights?\"\n"
            "Type 'quit' or 'exit' to stop.\n"
        )
    else:
        print(
            "AWS docs assistant ready (MCP). Ask about AWS (e.g. 'What is Amazon S3?').\n"
            "Type 'quit' or 'exit' to stop.\n"
        )

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            break
        try:
            print(f"\nAssistant: {agent(user_input)}\n")
        except Exception as e:
            msg = "MCP connection error" if (MCPClientInitializationError and isinstance(e, MCPClientInitializationError)) else "Tool or connection error"
            print(f"\n{msg}: {e}\n")


def main() -> None:
    """Parse args, create agent, run one-shot or interactive with error handling."""
    use_multi, question = _parse_args(sys.argv[1:])

    try:
        agent = create_multi_mcp_agent() if use_multi else create_mcp_agent()
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        print(_connection_error_message(use_multi))
        print(f"Details: {e}")
        sys.exit(1)

    if question:
        _run_one_shot(agent, question)
    _run_interactive(agent, use_multi)


if __name__ == "__main__":
    main()
