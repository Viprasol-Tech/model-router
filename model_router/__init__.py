"""model-router: pick an LLM by task, budget, latency or context window."""

__version__ = "0.2.0"

from .core import ModelProfile, ModelRouter, compare, main, select_model

__all__ = ["ModelProfile", "ModelRouter", "compare", "main", "select_model"]
