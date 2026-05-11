# Testing Guide

## Run Full Test Suite

```bash
source .venv/bin/activate
python -m unittest discover tests -v
```

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
