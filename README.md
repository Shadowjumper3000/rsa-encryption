## Library Usage

You can use the RSA encryption library in your own Python code after installing in editable mode:

```bash
pip install -e .
```

### Example: Encrypt and Decrypt a Message

```python
from rsa_encryption.key_generation import generate_keys
from rsa_encryption.encryption import rsa_encrypt
from rsa_encryption.decryption import rsa_decrypt

alphabet = "abcdefghijklmnopqrstuvwxyz "
public_key, private_key = generate_keys()
n, e = public_key
n, d = private_key
message = "hello world"

encrypted = rsa_encrypt(alphabet, n, e, message)
decrypted = rsa_decrypt(alphabet, n, d, encrypted)
print("Encrypted:", encrypted)
print("Decrypted:", decrypted)
```

### Public API

- `generate_keys(use_crypto=False, bits=16, prefer="auto")` → `((n, e), (n, d))`: Generate RSA key pairs.
- `rsa_encrypt(alphabet, n, e, message)` → `str`: Encrypt a message.
- `rsa_decrypt(alphabet, n, d, encrypted_message)` → `str`: Decrypt a message.

See docstrings in the code for more details.
# RSA Encryption Tool

A Python implementation of RSA encryption for educational purposes with both CLI and library interfaces, demonstrating public-key cryptography concepts.
## ToDo
- [] Fix padding being stripped on decryption for single block messages
- [] Add more prime numbers to the prime list for key generation
## Features

- **Command Line Interface**: Easy-to-use CLI for all RSA operations
- **RSA Key Generation**: Generate secure RSA key pairs using randomly selected prime numbers
- **Message Encryption**: Encrypt text messages using RSA public keys
- **Message Decryption**: Decrypt encrypted messages using RSA private keys
- **Flexible Alphabets**: Support for various character sets:
  - `basic`: Lowercase letters and space (27 chars)
  - `extended`: Lowercase, uppercase letters and space (53 chars)
  - `full`: Letters, numbers, and space (63 chars)
  - `numeric`: Numbers and space (11 chars)
  - Custom: Any custom alphabet string
- **File I/O**: Save/load keys and messages to/from files
- **Block Processing**: Intelligent block-based message handling for longer texts
- **Comprehensive Testing**: Full test suite with unit and integration tests

## Installation

```bash
git clone https://github.com/Shadowjumper3000/RSA-Encryption.git
cd RSA-Encryption
```

## CLI Usage

The main interface is through the command line using `main.py`:

### Generate Keys

```bash
# Generate keys and display them
python main.py generate-keys

# Save keys to a JSON file
python main.py generate-keys --output keys.json
```

### Encrypt Messages

```bash
# Encrypt with saved keys (interactive message input)
python main.py encrypt --key-file keys.json --alphabet basic

# Encrypt with explicit message and keys
python main.py encrypt --key-file keys.json --message "hello world" --alphabet basic

# Encrypt with explicit key values
python main.py encrypt --n 1091218173 --e 65537 --message "hello" --alphabet basic

# Save encrypted message to file
python main.py encrypt --key-file keys.json --message "secret" --alphabet basic --output encrypted.txt
```

### Decrypt Messages

```bash
# Decrypt with saved keys (interactive input)
python main.py decrypt --key-file keys.json --alphabet basic

# Decrypt explicit message
python main.py decrypt --key-file keys.json --message "123456789" --alphabet basic

# Decrypt from file
python main.py decrypt --key-file keys.json --input encrypted.txt --alphabet basic

# Decrypt with explicit key values
python main.py decrypt --n 1091218173 --d 987654321 --message "123456789" --alphabet basic
```

### Alphabet Information

```bash
# Show available alphabet types
python main.py alphabet-info
```

## Library Usage

You can also use the package as a Python library:

```python
from rsa_encryption import generate_keys, rsa_encrypt, rsa_decrypt
"""RSA Encryption — concise

Small educational RSA implementation (key generation, encryption,
decryption). Refactors split encryption/decryption into small helpers and
moved shared utilities into `src/rsa_encryption/utils.py`.

Quickstart
----------

Clone and run tests:

```bash
git clone https://github.com/Shadowjumper3000/RSA-Encryption.git
cd RSA-Encryption
python -m venv .venv
source .venv/bin/activate
python -m unittest discover tests -v
```

Library usage (example):

```python
from rsa_encryption import generate_keys, rsa_encrypt, rsa_decrypt
pub, priv = generate_keys()
n, e = pub
_, d = priv
alphabet = "abcdefghijklmnopqrstuvwxyz "
msg = "hello world"
enc = rsa_encrypt(alphabet, n, e, msg)
dec = rsa_decrypt(alphabet, n, d, enc)
assert dec == msg
```

CLI: use `main.py` for `generate-keys`, `encrypt`, `decrypt`, and
`alphabet-info` commands (see CLI help for details).

Notes
-----

- Educational only — not production-ready. Use audited libraries and OAEP
  padding for real-world use.
- Recent refactors preserved public APIs; full test suite passes.

Contributing
------------

PRs welcome. Open an issue for major changes.
"""
## Development
