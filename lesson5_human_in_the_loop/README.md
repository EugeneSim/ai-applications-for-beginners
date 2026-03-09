# Lesson 5: Human-in-the-Loop Agent

**Lesson 5** of [AI Applications for Beginners](../). You'll implement **human-in-the-loop (HITL)** patterns so your agent can pause execution and request human input when needed. This builds safer, more interactive AI systems that work alongside humans instead of running fully autonomously.

## What You'll Learn

- How to implement human-in-the-loop patterns in AI agents using the **Strands interrupt system**
- Using **hooks** (`BeforeToolCallEvent`) and **`event.interrupt()`** for approval requests and handoffs
- Two main use cases: **approval requests** (e.g. before delete) and **task completion handoffs** (e.g. submit for review)
- Best practices for building collaborative AI systems

## Prerequisites

- Basic understanding of the AWS Strands framework (Lessons 1–4)
- Python environment with the lesson dependencies
- `GROQ_API_KEY` in the repo root `.env` (same as other lessons)

## Use Cases Covered

| Category | Example in this lesson |
|----------|------------------------|
| **Security-critical operations** | Delete files only after human approval |
| **Collaborative decision making** | Submit content for review before “completing” |
| **Task completion handoffs** | Pause and hand control to the user with next steps |

Human-in-the-loop is also useful for:

- **Clarification**: When the user’s intent is unclear, the agent can interrupt to ask for details.
- **Quality control**: A human can verify or correct the agent’s output before it’s used downstream.

## Concepts

| Concept | What it is |
|--------|-------------|
| **Interrupt** | A pause in the agent loop; control returns to the user until they respond. |
| **`BeforeToolCallEvent`** | Hook event fired before a tool runs; you can interrupt here to ask for approval. |
| **`event.interrupt(name, reason)`** | Raises an interrupt with a unique name and optional context (e.g. paths to delete). |
| **`event.cancel_tool`** | Set to a message (or `True`) to cancel the tool when the user denies. |
| **Interrupt response** | User sends back `interruptResponse` blocks (`interruptId` + `response`) and calls the agent again to resume. |
| **Handoff** | Interrupt that passes context and “next steps” to the user (task completion handoff). |

## Demo

1. **Interactive HITL loop** (approval + handoff):

   ```bash
   cd lesson5_human_in_the_loop
   pip install -r requirements.txt
   python run_example.py
   ```

2. **Try approval**: Ask the agent to create some files, then to delete them. It will pause and ask **Approve delete of [...]? (y/N):** — reply `y` to allow or anything else to deny.

3. **Try handoff**: Say something like “Draft a short summary and submit it for review.” The agent will use `submit_for_review`; the app will pause, show next steps, and ask for your reply before completing.

You can also run the agent module directly:

```bash
python hitl_agent.py
```

## Testing (walkthrough)

Follow these steps to verify both HITL flows: **approval** (pause before delete) and **handoff** (submit for review).

### 1. Start the app

From the repo root or this folder:

```bash
cd lesson5_human_in_the_loop
pip install -r requirements.txt
python run_example.py
```

You should see:

```
HITL file assistant ready. Create/list/delete files; delete requires approval.

Say 'submit for review' to trigger a handoff. Type 'quit' or 'exit' to stop.

You:
```

### 2. Test approval flow (delete with human approval)

**2a. Create files** (no interrupt)

| You type | What happens |
|----------|----------------|
| `Create a file called notes.txt with content Hello` | Agent calls `create_file`; no interrupt. You get a short confirmation. |
| `Also create draft.md and temp.log` | Agent creates both. |

**2b. List files** (optional)

| You type | What happens |
|----------|----------------|
| `List all files` | Agent calls `list_files`; you see e.g. `notes.txt`, `draft.md`, `temp.log`. |

**2c. Delete with approval — approve**

| You type | What happens |
|----------|----------------|
| `Delete notes.txt` | Agent decides to call `delete_files(["notes.txt"])`. **Before** the tool runs, the app pauses and prints: `Approve delete of ['notes.txt']? (y/N):` |
| `y` | Your response is sent as an interrupt response; the tool runs; the agent confirms the file was deleted. |

**2d. Delete with approval — deny**

| You type | What happens |
|----------|----------------|
| `Delete draft.md and temp.log` | Again you see: `Approve delete of ['draft.md', 'temp.log']? (y/N):` |
| `n` or `No` or just Enter | The tool is **cancelled** (`event.cancel_tool`). The agent reports that permission was denied; the files are not deleted. |

This confirms the **approval** use case: dangerous operations don’t run until the user approves.

### 3. Test handoff flow (submit for review)

| You type | What happens |
|----------|----------------|
| `Draft a one-sentence summary of Lesson 5 and submit it for review` | Agent drafts text, then calls `submit_for_review(title=..., summary=...)`. **Before** the tool runs, the handoff hook interrupts. |
| *(You see)* | `[Handoff] Review the content above. Reply with 'ok' to confirm handoff, or add notes for the agent.` and `Reply (e.g. 'ok' or your notes):` |
| `ok` or any reply | Your response is sent; the tool runs; the agent completes the handoff. |

This confirms the **task completion handoff** use case: the agent pauses, shows context and next steps, and only continues after you respond.

### 4. Exit

| You type | What happens |
|----------|----------------|
| `quit` or `exit` or `q` | Loop ends; process exits. |

### Quick checklist

- [ ] App starts and shows the “HITL file assistant ready” message.
- [ ] Create/list work without any approval prompt.
- [ ] Delete triggers “Approve delete of [...]? (y/N):”; answering `y` deletes; answering `n` (or other) cancels and leaves files intact.
- [ ] “Submit for review” triggers the handoff message and “Reply (e.g. 'ok' or your notes):”; after you reply, the agent completes.
- [ ] `quit` / `exit` exits cleanly.

If any step behaves differently (e.g. no interrupt on delete, or no handoff message), check that you’re running `run_example.py` and that `GROQ_API_KEY` is set in the repo root `.env`.

## How It Works

1. **Approval (delete_files)**  
   - Agent decides to call `delete_files(paths)`.  
   - `ApprovalHook` runs on `BeforeToolCallEvent`, sees `delete_files`, and calls `event.interrupt(...)` with the paths in `reason`.  
   - The agent loop stops and returns `result.stop_reason == "interrupt"` and `result.interrupts`.  
   - `run_interactive()` in `hitl_agent.py` prompts the user, builds `interruptResponse` blocks, and calls `agent(responses)` to resume.  
   - On resume, `event.interrupt()` returns the user’s response; if it’s not approval, we set `event.cancel_tool` so the tool is not executed.

2. **Handoff (submit_for_review)**  
   - Agent calls `submit_for_review(title, summary)`.  
   - `HandoffHook` interrupts with `reason` containing title, summary, and next steps.  
   - User sees the context and replies; after resume, the tool runs and the handoff is complete.

## Files

| File | Description |
|------|-------------|
| `hitl_agent.py` | Agent with `list_files`, `create_file`, `delete_files`, `submit_for_review`; `ApprovalHook` and `HandoffHook`; `create_hitl_agent()` and `run_interactive()`. |
| `run_example.py` | Creates the agent and runs the interactive HITL loop. |
| `requirements.txt` | Dependencies (Strands + LiteLLM, python-dotenv). |

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
   Put `GROQ_API_KEY=...` in the **repo root** `.env` file (same as other lessons). Never commit `.env`.

## Best Practices

- **Namespace interrupt names** (e.g. `lesson5-hitl-approval`) so you can tell them apart when building responses.
- **Put context in `reason`** (e.g. paths, summary) so the user knows what they’re approving or reviewing.
- **Use `cancel_tool`** when the user denies an action so the agent doesn’t run the dangerous operation.
- **Keep `reason` JSON-serializable** for session persistence if you add session management later.
- For **task handoffs**, include clear “next steps” in the interrupt reason so the user knows what to do.

## Further Learning

- [Strands: Interrupts (Human-in-the-Loop)](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/interrupts/)
- [Strands: Hooks](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/agents/hooks/)
- [Strands: API Reference – Interrupt](https://strandsagents.com/latest/documentation/docs/api-reference/python/types/interrupt/)
