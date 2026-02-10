"""
Unit tests for RSA decryption functionality.
Tests cover:
- Basic message decryption
- Decryption with extended alphabet
- Handling of spaces and edge cases
- Invalid input scenarios
"""

import unittest

# Imports assume package is installed in editable mode (pip install -e .)
from rsa_encryption.encryption import rsa_encrypt
from rsa_encryption.decryption import rsa_decrypt
from rsa_encryption.key_generation import generate_keys


class TestDecryption(unittest.TestCase):
    """Test cases for RSA decryption."""

    def setUp(self):
        """Set up test fixtures."""
        self.alphabet = "abcdefghijklmnopqrstuvwxyz "
        self.public_key, self.private_key = generate_keys()
        self.modulus, self.pub_exp = self.public_key
        self.modulus_priv, self.priv_exp = self.private_key

    def test_decrypt_basic_messages(self):
        """Test decryption of basic messages."""
        test_messages = ["hello", "world", "test message", "a", "z "]

        for message in test_messages:
            with self.subTest(message=message):
                encrypted = rsa_encrypt(
                    self.alphabet, self.modulus, self.pub_exp, message
                )
                decrypted = rsa_decrypt(
                    self.alphabet, self.modulus, self.priv_exp, encrypted
                )
                self.assertEqual(decrypted, message)

    def test_decrypt_invalid_input(self):
        """Test decryption with invalid encrypted input."""
        with self.assertRaises(ValueError):
            rsa_decrypt(self.alphabet, self.modulus, self.priv_exp, "invalid")

    def test_decrypt_extended_alphabet(self):
        """Test decryption with extended alphabet."""
        extended_alphabet = (
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
        )
        message = "Hello World 123"

        encrypted = rsa_encrypt(extended_alphabet, self.modulus, self.pub_exp, message)
        decrypted = rsa_decrypt(
            extended_alphabet, self.modulus, self.priv_exp, encrypted
        )
        self.assertEqual(decrypted, message)

    def test_decrypt_spaces_and_special_cases(self):
        """Test decryption with spaces and edge cases."""
        test_cases = [
            "   ",  # Only spaces
            "a ",  # Letter and space
            " a",  # Space and letter
            "z z z",  # Alternating
        ]

        for message in test_cases:
            with self.subTest(message=repr(message)):
                encrypted = rsa_encrypt(
                    self.alphabet, self.modulus, self.pub_exp, message
                )
                decrypted = rsa_decrypt(
                    self.alphabet, self.modulus, self.priv_exp, encrypted
                )
                self.assertEqual(decrypted, message)

    def test_decrypt_malformed_input(self):
        """Test decryption with malformed input."""
        test_cases = [
            "",  # Empty string
            "abc",  # Non-numeric
            "12345abc",  # Mixed
        ]

        for invalid_input in test_cases:
            with self.subTest(input=invalid_input):
                with self.assertRaises(ValueError):
                    rsa_decrypt(
                        self.alphabet, self.modulus, self.priv_exp, invalid_input
                    )


if __name__ == "__main__":
    unittest.main()
