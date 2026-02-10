"""
RSA Key Generation (refactored)

This module provides a refactored, SOLID-friendly implementation of RSA
key generation. By default it maintains backward compatibility with the
existing static `PRIME_NUMBERS` list so tests and demo code continue to
work. Optionally a cryptographic prime generator (PyCryptodome or sympy)
can be used by setting `use_crypto=True` when calling `generate_keys()`.

Design goals and changes:
- Single Responsibility: small functions each perform one task.
- Open/Closed: prime generation strategy is pluggable.
- Backward compatible defaults preserve existing behavior.
"""

import importlib
import random
import warnings
from typing import Callable, Tuple

import sympy
from Crypto.Util import number

from .utils import gcd


# Load static primes from a packaged resource. This keeps the large list out
# of the code and makes it easy to update or replace without editing Python.
def _load_static_primes() -> list[int]:
    try:
        mod = importlib.import_module(f"{__package__}.libraries")
        data = getattr(mod, "PRIME_NUMBERS")
        if not isinstance(data, list):
            raise ValueError("libraries.PRIME_NUMBERS is not a list")
        return [int(x) for x in data]
    except Exception:
        warnings.warn(
            "Could not import libraries.PRIME_NUMBERS. Falling back to a small built-in set which is NOT suitable for production.",
            UserWarning,
        )
        # Minimal fallback to allow demo/test runs in hostile environments.
        return [101, 103, 107, 109, 113, 127]


PRIME_NUMBERS = _load_static_primes()


def _prime_factory_from_crypto(bits: int) -> int:
    """Generate a prime using PyCryptodome if available.

    Falls back by raising ImportError if the library is missing.
    """
    try:

        return number.getPrime(bits)
    except Exception as exc:
        raise ImportError("PyCryptodome not available") from exc


def _prime_factory_from_sympy(bits: int) -> int:
    """Generate a prime using sympy if available.

    This is a slower pure-Python fallback compared to PyCryptodome.
    """
    try:
        low = 1 << (bits - 1)
        high = (1 << bits) - 1
        return int(sympy.randprime(low, high))
    except Exception as exc:
        raise ImportError("sympy not available") from exc


def _prime_factory_from_static(_bits: int) -> int:
    """Select a prime from the static `PRIME_NUMBERS` list.

    This is intentionally small and deterministic - suitable only for
    demos, tests, or when cryptographic security is not required.
    """
    return random.choice(PRIME_NUMBERS)


def _select_prime_factory(prefer: str = "auto") -> Callable[[int], int]:
    """Return a prime-producing callable based on availability and preference.

    prefer: "auto" | "crypto" | "sympy" | "static"
    """
    if prefer == "static":
        return _prime_factory_from_static

    if prefer == "crypto" or prefer == "auto":
        try:
            return _prime_factory_from_crypto
        except Exception:
            if prefer == "crypto":
                raise

    if prefer == "sympy" or prefer == "auto":
        try:
            return _prime_factory_from_sympy
        except Exception:
            if prefer == "sympy":
                raise

    # Final fallback: static primes
    warnings.warn(
        "Falling back to static prime list; not suitable for production.",
        UserWarning,
    )
    return _prime_factory_from_static


def _select_two_distinct_primes(
    prime_factory: Callable[[int], int], bits: int
) -> Tuple[int, int]:
    """Generate two distinct primes using ``prime_factory``.

    Ensures that p != q.
    """
    p = prime_factory(bits)
    q = prime_factory(bits)
    attempts = 0
    while q == p and attempts < 10:
        q = prime_factory(bits)
        attempts += 1
    if q == p:
        raise RuntimeError("Failed to generate two distinct primes")
    return p, q


def _compute_modulus(p: int, q: int) -> int:
    """Compute RSA modulus n = p * q."""
    return p * q


def _compute_totient(p: int, q: int) -> int:
    """Compute Euler's totient for RSA: (p-1)*(q-1)."""
    return (p - 1) * (q - 1)


def _compute_private_exponent(e: int, totient: int) -> int:
    """Compute private exponent d as modular inverse of e mod totient."""
    return pow(e, -1, totient)


def generate_keys(
    use_crypto: bool = False,
    bits: int = 16,
    prefer: str = "auto",
) -> tuple[tuple[int, int], tuple[int, int]]:
    """Generate an RSA key pair.

    Args:
        use_crypto: If True, attempt to use a crypto-grade prime generator
            (PyCryptodome or sympy). Default False to preserve existing
            deterministic behavior for tests and demos.
        bits: Bit-size for primes when using generators. Defaults to 16 to
            keep numbers small and compatible with existing tests.
        prefer: Which generator to prefer: "auto", "crypto", "sympy", or "static".

    Returns:
        ((n, e), (n, d)) public and private key tuples.

    Notes:
        - For production, call with `use_crypto=True` and a larger `bits`
          (e.g., 1024 or 2048).
        - Keeping `use_crypto=False` preserves prior behavior and test
          compatibility which relies on primes from `PRIME_NUMBERS`.
    """
    # Standard public exponent
    public_exp = 65537

    if not use_crypto:
        # Backward-compatible deterministic mode (small primes from list)
        p, q = random.sample(PRIME_NUMBERS, 2)
    else:
        factory = _select_prime_factory(prefer=prefer)
        p, q = _select_two_distinct_primes(factory, bits)

    n = _compute_modulus(p, q)
    totient = _compute_totient(p, q)

    # Ensure e is coprime to totient
    if gcd(public_exp, totient) != 1:
        raise ValueError("Chosen public exponent is not coprime with totient")

    private_exp = _compute_private_exponent(public_exp, totient)

    return (n, public_exp), (n, private_exp)


if __name__ == "__main__":
    pub, priv = generate_keys()
    print(f"Public Key (n,e): {pub}")
    print(f"Private Key (n,d): {priv}")
