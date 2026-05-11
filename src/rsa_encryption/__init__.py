"""Public package API for ``rsa_encryption``."""

from importlib.metadata import PackageNotFoundError, version

from .decryption import rsa_decrypt
from .encryption import rsa_encrypt
from .key_generation import PRIME_NUMBERS, generate_keys, gcd
from .libraries import ALPHABETS
from .exceptions import ValidationError

try:
    __version__ = version("rsa-encryption")
except PackageNotFoundError:
    __version__ = "2.0.2"

__all__ = [
    "ALPHABETS",
    "PRIME_NUMBERS",
    "generate_keys",
    "gcd",
    "rsa_encrypt",
    "rsa_decrypt",
    "ValidationError",
]
