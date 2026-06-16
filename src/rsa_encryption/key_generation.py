"""RSA key generation.

This module keeps default behavior compatible with earlier versions while
improving library ergonomics and separation of concerns.

Design notes:
- Single Responsibility: each helper has one job.
- Open/Closed + Dependency Inversion: prime generation strategy can be
  injected via ``prime_provider``.
- No external dependencies are required. Prime generation is implemented
    in pure Python.
"""

import importlib
import random
import warnings
from typing import Callable, List, Optional, Protocol, Tuple

from .utils import gcd

__all__ = [
    "PRIME_NUMBERS",
    "generate_keys",
    "gcd",
]


class PrimeProvider(Protocol):
    """Protocol for pluggable prime generators."""

    def generate_prime(self, bits: int) -> int:
        """Return a prime number with approximately ``bits`` bits."""


class StaticPrimeProvider:
    """Prime provider that samples from a static list."""

    def __init__(
        self,
        primes: List[int],
        chooser: Optional[Callable[[List[int]], int]] = None,
    ) -> None:
        if len(primes) < 2:
            from .exceptions import ValidationError

            raise ValidationError("At least two primes are required")
        self._primes = primes
        self._chooser = chooser or random.choice

    def generate_prime(self, _bits: int) -> int:
        return int(self._chooser(self._primes))


def _is_probable_prime(candidate: int, rounds: int = 8) -> bool:
    """Return True when candidate passes Miller-Rabin primality checks."""
    if candidate < 2:
        return False

    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)
    for prime in small_primes:
        if candidate == prime:
            return True
        if candidate % prime == 0:
            return False

    # Decompose candidate - 1 as d * 2^r where d is odd.
    d = candidate - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    # Use a system RNG for witness selection to avoid relying on the global
    # PRNG state when this function is used in a cryptographic context.
    sysrand = random.SystemRandom()
    for _ in range(rounds):
        witness = sysrand.randrange(2, candidate - 1)
        x = pow(witness, d, candidate)
        if x in (1, candidate - 1):
            continue

        for _ in range(r - 1):
            x = pow(x, 2, candidate)
            if x == candidate - 1:
                break
        else:
            return False

    return True


def _generate_internal_prime(bits: int) -> int:
    """Generate a prime using pure-Python Miller-Rabin testing."""
    if bits < 2:
        from .exceptions import ValidationError

        raise ValidationError("bits must be >= 2")

    # Use a system RNG for prime candidate generation when in crypto mode.
    sysrand = random.SystemRandom()
    while True:
        candidate = sysrand.getrandbits(bits)
        # Ensure requested bit length and odd parity.
        candidate |= 1 << (bits - 1)
        candidate |= 1
        if _is_probable_prime(candidate):
            return candidate


class InternalPrimeProvider:
    """Prime provider implemented entirely with standard library code."""

    def generate_prime(self, bits: int) -> int:
        return _generate_internal_prime(bits)


# Load static primes from a packaged resource. This keeps the large list out
# of the code and makes it easy to update or replace without editing Python.
def _load_static_primes() -> List[int]:
    try:
        mod = importlib.import_module(f"{__package__}.libraries")
        data = getattr(mod, "PRIME_NUMBERS")
        if not isinstance(data, list):
            raise ValueError("libraries.PRIME_NUMBERS is not a list")
        return [int(x) for x in data]
    except Exception:
        warnings.warn(
            "Could not import libraries.PRIME_NUMBERS.",
            UserWarning,
        )
        # Minimal fallback to allow demo/test runs in hostile environments.
        return [101, 103, 107, 109, 113, 127]


PRIME_NUMBERS = _load_static_primes()


def _select_prime_provider(use_crypto: bool, prefer: str) -> PrimeProvider:
    """Select a prime provider from runtime configuration."""
    if prefer not in {"auto", "internal", "static"}:
        from .exceptions import ValidationError

        raise ValidationError("prefer must be one of: 'auto', 'internal', 'static'")

    static_provider = StaticPrimeProvider(PRIME_NUMBERS)

    if not use_crypto or prefer == "static":
        return static_provider

    return InternalPrimeProvider()


def _select_two_distinct_primes(
    prime_provider: PrimeProvider,
    bits: int,
    max_attempts: int = 20,
) -> Tuple[int, int]:
    """Generate two distinct primes using ``prime_factory``.

    Ensures that p != q.
    """
    p = prime_provider.generate_prime(bits)
    q = prime_provider.generate_prime(bits)
    attempts = 0
    while q == p and attempts < max_attempts:
        q = prime_provider.generate_prime(bits)
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
    prime_provider: Optional[PrimeProvider] = None,
) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Generate an RSA key pair.

    Args:
        use_crypto: If True, use the built-in probabilistic prime generator.
            Default False preserves historical behavior that samples from the
            packaged static prime list.
        bits: Bit-size for primes when using generators. Defaults to 16 to
            keep numbers small and compatible with existing tests.
        prefer: Which generator to prefer: "auto", "internal", or "static".
        prime_provider: Optional custom prime provider implementing
            ``generate_prime(bits: int) -> int``. When provided, this takes
            precedence over ``use_crypto`` and ``prefer``.

    Returns:
        ((n, e), (n, d)) public and private key tuples.

    Notes:
                - For stronger keys, call with `use_crypto=True` and a larger `bits`
          (e.g., 1024 or 2048).
        - Keeping `use_crypto=False` preserves prior behavior and test
          compatibility which relies on primes from `PRIME_NUMBERS`.
    """
    if bits < 2:
        from .exceptions import ValidationError

        raise ValidationError("bits must be >= 2")

    # Standard public exponent
    public_exp = 65537

    if prime_provider is not None:
        p, q = _select_two_distinct_primes(prime_provider, bits)
    elif not use_crypto:
        # Backward-compatible deterministic mode (small primes from list)
        p, q = random.sample(PRIME_NUMBERS, 2)  # nosec B311
    else:
        provider = _select_prime_provider(use_crypto=use_crypto, prefer=prefer)
        p, q = _select_two_distinct_primes(provider, bits)

    n = _compute_modulus(p, q)
    totient = _compute_totient(p, q)

    # Ensure e is coprime to totient
    if gcd(public_exp, totient) != 1:
        from .exceptions import ValidationError

        raise ValidationError("Chosen public exponent is not coprime with totient")

    private_exp = _compute_private_exponent(public_exp, totient)

    return (n, public_exp), (n, private_exp)


if __name__ == "__main__":
    pub, priv = generate_keys()
    print(f"Public Key (n,e): {pub}")
    print(f"Private Key (n,d): {priv}")
