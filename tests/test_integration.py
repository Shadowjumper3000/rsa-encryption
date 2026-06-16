"""
Integration tests for the RSA encryption system.
Tests cover:
- Full encryption-decryption cycles with various messages
- Different alphabet configurations
- Handling of long messages that require multiple blocks
- Consistency across multiple round trips
"""

import unittest

from rsa_encryption import generate_keys, rsa_decrypt, rsa_encrypt


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete RSA system."""

    def test_full_encryption_decryption_cycle(self):
        """Test complete encryption-decryption cycle multiple times."""
        alphabet = "abcdefghijklmnopqrstuvwxyz "
        test_messages = [
            "hello world",
            "the quick brown fox jumps over the lazy dog",
            "a",
            "z",
            "     ",  # Multiple spaces
            "abcdefghijklmnopqrstuvwxyz",  # Full alphabet
        ]

        for _ in range(3):  # Test with different key pairs
            public_key, private_key = generate_keys()
            modulus, pub_exp = public_key
            _, priv_exp = private_key

            for message in test_messages:
                with self.subTest(message=repr(message)):
                    try:
                        encrypted = rsa_encrypt(alphabet, modulus, pub_exp, message)
                        decrypted = rsa_decrypt(alphabet, modulus, priv_exp, encrypted)
                        self.assertEqual(decrypted, message)
                    except Exception as e:
                        self.fail(f"Failed for message {repr(message)}: {e}")

    def test_different_alphabet_sizes(self):
        """Test with different alphabet configurations."""
        alphabets = [
            "abcdefghijklmnopqrstuvwxyz ",
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ",
            "abcdefghijklmnopqrstuvwxyz0123456789 ",
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ",
        ]

        messages = [
            "hello",
            "Hello",
            "hello123",
            "Hello World 123",
        ]

        public_key, private_key = generate_keys()
        modulus, pub_exp = public_key
        _, priv_exp = private_key

        for alphabet in alphabets:
            for message in messages:
                # Only test if message is valid for this alphabet
                if all(char in alphabet for char in message):
                    with self.subTest(alphabet_len=len(alphabet), message=message):
                        try:
                            encrypted = rsa_encrypt(alphabet, modulus, pub_exp, message)
                            decrypted = rsa_decrypt(
                                alphabet, modulus, priv_exp, encrypted
                            )
                            self.assertEqual(decrypted, message)
                        except Exception as e:
                            msg = (
                                f"Failed for alphabet size {len(alphabet)},"
                                f" message {repr(message)}: {e}"
                            )
                            self.fail(msg)

    def test_long_message_handling(self):
        """Test handling of long messages that require multiple blocks."""
        alphabet = "abcdefghijklmnopqrstuvwxyz "
        long_message = (
            "this is a very long message that should be split into multiple blocks"
            " during encryption and then properly reconstructed during decryption"
        )

        public_key, private_key = generate_keys()
        modulus, pub_exp = public_key
        _, priv_exp = private_key

        encrypted = rsa_encrypt(alphabet, modulus, pub_exp, long_message)
        decrypted = rsa_decrypt(alphabet, modulus, priv_exp, encrypted)

        self.assertEqual(decrypted, long_message)

    def test_round_trip_consistency(self):
        """Test that multiple round trips maintain consistency."""
        alphabet = "abcdefghijklmnopqrstuvwxyz "
        message = "consistency test"

        public_key, private_key = generate_keys()
        modulus, pub_exp = public_key
        _, priv_exp = private_key

        # Perform multiple encryption/decryption cycles
        current_message = message
        for i in range(5):
            with self.subTest(cycle=i):
                encrypted = rsa_encrypt(alphabet, modulus, pub_exp, current_message)
                decrypted = rsa_decrypt(alphabet, modulus, priv_exp, encrypted)
                self.assertEqual(decrypted, message)  # Should always equal original
                current_message = decrypted


if __name__ == "__main__":
    unittest.main()
