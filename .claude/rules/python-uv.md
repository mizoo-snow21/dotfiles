---
paths:
  - "**/*.py"
  - "**/*.pyi"
  - "**/pyproject.toml"
  - "**/uv.lock"
---

# Python Package Management

- Use `uv` for all Python dependency, environment, and script execution in this project.
- Do not use `pip`, `pip-tools`, `poetry`, `venv`, or `source .venv/bin/activate`.
- Use `uv add`, `uv remove`, `uv sync`, and `uv run`.
- For standalone scripts, prefer inline metadata or `uv add/remove/sync --script`.
