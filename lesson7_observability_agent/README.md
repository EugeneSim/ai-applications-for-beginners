# Lesson 7: Observability Agent

Observability for monitoring and debugging AI agents in production using **AWS Strands** with **OpenTelemetry** tracing and **Langfuse** integration.

## What You'll Learn

- Configure OpenTelemetry for AI agent observability
- Set up Langfuse for tracing and monitoring
- Monitor agent interactions and performance
- Best practices for AI application observability

## Prerequisites

- Basic understanding of AWS Strands framework
- Python environment with required dependencies
- API key for your chosen language model (Nebius, OpenAI, Groq, etc.)
- [Langfuse](https://cloud.langfuse.com) account for observability

## Quick Start

### 1. Setup Environment

```bash
# Install dependencies (from repo root or this folder)
uv sync
# or: pip install -r requirements.txt

# Set up environment variables in the repo root .env (never commit this file)
# Copy the repo root .env.example to .env and set your real keys there:
#   GROQ_API_KEY or NEBIUS_API_KEY
#   LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST (optional, default EU)
```

### 2. Run the Example

```bash
uv run main.py
# or: python main.py
```

### 3. Expected Output

```
🤖 Restaurant Helper Agent initialized with observability!
📊 All interactions will be traced and monitored in Langfuse.
------------------------------------------------------------
👤 User: Hi, where can I eat in San Francisco?
🤖 Restaurant Helper: [Agent response with tracing enabled]
------------------------------------------------------------
The interaction was captured in Langfuse for monitoring and analysis.
```

View traces in your [Langfuse dashboard](https://cloud.langfuse.com).

## Key Components

- **Environment validation**: Ensures all required variables are set
- **Langfuse integration**: OpenTelemetry OTLP exporter to Langfuse
- **Agent configuration**: `trace_attributes` for session.id, user.id, tags
- **Automatic tracing**: All agent interactions are traced

## Trace Attributes

| Attribute   | Description              | Example                    |
|------------|--------------------------|----------------------------|
| session.id | Unique session identifier| `"lesson7-demo-session"`   |
| user.id    | User identification      | `"user@example.com"`       |
| tags       | Categorization tags      | `["production", "restaurant-bot"]` |

## Use Cases

- **Performance monitoring**: Response time, token usage, error rates
- **Debugging**: Distributed tracing, error tracking, log correlation
- **Business intelligence**: Usage analytics, cost analysis, quality metrics
- **Security and compliance**: Audit trails, access control

## Security & cleanup (public repo / before you push)

- **Never commit secrets.** Store `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, and API keys only in the **repo root** `.env` file. That file is gitignored and must not be committed.
- **Use the template.** Copy the repo root [`.env.example`](../.env.example) to `.env` and set your real keys locally. Do not add real keys to `.env.example` or any tracked file.
- **No keys in code.** This lesson reads all credentials from the environment via `os.environ.get(...)`; there are no hardcoded API keys or secrets.
- **Before pushing:** Run `git status` and ensure `.env` is not staged. Run `git diff --cached` and confirm no real keys appear in staged files.
- **Cleanup:** If you ever pasted a real key into a terminal (e.g. `export LANGFUSE_SECRET_KEY=...`), clear your shell history for that session or remove that line from history; never commit shell logs that might contain secrets.
