"""
Unit tests for RSA encryption functionality.
Tests cover:
- Basic message encryption
- Encryption with extended alphabet
- Handling of spaces and edge cases
- Invalid input scenarios
"""

import unittest

from rsa_encryption.encryption import rsa_encrypt
from rsa_encryption.key_generation import generate_keys


class TestEncryption(unittest.TestCase):
    """Test cases for RSA encryption."""

    def setUp(self):
        """Set up test fixtures."""
        self.alphabet = "abcdefghijklmnopqrstuvwxyz "
        self.public_key, self.private_key = generate_keys()
        self.modulus, self.pub_exp = self.public_key

    def test_encrypt_basic_message(self):
        """Test encryption of basic messages."""
        test_cases = ["hello", "world", "test message", "a", "z"]

        for message in test_cases:
            with self.subTest(message=message):
                encrypted = rsa_encrypt(
                    self.alphabet, self.modulus, self.pub_exp, message
                )
                self.assertIsNotNone(encrypted)
                self.assertNotEqual(encrypted, message)
                self.assertTrue(encrypted.isdigit())

    def test_encrypt_empty_message(self):
        """Test that empty message raises ValueError."""
        with self.assertRaises(ValueError):
            rsa_encrypt(self.alphabet, self.modulus, self.pub_exp, "")

    def test_encrypt_invalid_characters(self):
        """Test that invalid characters raise ValueError."""
        invalid_messages = ["hello!", "test@message", "número"]

        for message in invalid_messages:
            with self.subTest(message=message):
                with self.assertRaises(ValueError):
                    rsa_encrypt(self.alphabet, self.modulus, self.pub_exp, message)

    def test_encrypt_extended_alphabet(self):
        """Test encryption with extended alphabet."""
        extended_alphabet = (
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
        )
        message = "Hello World 123"

        encrypted = rsa_encrypt(extended_alphabet, self.modulus, self.pub_exp, message)
        self.assertIsNotNone(encrypted)
        self.assertTrue(encrypted.isdigit())

    def test_encrypt_spaces_and_special_cases(self):
        """Test encryption with spaces and edge cases."""
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
                self.assertIsNotNone(encrypted)
                self.assertTrue(encrypted.isdigit())


if __name__ == "__main__":
    unittest.main()
