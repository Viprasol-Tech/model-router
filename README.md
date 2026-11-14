# Model Router

Intelligent model selection based on cost and performance

## Features

- Zero external dependencies (stdlib only)
- Easy-to-use CLI interface
- Professional Python implementation
- MIT licensed

## Installation

```bash
pip install -e .
```

Or clone and install:

```bash
git clone https://github.com/Viprasol-Tech/model-router
cd model-router
pip install -e .
```

## Usage

### Python

```python
from model_router import ModelRouter

print(ModelRouter.select_by_task("coding"))  # claude-3-opus
```

### CLI

```bash
python -m model_router --task coding
python -m model_router --budget 1 --context 100000
python -m model_router --compare claude-3-haiku gpt-4-turbo
```

## Documentation

See the source code and docstrings for detailed API documentation.

## License

MIT License - see LICENSE file for details

## About

Part of Viprasol Utilities: https://viprasol.com

Created by Viprasol - Building AI-focused tools for developers.
