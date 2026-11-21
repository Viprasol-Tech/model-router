<div align="center">

<img src="docs/assets/logo.png" alt="Viprasol Tech logo" width="120" />

# model-router

**Pick the right LLM for each request by task, budget, latency or context size.**

_Built and maintained by [Viprasol Tech](https://viprasol.com) — Fintech Experts. Full-Stack Builders._

[![CI](https://img.shields.io/github/actions/workflow/status/Viprasol-Tech/model-router/ci.yml?branch=main&style=flat-square&label=CI)](https://github.com/Viprasol-Tech/model-router/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-black?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square)](https://www.python.org/)
[![Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen?style=flat-square)](pyproject.toml)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-261230?style=flat-square)](https://github.com/astral-sh/ruff)

</div>

---

`model-router` chooses a model from a table of model profiles. Ask for the best model for a task, the most quality per dollar under a budget, the fastest model under a latency limit, or the cheapest model whose context window fits your prompt. It is a small Python library and CLI with zero dependencies, so you can drop the routing rule into any service.

> **Bring your own profiles.** The built-in table holds example profiles for a few well-known models, with list input prices, published context windows and **illustrative** speed and quality scores. Replace them with the models you use and scores from your own evaluations.

## ✨ Features

- 🎯 **By task:** the highest-quality model tagged for the task (`coding`, `summary`, `classification`, ...).
- 💰 **By budget:** the best quality per dollar under a price per 1M input tokens, with a minimum quality.
- ⚡ **By latency:** the fastest model under a per-token latency limit.
- 📏 **By context:** the cheapest model whose context window fits.
- 🧭 **Combined recommendation** and a side-by-side comparison table.
- 🖥️ **CLI** (`model-router`); zero runtime dependencies.

## 🚀 Quickstart

```bash
git clone https://github.com/Viprasol-Tech/model-router.git
cd model-router
pip install -e .

model-router --task coding                        # Recommended: claude-3-opus
model-router --budget 1 --context 100000          # Recommended: claude-3-haiku
model-router --compare claude-3-haiku gpt-4-turbo # JSON comparison
```

## 🐍 Python API

```python
from model_router import ModelProfile, ModelRouter

ModelRouter.select_by_task("coding")  # 'claude-3-opus'
ModelRouter.select_by_budget(1.0, min_quality=75)  # 'gpt-3.5-turbo'
ModelRouter.select_by_context(150_000)  # 'claude-3-haiku'
ModelRouter.recommend(task="coding", budget=1.0)["primary"]

# Add your own model (name, speed, quality, USD per 1M input tokens, context, tasks):
ModelRouter.MODELS["my-model"] = ModelProfile(
    "my-model",
    speed=60.0,
    quality=82,
    cost_per_1m_tokens=0.8,
    max_context=128_000,
    best_for=["summary", "classification"],
)
```

`select_by_budget`, `select_by_speed` and `select_by_context` return `None` when no model qualifies, so you can decide the fallback.

## ⚙️ CLI options

| Option | Meaning |
|---|---|
| `--task TYPE` | Best model tagged for this task |
| `--budget USD` | Max price per 1M input tokens |
| `--speed MS` | Max latency per token in milliseconds |
| `--context N` | Tokens the context window must hold |
| `--compare A B ...` | Print a JSON comparison of these models |

With several criteria, the first match in the order task, budget, speed, context is the primary recommendation.

## 🧪 Development

```bash
pip install -e ".[dev]"
ruff check . && ruff format --check . && pytest
```

## 🤝 Contributing

PRs are welcome. Run `ruff check . && ruff format --check . && pytest` before you open one.

## 📬 Contact — Viprasol Tech Private Limited

- 🌐 Website: [viprasol.com](https://viprasol.com)
- ✉️ Email: [support@viprasol.com](mailto:support@viprasol.com)
- 💬 Telegram: [t.me/viprasol_help](https://t.me/viprasol_help) · 📱 WhatsApp: +91 96336 52112
- 🐙 GitHub: [@Viprasol-Tech](https://github.com/Viprasol-Tech) · 💼 [LinkedIn](https://www.linkedin.com/in/viprasol/) · 𝕏 [@viprasol](https://twitter.com/viprasol)

> *Viprasol Tech builds fintech software, algorithmic trading systems, MT4/MT5 bots, AI voice agents, and B2B SaaS. Need a custom build? [Get in touch](mailto:support@viprasol.com).*

## License

[MIT](LICENSE) © 2026 Viprasol Tech Private Limited
