"""
Shared config for Lesson 6: model and env. API key is read from environment only.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from strands.models.litellm import LiteLLMModel

REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")

MODEL_ID = "groq/llama-3.3-70b-versatile"
MODEL_PARAMS = {"max_tokens": 1024, "temperature": 0.3}


def get_model() -> LiteLLMModel:
    api_key = (os.environ.get("GROQ_API_KEY") or "").strip()
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not set. Copy repo root .env.example to .env and set your key."
        )
    return LiteLLMModel(
        client_args={"api_key": api_key},
        model_id=MODEL_ID,
        params=MODEL_PARAMS,
    )
