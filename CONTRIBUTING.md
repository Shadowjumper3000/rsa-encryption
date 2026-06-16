# Contributing

Thank you for considering contributing to `rsa-encryption`! This is an educational
project, and contributions of all kinds — bug reports, feature ideas, docs, tests,
and code — are welcome.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style & Quality](#code-style--quality)
- [Testing](#testing)
- [Git Workflow](#git-workflow)
- [Pull Request Process](#pull-request-process)
- [Commit Conventions](#commit-conventions)
- [Release Cycle](#release-cycle)

## Code of Conduct

This project is governed by the [Contributor Covenant](https://www.contributor-covenant.org/).
By participating, you agree to uphold a harassment-free, inclusive environment for everyone.

## Getting Started

1. Fork the repository.
2. Clone your fork.
3. Set up the development environment (see below).
4. Create a feature branch from `main`.
5. Make your changes, write tests, run linting.
6. Push and open a pull request against `main`.

## Development Setup

```bash
git clone https://github.com/<your-username>/rsa-encryption.git
cd rsa-encryption

python -m venv .venv
source .venv/bin/activate

# Editable install with dev extras
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Code Style & Quality

This project enforces code quality automatically via pre-commit and CI:

| Tool     | Purpose                        | Config File            |
|----------|--------------------------------|------------------------|
| Ruff     | Linting + formatting           | `pyproject.toml`       |
| MyPy     | Static type checking           | `pyproject.toml`       |
| Bandit   | Security scanning              | `pyproject.toml`       |
| Pre-commit | Local quality gate            | `.pre-commit-config.yaml` |

Run all checks locally before pushing:

```bash
pre-commit run --all-files
```

Or invoke tools directly:

```bash
ruff check src/ tests/
ruff format --check src/ tests/
mypy src/
bandit -r src/
```

## Testing

```bash
# Run full test suite
python -m unittest discover tests -v

# Run with coverage
coverage run -m unittest discover tests
coverage report -m
coverage html   # Open htmlcov/index.html
```

Tests live in `tests/` and mirror the module structure. See [docs/TESTING.md](docs/TESTING.md)
for the testing strategy.

## Git Workflow

```
feature/*  ──→  main  ──→  GitHub Release (tag) ──→  prod
                    │                                       │
                staging deploy (auto)                   PyPI publish
                                                        + version bump
```

### Branches

| Branch       | Purpose                                                   |
|--------------|-----------------------------------------------------------|
| `feature/*`  | Short-lived feature branches. PR into `main`.             |
| `main`       | Integration + staging. CI runs on every push/PR.          |
| GitHub Release | Triggered from `main`; creates tag and deploys to prod. |

### Flow

1. Create a feature branch from `main`: `git checkout -b feature/my-thing main`
2. Commit with conventional commits (see below).
3. Open a PR against `main`. CI runs tests, linting, typing, coverage.
4. Squash-merge into `main` after review.
5. Every push to `main` triggers automatic staging deployment.
6. To release: create a **GitHub Release** from `main`. The release workflow:
   - Bumps the version in `pyproject.toml` (patch/minor/major as specified in the release).
   - Creates a signed Git tag (`vX.Y.Z`).
   - Builds and publishes to PyPI.

## Pull Request Process

1. Ensure your branch is up to date with `main`.
2. Write or update tests for your changes.
3. Run `pre-commit run --all-files` and fix any issues.
4. Keep PRs focused — one logical change per PR.
5. In the PR description, explain what and why, not how.
6. Reference any related issues.

## Commit Conventions

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add XXE resistance to XML parser
^───^  ^──────────────────────────────^
│      └─ description in imperative mood
│
type: feat, fix, docs, style, refactor, perf, test, ci, chore
```

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only
- **style**: Code style (formatting, no logic change)
- **refactor**: Code change that neither fixes nor adds
- **perf**: Performance improvement
- **test**: Adding or fixing tests
- **ci**: CI/CD changes
- **chore**: Tooling, dependencies, maintenance

Breaking changes: append `!` after the type, e.g., `feat!: change public API`.

## Release Cycle

Releases follow [Semantic Versioning](https://semver.org/).

| Version bump  | When                                    |
|---------------|-----------------------------------------|
| PATCH (1.0.x) | Bug fixes, minor docs changes           |
| MINOR (1.x.0) | New features, backwards-compatible      |
| MAJOR (x.0.0) | Breaking API changes                    |

To trigger a release:
1. Ensure `main` has the changes you want.
2. Go to GitHub → Releases → "Draft a new release".
3. The Release workflow handles version bump, tagging, and PyPI publishing automatically.

---
*This project is educational — keep it simple, keep it safe.*
