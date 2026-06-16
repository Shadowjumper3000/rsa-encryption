# rsa-encryption

[![CI](https://github.com/Shadowjumper3000/rsa-encryption/actions/workflows/ci.yml/badge.svg)](https://github.com/Shadowjumper3000/rsa-encryption/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/rsa-encryption)](https://pypi.org/project/rsa-encryption/)
[![Python versions](https://img.shields.io/pypi/pyversions/rsa-encryption)](https://pypi.org/project/rsa-encryption/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Educational RSA package with a clean Python library API and CLI. Demonstrates
RSA key generation, message encryption, and decryption using a configurable
alphabet. Designed for learning and experimentation.

**No third-party runtime dependencies are required.**

> **Security Warning**: This package is educational. It does not implement
> production safeguards such as OAEP padding or side-channel hardened operations.
> Use vetted crypto libraries for real-world security use cases.

---

## About

`rsa-encryption` was created to provide a clear, well-structured reference
implementation of RSA cryptography for students and developers learning about
public-key encryption. The codebase is intentionally small and self-contained.

### Goals

- **Educational clarity** — each module has one responsibility; functions are
  short and testable.
- **No runtime dependencies** — pure Python standard library.
- **Extensibility** — prime providers, alphabets, and encryption strategies
  are pluggable.
- **Production-quality engineering** — even though the crypto is educational,
  the project follows professional practices: CI/CD, type checking, linting,
  thorough testing, semantic versioning, and automated releases.

### Non-goals

- Production-grade security (OAEP, side-channel resistance, large prime
  sizes). This is not a substitute for `cryptography`, `PyCryptodome`, or
  similar vetted libraries.

---

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install rsa-encryption
```

For development:

```bash
git clone https://github.com/Shadowjumper3000/rsa-encryption.git
cd rsa-encryption
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

---

## Quickstart (Library)

```python
from rsa_encryption import generate_keys, rsa_encrypt, rsa_decrypt, ALPHABETS

alphabet = ALPHABETS["basic"]
(public_n, public_e), (_, private_d) = generate_keys()

message = "hello world"
encrypted = rsa_encrypt(alphabet, public_n, public_e, message)
decrypted = rsa_decrypt(alphabet, public_n, private_d, encrypted)

assert decrypted == message
```

---

## Public API

| Function / Constant | Description |
|---|---|
| `generate_keys(use_crypto, bits, prefer, prime_provider)` | Returns `((n, e), (n, d))`. Supports dependency injection for custom prime providers. |
| `rsa_encrypt(alphabet, modulus, public_exponent, message)` | Encrypts plaintext to digit-only ciphertext string. |
| `rsa_decrypt(alphabet, modulus, private_exponent, encrypted_message)` | Decrypts ciphertext back to plaintext. Enforces strict validation. |
| `ALPHABETS` | Packaged presets: `basic`, `extended`, `full`, `numeric`. |
| `PRIME_NUMBERS` | Static prime list used in default (deterministic) key generation. |
| `ValidationError` | Exception raised on invalid input. Subclass of `ValueError`. |

---

## CLI Usage

```bash
# Show help
rsa-encrypt --help

# Generate keys
rsa-encrypt generate-keys --output keys.json

# Encrypt
rsa-encrypt encrypt --key-file keys.json --message "hello world" --alphabet basic

# Decrypt
rsa-encrypt decrypt --key-file keys.json --message "<encrypted_digits>" --alphabet basic

# Show packaged alphabets
rsa-encrypt alphabet-info
```

---

## Architecture

```
src/rsa_encryption/
├── __init__.py       # Public API exports, version detection
├── __main__.py       # `python -m rsa_encryption` entry point
├── cli.py            # Argument parsing and command orchestration
├── key_generation.py # Key creation, prime-provider strategy, Miller-Rabin
├── encryption.py     # Plaintext validation, mapping, chunking, block encryption
├── decryption.py     # Input validation, block decryption, reverse mapping
├── utils.py          # Shared utilities (block sizing, alphabet validation, GCD)
├── exceptions.py     # ValidationError exception class
└── libraries.py      # Packaged alphabet and prime data
```

Design principles:

- **Single Responsibility** — each module and function has one job.
- **Dependency Inversion** — prime providers are injectable; custom strategies
  need only implement `generate_prime(bits: int) -> int`.
- **No magic** — all logic is explicit and traceable through the standard
  library.

---

## Git Workflow

```
feature/*  ──→  main  ──→  GitHub Release (tag) ──→  prod
                    │                                       │
                staging deploy (auto)                   PyPI publish
                                                        + version bump
```

| Branch       | Purpose                                                   |
|--------------|-----------------------------------------------------------|
| `feature/*`  | Short-lived branches. PR into `main`.                     |
| `main`       | Integration + staging. CI runs on every push/PR.          |
| GitHub Release | Triggered from `main`; creates tag + deploys to prod.  |

**How it works:**

1. All development happens on feature branches branched from `main`.
2. Once reviewed, feature branches are squashed into `main`.
3. Every push to `main` triggers CI (tests, linting, typing, security)
   and an automatic staging deployment.
4. To release: create a **GitHub Release** from `main`. The release workflow:
   - Bumps the version in `pyproject.toml` (following semver).
   - Creates and pushes a Git tag (`vX.Y.Z`).
   - Builds the package and publishes to PyPI.

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contributor guidance.

---

## Open Source & Collaboration

This project is open source under the MIT license. Contributions are welcome!

- **Issues**: Bug reports, feature requests, and questions.
- **Pull Requests**: See [CONTRIBUTING.md](CONTRIBUTING.md) for the PR process
  and commit conventions.
- **Security**: Report vulnerabilities privately per [SECURITY.md](SECURITY.md).

All participants are expected to follow the [Contributor Covenant](https://www.contributor-covenant.org/).

---

## Documentation

| Resource | Description |
|---|---|
| [API.md](docs/API.md) | Full API reference for all public functions and constants. |
| [EDGE_CASES.md](docs/EDGE_CASES.md) | Validation rules and edge-case behavior. |
| [TESTING.md](docs/TESTING.md) | Testing strategy, coverage areas, and how to run tests. |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contributor guide, code style, release cycle. |
| [CHANGELOG.md](CHANGELOG.md) | Version history and release notes. |
| [SECURITY.md](SECURITY.md) | Security policy and vulnerability reporting. |

---

## Development

```bash
source .venv/bin/activate

# Run tests
python -m unittest discover tests -v

# Lint and format
ruff check src/ tests/
ruff format --check src/ tests/

# Type check
mypy src/

# Security scan
bandit -r src/

# Coverage
coverage run -m unittest discover tests && coverage report -m
```

---

## Release Cycle

Releases follow [Semantic Versioning](https://semver.org/).

| Version | When |
|---------|------|
| PATCH   | Bug fixes, documentation |
| MINOR   | New features (backwards-compatible) |
| MAJOR   | Breaking API changes |

To trigger a release, create a [GitHub Release](https://github.com/Shadowjumper3000/rsa-encryption/releases/new)
from `main`. The CI pipeline handles version bumping, tagging, and PyPI publishing
automatically.

---

*Built with Python standard library. No batteries required.*
