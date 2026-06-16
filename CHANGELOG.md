# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Project governance files (CONTRIBUTING.md, SECURITY.md, CHANGELOG.md, LICENSE)
- Pre-commit configuration for automated code quality
- Automated staging deployment on push to `main`
- Automated release workflow: version bump + PyPI publish on GitHub Release
- CI quality gates: Ruff linting, MyPy typing, Bandit security scanning, coverage

### Changed
- README overhauled with About section, branching strategy, and collaboration guide
- CI workflow expanded to include quality checks beyond unit tests
- Tag-on-prod workflow replaced with semantic release pipeline

### Fixed
- LICENSE file was missing despite MIT classifier in package metadata

## [2.0.2] - 2025-06-16

### Added
- Edge case coverage for large alphabets (100+ symbols) and duplicate chars
- Library API tests for public exports, version presence, and provider injection
- EDGE_CASES.md and TESTING.md documentation

### Changed
- Pinned static prime list to deterministic values for reproducibility
- Decryption enforces strict padding sequence validation

### Fixed
- CLI atomic writes now use tempfile + os.replace to avoid partial outputs

## [2.0.1] - 2025-06-10

### Added
- Alphabet-info CLI command
- Support for custom alphabet strings via CLI

### Fixed
- Decryption now raises on non-numeric ciphertext

## [2.0.0] - 2025-06-05

### Added
- Full refactor into modular package structure
- Dependency-injectable prime providers
- `ValidationError` exception class
- Multi-alphabet support (basic, extended, full, numeric)
- Pure-Python Miller-Rabin prime generation
- CLI with generate-keys, encrypt, decrypt commands

### Changed
- Complete API redesign (breaking — see API.md)
- Minimum Python version raised to 3.8

### Removed
- Monolithic single-file implementation
- External cryptography library dependency

## [1.0.0] - 2025-05-20

### Added
- Initial release with basic RSA encryption/decryption
- Menu-driven CLI
- Single-alphabet support
