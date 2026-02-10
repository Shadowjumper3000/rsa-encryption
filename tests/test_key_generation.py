import unittest
import sys
import os

# Ensure tests import the package implementation from src/
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from rsa_encryption.key_generation import generate_keys, gcd, PRIME_NUMBERS


class TestKeyGeneration(unittest.TestCase):
    """Test cases for RSA key generation."""

    def test_gcd_basic_cases(self):
        """Test GCD function with basic cases."""
        test_cases = [
            (48, 18, 6),
            (54, 24, 6),
            (7, 13, 1),
            (28, 0, 28),
            (0, 28, 28),
            (17, 17, 17),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                self.assertEqual(gcd(a, b), expected)

    def test_gcd_large_numbers(self):
        """Test GCD with large numbers."""
        self.assertEqual(gcd(1071, 462), 21)
        self.assertEqual(gcd(32749, 32771), 1)

    def test_key_generation_consistency(self):
        """Test that key generation produces consistent results."""
        public_key, private_key = generate_keys()
        n_pub, e = public_key
        n_priv, d = private_key

        # Both keys should share the same modulus
        self.assertEqual(n_pub, n_priv)

        # Modulus should be product of two primes from our list
        factors = [p for p in PRIME_NUMBERS if n_pub % p == 0]
        self.assertEqual(len(factors), 2)

        # Public exponent should be 65537
        self.assertEqual(e, 65537)

    def test_key_mathematical_properties(self):
        """Test mathematical properties of generated keys."""
        public_key, private_key = generate_keys()
        n, e = public_key
        _, d = private_key

        # Test if n is product of two primes from our list
        factors = [p for p in PRIME_NUMBERS if n % p == 0]
        self.assertEqual(len(factors), 2)
        p, q = factors
        self.assertEqual(n, p * q)

        # Test if e and totient are coprime
        totient = (p - 1) * (q - 1)
        self.assertEqual(gcd(e, totient), 1)

        # Test if d is the multiplicative inverse of e mod totient
        self.assertEqual((d * e) % totient, 1)


if __name__ == "__main__":
    unittest.main()
