# Lesson 2: Session state and agent memory

**Lesson 2** of [AI Applications for Beginners](../). Traditionally agents are **stateless**: each request has no memory of past turns. This lesson gives the agent **memory** by persisting conversation history per **session** (JSON on disk).

## Concepts

| Concept | What it is |
|--------|------------|
| **Stateless** | Default agent behavior: no memory between invocations. |
| **Session** | A unique `session_id` (e.g. user or chat id) that groups one conversation. |
| **FileSessionManager** | Creates a **folder per `session_id`**. Inside it, each message is saved as a **separate JSON file**. |
| **Restore** | With an existing `session_id`, the manager **loads** those JSON files to **reconstruct** the conversation before processing the new query. |

## Storage layout

With `FileSessionManager(session_id="eugene-demo", storage_dir="./sessions")`:

```
sessions/
└── session_eugene-demo/
    ├── session.json
    └── agents/
        └── agent_<agent_id>/
            ├── agent.json
            └── messages/
                ├── message_<id>.json
                ├── message_<id>.json
                └── ...
```

Each message is one JSON file; loading a session reads these files to restore history.

## Demo: “Do you know who I am? I am Eugene Sim”

1. **First run** — tell the agent your name:
   ```bash
   cd lesson2_sessions_state
   pip install -r requirements.txt
   python run_example.py "I am Eugene Sim"
   ```

2. **Second run** — same session, ask for memory:
   ```bash
   python run_example.py "Do you know who I am?"
   ```
   The agent loads the stored conversation and should answer with your name (e.g. Eugene Sim).

**Custom session ID:**
```bash
python run_example.py --session my-user-123 "I am Eugene Sim"
python run_example.py --session my-user-123 "Do you know who I am?"
```

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

3. **API key:** Put `GROQ_API_KEY=your-key` in the **repo root** `.env` (same as Lesson 1). Free key at [console.groq.com](https://console.groq.com). Never commit `.env`.

## Run

**Single message (demo):**
```bash
python run_example.py "I am Eugene Sim"
python run_example.py "Do you know who I am?"
```

**Interactive chat (same session = same memory):**
```bash
python session_agent.py
python session_agent.py my-session-id
```

## Files

| File | Description |
|------|-------------|
| `session_agent.py` | System prompt, `FileSessionManager`, and `create_session_agent(session_id, storage_dir)`. |
| `run_example.py` | One-shot or interactive demo; default session `eugene-demo`. |
| `requirements.txt` | Dependencies (Strands + LiteLLM, python-dotenv). |
| `sessions/` | Created at runtime; session folders and message JSON (gitignored). |

## Further learning

- [Strands Session Management](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/agents/session-management/)
- [Strands documentation](https://strandsagents.com/)
