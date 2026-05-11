"""Additional edge-case coverage for RSA encryption library."""

import unittest

from rsa_encryption import generate_keys, rsa_decrypt, rsa_encrypt


class TestEdgeCases(unittest.TestCase):
    """Edge-case tests not covered in standard flow tests."""

    def test_round_trip_large_alphabet_over_100_chars(self):
        # Build a deterministic, unique 110-character alphabet.
        large_alphabet = "".join(chr(code) for code in range(33, 143))
        message = large_alphabet[0] + large_alphabet[55] + large_alphabet[109]

        public_key, private_key = generate_keys()
        modulus, pub_exp = public_key
        _, priv_exp = private_key

        encrypted = rsa_encrypt(large_alphabet, modulus, pub_exp, message)
        decrypted = rsa_decrypt(large_alphabet, modulus, priv_exp, encrypted)

        self.assertEqual(decrypted, message)

    def test_encrypt_rejects_empty_alphabet(self):
        public_key, _ = generate_keys()
        modulus, pub_exp = public_key

        with self.assertRaises(ValueError):
            rsa_encrypt("", modulus, pub_exp, "hello")

    def test_encrypt_rejects_duplicate_alphabet_chars(self):
        public_key, _ = generate_keys()
        modulus, pub_exp = public_key

        with self.assertRaises(ValueError):
            rsa_encrypt("abcdea", modulus, pub_exp, "hello")

    def test_decrypt_rejects_duplicate_alphabet_chars(self):
        _, private_key = generate_keys()
        modulus, priv_exp = private_key

        with self.assertRaises(ValueError):
            rsa_decrypt("abcdea", modulus, priv_exp, "1234")

    def test_encrypt_rejects_too_small_modulus(self):
        with self.assertRaises(ValueError):
            rsa_encrypt("abc", 11, 3, "ab")


if __name__ == "__main__":
    unittest.main()
