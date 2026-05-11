"""Library API and extensibility tests."""

import unittest

import rsa_encryption
from rsa_encryption.key_generation import generate_keys


class SequencePrimeProvider:
    """Deterministic provider for testing provider injection."""

    def __init__(self, values):
        self._values = list(values)
        self._index = 0

    def generate_prime(self, _bits):
        value = self._values[self._index]
        self._index += 1
        return value


class TestLibraryApi(unittest.TestCase):
    """Tests for package-level API behavior."""

    def test_public_exports(self):
        expected_exports = {
            "ALPHABETS",
            "PRIME_NUMBERS",
            "generate_keys",
            "gcd",
            "rsa_encrypt",
            "rsa_decrypt",
        }
        self.assertTrue(expected_exports.issubset(set(rsa_encryption.__all__)))

    def test_version_present(self):
        self.assertIsInstance(rsa_encryption.__version__, str)
        self.assertTrue(len(rsa_encryption.__version__) > 0)

    def test_generate_keys_with_custom_provider(self):
        provider = SequencePrimeProvider([101, 103])
        public_key, private_key = generate_keys(
            use_crypto=True,
            bits=8,
            prime_provider=provider,
        )

        n, e = public_key
        _, d = private_key
        totient = (101 - 1) * (103 - 1)

        self.assertEqual(n, 101 * 103)
        self.assertEqual(e, 65537)
        self.assertEqual((d * e) % totient, 1)

    def test_generate_keys_rejects_invalid_bits(self):
        with self.assertRaises(ValueError):
            generate_keys(bits=1)

    def test_generate_keys_rejects_invalid_prefer(self):
        with self.assertRaises(ValueError):
            generate_keys(use_crypto=True, prefer="invalid")

    def test_generate_keys_internal_provider(self):
        public_key, private_key = generate_keys(
            use_crypto=True,
            bits=16,
            prefer="internal",
        )
        self.assertEqual(public_key[0], private_key[0])
        self.assertEqual(public_key[1], 65537)

    def test_generate_keys_auto_provider(self):
        public_key, private_key = generate_keys(use_crypto=True, bits=16, prefer="auto")
        self.assertEqual(public_key[0], private_key[0])
        self.assertEqual(public_key[1], 65537)


if __name__ == "__main__":
    unittest.main()
