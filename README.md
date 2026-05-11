# rsa-encryption

Educational RSA package with a clean Python library API and CLI.

This project demonstrates RSA key generation, message encryption, and decryption
using a configurable alphabet. It is designed for learning and experimentation,
not production cryptography.

No third-party runtime dependencies are required.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

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

## Public API

- `generate_keys(use_crypto=False, bits=16, prefer="auto", prime_provider=None)`
  - Returns `((n, e), (n, d))`
  - Supports dependency injection via `prime_provider` for custom prime strategies
  - Uses built-in prime generation only (no external crypto libraries)
- `rsa_encrypt(alphabet, modulus, public_exponent, message)`
  - Returns encrypted numeric string
- `rsa_decrypt(alphabet, modulus, private_exponent, encrypted_message)`
  - Returns decrypted plaintext string
  - Enforces strict ciphertext validation and strict padding sequence checks
- `ALPHABETS`
  - Predefined alphabets: `basic`, `extended`, `full`, `numeric`
- `PRIME_NUMBERS`
  - Static prime list used in default key generation mode

## CLI Usage

Console script:

```bash
rsa-encrypt --help
```

Commands:

```bash
# Generate keys
rsa-encrypt generate-keys --output keys.json

# Encrypt
rsa-encrypt encrypt --key-file keys.json --message "hello world" --alphabet basic

# Decrypt
rsa-encrypt decrypt --key-file keys.json --message "<encrypted_digits>" --alphabet basic

# Show packaged alphabets
rsa-encrypt alphabet-info
```

## Architecture Notes

The codebase is organized around small, single-purpose functions:

- `key_generation.py`: key creation and prime-provider strategy selection
- `encryption.py`: plaintext validation, mapping, chunking, block encryption
- `decryption.py`: encrypted input validation, block decryption, reverse mapping
- `utils.py`: shared pure utility functions
- `cli.py`: argument parsing and command orchestration

SOLID-oriented improvements:

- Dependency inversion in key generation via injectable `prime_provider`
- Dependency-free runtime: all logic built with Python standard library
- Public package surface is explicitly exported through `rsa_encryption.__all__`

## Documentation

- API reference: [docs/API.md](docs/API.md)
- Edge cases and validation rules: [docs/EDGE_CASES.md](docs/EDGE_CASES.md)
- Testing strategy and coverage map: [docs/TESTING.md](docs/TESTING.md)

## Development

Run tests:

```bash
source .venv/bin/activate
python -m unittest discover tests -v
```

## Security Warning

This package is educational. It does not implement modern production safeguards
such as OAEP padding or side-channel hardened operations. Use vetted crypto
libraries for real-world security use cases.
