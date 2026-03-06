# Lesson 3: Getting Structured Output

**Lesson 3** of [AI Applications for Beginners](../). You'll learn one of the most powerful features of the Strands SDK: **extracting structured data** (like JSON) from **unstructured text**. This is essential for any application that needs to reliably get specific pieces of information from an LLM.

We use a **Pydantic model** to define the exact data schema we want, and the agent's **`structured_output_model`** parameter does the heavy lifting of guiding the LLM's output into that schema. You get a validated Python object instead of raw text to parse.

## Concepts

| Concept | What it is |
|--------|------------|
| **Structured output** | LLM response forced into a fixed schema (e.g. a Pydantic model) so you get typed, validated data. |
| **Pydantic model** | A class defining fields and types (e.g. `name: str`, `age: int`). Use `Field(description=...)` to help the LLM fill each field correctly. |
| **`structured_output_model`** | Parameter passed when calling the agent: `agent(prompt, structured_output_model=PersonInfo)`. |
| **`result.structured_output`** | The validated Pydantic instance returned by the agent (e.g. `PersonInfo`). |

## Why it matters

- **Type safety**: You get a Python object with known fields and types, not a string to parse.
- **Validation**: Pydantic validates the LLM output; invalid or missing fields can be caught early.
- **IDE support**: Autocomplete and type hints work on `result.structured_output`.
- **Reliability**: Your app can depend on a consistent shape (e.g. for APIs or databases).

## Example: PersonInfo

Define a Pydantic model (optional fields use `None` when the text doesn’t mention them):

```python
from pydantic import BaseModel, Field

class PersonInfo(BaseModel):
    name: str = Field(description="Full name of the person")
    age: int | None = Field(default=None, description="Age in years when mentioned (0-150)")
    occupation: str | None = Field(default=None, description="Job or occupation when mentioned")
    location: str | None = Field(default=None, description="City or place if mentioned")
```

Call the agent with your text and the model:

```python
agent = create_agent()  # Strands agent (model, system prompt, etc.)
result = agent(
    "Eugene Sim, 28, is an aspiring data engineer based in Singapore.",
    structured_output_model=PersonInfo,
)
person = result.structured_output  # PersonInfo instance
print(person.name)       # "Eugene Sim"
print(person.occupation) # "data engineer"
```

The LLM is guided to produce output that fits `PersonInfo`; Strands validates it and returns it as `result.structured_output`.

## Demo

1. **Run with built-in samples** (PersonInfo + MeetingSummary):
   ```bash
   cd lesson3_structured_output
   pip install -r requirements.txt
   python run_example.py
   ```

2. **Extract from your own text** (PersonInfo by default):
   ```bash
   python run_example.py "Eugene Sim is an aspiring data engineer based in Singapore."
   ```

3. **Extract a meeting summary** instead:
   ```bash
   python run_example.py --meeting "Daily standup, March 6, 2025. Attendees: Eugene, Priya. Actions: send report."
   ```

4. **Quick test from the agent module**:
   ```bash
   python structured_agent.py
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

3. **API key:** Put `GROQ_API_KEY=your-key` in the **repo root** `.env` (same as Lessons 1–2). Free key at [console.groq.com](https://console.groq.com). Never commit `.env`.

## Files

| File | Description |
|------|-------------|
| `structured_agent.py` | Pydantic models (`PersonInfo`, `MeetingSummary`), `create_agent()`, `extract_person()`, `extract_meeting()`. |
| `run_example.py` | Demo: run samples or pass your own text; optional `--meeting` for `MeetingSummary`. |
| `requirements.txt` | Dependencies (Strands + LiteLLM, python-dotenv, pydantic). |

## Error handling

If the LLM output cannot be validated against your schema, Strands can raise a `StructuredOutputException`. In production you may want to catch it and retry or fall back:

```python
from strands.types.exceptions import StructuredOutputException

try:
    result = agent(prompt, structured_output_model=PersonInfo)
    person = result.structured_output
except StructuredOutputException as e:
    print(f"Structured output failed: {e}")
```

## Further learning

- [Strands: Structured Output](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/agents/structured-output/)
- [Pydantic models and fields](https://docs.pydantic.dev/latest/concepts/models/)
