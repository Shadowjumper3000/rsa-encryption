"""
RSA Encryption Package (src layout)

This package is the same as the original `rsa_encryption` package
but placed under `src/` for a standard src-layout Python project.
"""

from .key_generation import generate_keys, gcd
from .encryption import rsa_encrypt
from .decryption import rsa_decrypt

__version__ = "1.0.0"
__all__ = ["generate_keys", "gcd", "rsa_encrypt", "rsa_decrypt"]
