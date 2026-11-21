import json

import pytest

from model_router import ModelProfile, ModelRouter, compare, main, select_model


def test_select_by_task_picks_highest_quality_match():
    assert ModelRouter.select_by_task("coding") == "claude-3-opus"
    assert ModelRouter.select_by_task("classification") == "claude-3-haiku"


def test_unknown_task_falls_back_to_default():
    assert ModelRouter.select_by_task("knitting") == "claude-3-sonnet"


def test_select_by_budget_respects_price_and_quality():
    assert ModelRouter.select_by_budget(1.0) == "claude-3-haiku"
    assert ModelRouter.select_by_budget(1.0, min_quality=75) == "gpt-3.5-turbo"
    assert ModelRouter.select_by_budget(0.1) is None


def test_select_by_context_returns_cheapest_that_fits():
    assert ModelRouter.select_by_context(16_000) == "claude-3-haiku"
    assert ModelRouter.select_by_context(150_000) == "claude-3-haiku"
    assert ModelRouter.select_by_context(1_000_000) is None


def test_select_by_speed():
    assert ModelRouter.select_by_speed(30) == "claude-3-haiku"
    assert ModelRouter.select_by_speed(1, min_quality=90) is None


def test_compare_skips_unknown_models():
    result = compare(["gpt-4-turbo", "not-a-model"])
    assert list(result["models"]) == ["gpt-4-turbo"]
    assert result["models"]["gpt-4-turbo"]["efficiency"] == 9.0


def test_recommend_orders_criteria():
    rec = ModelRouter.recommend(task="coding", budget=1.0)
    assert rec["recommendations"] == [("by_task", "claude-3-opus"), ("by_budget", "claude-3-haiku")]
    assert rec["primary"] == "claude-3-opus"


def test_custom_profiles_are_used():
    ModelRouter.MODELS["tiny"] = ModelProfile("tiny", 100.0, 72, 0.05, 8_000, ["classification"])
    try:
        assert ModelRouter.select_by_budget(0.1) == "tiny"
    finally:
        del ModelRouter.MODELS["tiny"]


def test_select_model_helper():
    assert select_model(task="coding") == "claude-3-opus"
    assert select_model(budget=0.1) is None
    assert select_model() == "claude-3-sonnet"


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        (["--task", "coding"], "Recommended: claude-3-opus\n"),
        (["--budget", "1", "--context", "100000"], "Recommended: claude-3-haiku\n"),
    ],
)
def test_cli_recommend(capsys, argv, expected):
    main(argv)
    assert capsys.readouterr().out == expected


def test_cli_compare(capsys):
    main(["--compare", "claude-3-haiku", "gpt-4-turbo"])
    assert set(json.loads(capsys.readouterr().out)["models"]) == {"claude-3-haiku", "gpt-4-turbo"}
