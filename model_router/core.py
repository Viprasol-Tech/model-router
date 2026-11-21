"""
Model router - Intelligent model selection based on task requirements.

Cost vs quality comparison, latency considerations, fallback handling.
"""

from dataclasses import dataclass


@dataclass
class ModelProfile:
    """Model performance profile."""

    name: str
    speed: float  # Relative throughput score (higher = faster); used as tokens/second
    quality: float  # Relative quality score 0-100 (illustrative; set your own)
    cost_per_1m_tokens: float  # Input cost
    max_context: int  # Maximum context window
    best_for: list[str] | None = None  # Task types

    def __post_init__(self):
        if self.best_for is None:
            self.best_for = []

    @property
    def efficiency_score(self) -> float:
        """Quality per dollar."""
        if self.cost_per_1m_tokens == 0:
            return float("inf")
        return self.quality / self.cost_per_1m_tokens


class ModelRouter:
    """Route requests to best model.

    The built-in profiles are illustrative defaults. Add or replace entries in
    ``ModelRouter.MODELS`` with the models, prices and scores you actually use.
    """

    MODELS = {
        "claude-3-opus": ModelProfile(
            name="claude-3-opus",
            speed=5.0,
            quality=95,
            cost_per_1m_tokens=15.0,
            max_context=200_000,
            best_for=["complex-reasoning", "coding", "analysis"],
        ),
        "claude-3-sonnet": ModelProfile(
            name="claude-3-sonnet",
            speed=15.0,
            quality=85,
            cost_per_1m_tokens=3.0,
            max_context=200_000,
            best_for=["general", "content", "summary"],
        ),
        "claude-3-haiku": ModelProfile(
            name="claude-3-haiku",
            speed=50.0,
            quality=70,
            cost_per_1m_tokens=0.25,
            max_context=200_000,
            best_for=["quick-responses", "classification"],
        ),
        "gpt-4-turbo": ModelProfile(
            name="gpt-4-turbo",
            speed=20.0,
            quality=90,
            cost_per_1m_tokens=10.0,
            max_context=128_000,
            best_for=["vision", "complex", "coding"],
        ),
        "gpt-3.5-turbo": ModelProfile(
            name="gpt-3.5-turbo",
            speed=40.0,
            quality=75,
            cost_per_1m_tokens=0.5,
            max_context=16_385,
            best_for=["fast", "simple"],
        ),
    }

    @classmethod
    def select_by_task(cls, task_type: str) -> str:
        """Select best model for task type."""
        candidates = [m for m in cls.MODELS.values() if task_type in m.best_for]

        if not candidates:
            # Default to Sonnet if no match
            return "claude-3-sonnet"

        # Return best quality for task
        return max(candidates, key=lambda m: m.quality).name

    @classmethod
    def select_by_budget(cls, max_cost: float, min_quality: float = 70) -> str | None:
        """Select model within budget and quality threshold."""
        candidates = [
            m
            for m in cls.MODELS.values()
            if m.cost_per_1m_tokens <= max_cost and m.quality >= min_quality
        ]

        if not candidates:
            return None

        # Return most efficient (quality per dollar)
        return max(candidates, key=lambda m: m.efficiency_score).name

    @classmethod
    def select_by_speed(cls, max_latency_ms: float, min_quality: float = 70) -> str | None:
        """Select fastest model meeting quality threshold."""
        candidates = [
            m
            for m in cls.MODELS.values()
            if m.speed > 0 and (1000 / m.speed) <= max_latency_ms and m.quality >= min_quality
        ]

        if not candidates:
            return None

        return max(candidates, key=lambda m: m.speed).name

    @classmethod
    def select_by_context(cls, required_tokens: int) -> str | None:
        """Select model with sufficient context."""
        candidates = [m for m in cls.MODELS.values() if m.max_context >= required_tokens]

        if not candidates:
            return None

        # Return cheapest that fits
        return min(candidates, key=lambda m: m.cost_per_1m_tokens).name

    @classmethod
    def compare_models(cls, model_names: list[str] | None = None) -> dict:
        """Compare models side by side."""
        if model_names is None:
            models = cls.MODELS.values()
        else:
            models = [cls.MODELS.get(name) for name in model_names if name in cls.MODELS]

        comparison = {"models": {}}

        for model in models:
            comparison["models"][model.name] = {
                "speed": model.speed,
                "quality": model.quality,
                "cost_per_1m": model.cost_per_1m_tokens,
                "max_context": model.max_context,
                "efficiency": round(model.efficiency_score, 2),
                "best_for": model.best_for,
            }

        return comparison

    @classmethod
    def recommend(
        cls,
        task: str | None = None,
        budget: float | None = None,
        speed: float | None = None,
        context: int | None = None,
    ) -> dict:
        """Get recommendation based on criteria."""
        recommendations = []

        if task:
            model = cls.select_by_task(task)
            recommendations.append(("by_task", model))

        if budget is not None:
            model = cls.select_by_budget(budget)
            if model:
                recommendations.append(("by_budget", model))

        if speed is not None:
            model = cls.select_by_speed(speed)
            if model:
                recommendations.append(("by_speed", model))

        if context is not None:
            model = cls.select_by_context(context)
            if model:
                recommendations.append(("by_context", model))

        return {
            "recommendations": recommendations,
            "primary": recommendations[0][1] if recommendations else "claude-3-sonnet",
        }


def select_model(task: str | None = None, budget: float | None = None) -> str | None:
    """Quick model selection."""
    if task:
        return ModelRouter.select_by_task(task)
    elif budget is not None:
        return ModelRouter.select_by_budget(budget)
    else:
        return "claude-3-sonnet"


def compare(models: list[str] | None = None) -> dict:
    """Compare models."""
    return ModelRouter.compare_models(models)


def main(argv: list[str] | None = None) -> None:
    """CLI entry point."""
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Route requests to optimal model")
    parser.add_argument("--task", help="Task type")
    parser.add_argument("--budget", type=float, help="Max cost per 1M tokens")
    parser.add_argument("--speed", type=float, help="Max latency in ms")
    parser.add_argument("--context", type=int, help="Required context tokens")
    parser.add_argument("--compare", nargs="+", help="Compare models")

    args = parser.parse_args(argv)

    if args.compare:
        result = ModelRouter.compare_models(args.compare)
        print(json.dumps(result, indent=2))
    else:
        rec = ModelRouter.recommend(
            task=args.task, budget=args.budget, speed=args.speed, context=args.context
        )
        print(f"Recommended: {rec['primary']}")


if __name__ == "__main__":
    main()
