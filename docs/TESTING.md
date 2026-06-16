# Testing Guide

## Quality Gates

Before every commit (enforced by pre-commit and CI):

| Gate | Tool | Command |
|------|------|---------|
| Lint | Ruff | `ruff check src/ tests/` |
| Format | Ruff | `ruff format --check src/ tests/` |
| Type check | MyPy | `mypy src/` |
| Security | Bandit | `bandit -r src/ --quiet` |
| Tests | unittest | `python -m unittest discover tests -v` |
| Coverage | coverage | `coverage run -m unittest discover tests && coverage report -m` |

## Run Full Test Suite

```bash
source .venv/bin/activate
python -m unittest discover tests -v
```

## Coverage

```bash
coverage run -m unittest discover tests
coverage report -m          # Terminal report
coverage html               # Open htmlcov/index.html
```

Coverage threshold: **80%** minimum enforced in CI.

## Coverage Areas

- Unit tests for encryption behavior and invalid character handling.
- Unit tests for decryption behavior, malformed input, and strict ciphertext checks.
- Unit tests for key-generation math invariants.
- Integration tests for short, long, and multi-round-trip flows.
- API tests for public exports and prime-provider injection.
- Edge-case tests for:
  - large alphabets (100+ symbols)
  - empty/duplicate alphabets
  - too-small modulus
  - truncated ciphertext
  - invalid padding sequence

## Test Philosophy

- Favor deterministic assertions over print-based checks.
- Validate both success paths and explicit failure behavior.
- Treat malformed encrypted data as an error, not a recoverable warning.
