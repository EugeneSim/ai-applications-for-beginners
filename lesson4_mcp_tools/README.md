# Lesson 4: Extending Agents with External Tools (MCP)

**Lesson 4** of [AI Applications for Beginners](../). You'll make your agent more powerful by connecting it to **external tool servers** using the **Model Context Protocol (MCP)**. The agent **discovers and uses tools at runtime** without any changes to its own code.

We connect to the **AWS Documentation MCP server** so the agent can search and read current AWS docs, turning a general-purpose agent into an AWS documentation expert.

## Concepts

| Concept | What it is |
|--------|------------|
| **MCP** | Open protocol for connecting agents to external tool servers; tools are discovered at runtime. |
| **Dynamic tool discovery** | The agent receives tools from the server (e.g. `list_tools`) without changing agent code. |
| **MCPClient** | Strands client that connects to an MCP server and exposes its tools as a ToolProvider. |
| **Multi-server integration** | You can pass multiple MCP clients: `Agent(tools=[client1, client2])`; optional prefix/filtering to avoid name clashes. |
| **Real-time data** | External servers (e.g. AWS docs) provide current information the agent can use in its answers. |
| **Error handling** | Catching MCP initialization and connection/tool errors and returning clear messages to the user. |

## Why it matters

- **No code change to add tools** — plug in a new MCP server and the agent gains new capabilities.
- **Real-time information** — the AWS docs server gives access to up-to-date documentation.
- **Robust connections** — handle connection failures and tool errors so the app stays user-friendly.

## Benefits of MCP

- **Extensibility**: Add new capabilities without code changes — connect another MCP server and the agent gets new tools.
- **Maintainability**: Update tools on servers; agents gain new abilities instantly without redeploying the agent.
- **Modularity**: Mix and match tools from different servers (e.g. AWS docs + web search).
- **Real-time data**: Access current information from external sources (AWS docs, web search).
- **Specialization**: Transform general agents into domain experts (AWS docs, travel, etc.).

## Demo

1. **One-shot question** (requires [uv](https://docs.astral.sh/uv/) for `uvx` and the AWS docs server):
   ```bash
   cd lesson4_mcp_tools
   pip install -r requirements.txt
   python run_example.py "What is AWS Lambda?"
   ```

2. **Interactive chat**:
   ```bash
   python run_example.py
   ```
   Or run the agent module directly:
   ```bash
   python mcp_agent.py
   ```

3. **More examples** (single-server, AWS docs):
   ```bash
   python run_example.py "How do I create an S3 bucket?"
   python run_example.py "What is Amazon IAM?"
   ```

4. **Real-time web search (Tavily MCP)** — requires `TAVILY_API_KEY` in repo root `.env`:
   ```bash
   python run_example.py --multi "What's the fastest way to get to London from Singapore?"
   python run_example.py --multi "What accommodation is available in Maldives for 4 people for 5 nights?"
   python run_example.py --multi
   ```
   The `--multi` agent uses **Tavily** for real-time web search: travel, accommodation, and current information from the live web (no mock data).

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

3. **uv (for uvx)**  
   The AWS Documentation MCP server is run via `uvx`. Install [uv](https://docs.astral.sh/uv/) (e.g. `pip install uv` or the official installer).

4. **API keys** (in **repo root** `.env`):
   - `GROQ_API_KEY` — required for all lessons. Free key at [console.groq.com](https://console.groq.com).
   - `TAVILY_API_KEY` — required only for multi-server (`--multi`). Get one at [tavily.com](https://tavily.com). Never commit `.env`.

## Files

| File | Description |
|------|-------------|
| `mcp_agent.py` | `create_mcp_agent()` (AWS docs), `create_multi_mcp_agent()` (Tavily real-time web search); system prompts; interactive loop when run directly. |
| `run_example.py` | One-shot or interactive; use `--multi` for real-time web search (travel, accommodation); handles configuration, connection, and runtime errors. |
| `requirements.txt` | Dependencies (Strands + LiteLLM, mcp, python-dotenv). |
| `.env.example` | Documents `GROQ_API_KEY` and `TAVILY_API_KEY` (repo root `.env`). |

## Error handling

- **Configuration errors**: Missing API keys raise `ValueError` with a clear message (exit code 1).
- **Connection errors**: MCP server or network failures are caught and reported with a user-friendly message (exit code 1).
- **Runtime errors**: Failures during `agent(...)` (tool execution, timeouts) are caught and printed; one-shot mode exits with code 1.

Example pattern (as in `run_example.py`); the SDK may expose `MCPClientInitializationError` from `strands.tools.mcp.mcp_client` for connection failures:

```python
try:
    agent = create_mcp_agent()
    response = agent(question)
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print("Connection or tool error:", e)
```

## Troubleshooting

| Issue | What to do |
|-------|------------|
| **uvx not found** | Install [uv](https://docs.astral.sh/uv/). The AWS docs server is run via `uvx awslabs.aws-documentation-mcp-server@latest`. |
| **Windows vs Linux/Mac** | On Windows, the lesson uses different `uvx` args: `--from awslabs.aws-documentation-mcp-server@latest awslabs.aws-documentation-mcp-server.exe`. This is handled in `mcp_agent.py`. |
| **Connection or timeout** | Ensure no firewall blocks the MCP server process. First run may be slow while the server starts. |
| **Groq key** | Same as other lessons: `GROQ_API_KEY` in repo root `.env`. |
| **Multi-server: Tavily** | For `--multi`, set `TAVILY_API_KEY` in repo root `.env`. Get a key at [tavily.com](https://tavily.com). |

## Further learning

- [Strands: MCP Tools](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/mcp-tools/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
