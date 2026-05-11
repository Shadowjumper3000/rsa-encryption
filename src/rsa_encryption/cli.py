#!/usr/bin/env python3
"""
CLI entrypoint for the rsa_encryption package.

Loads alphabets from packaged Python module constants and exposes
generate-keys, encrypt, decrypt, and alphabet-info commands.
"""

import argparse
import sys
import json
import os
import tempfile
from . import generate_keys, rsa_encrypt, rsa_decrypt
from .libraries import ALPHABETS
from .exceptions import ValidationError


def get_alphabet(name_or_string):
    """Return the alphabet string for a given name or custom string."""
    if name_or_string in ALPHABETS:
        return ALPHABETS[name_or_string]
    return name_or_string


def generate_keys_command(args):
    """
    Generate RSA key pair and optionally save to a file.

    :param args: Command-line arguments
    :return: None
    """
    public_key, private_key = generate_keys()

    keys_data = {
        "public_key": {"n": public_key[0], "e": public_key[1]},
        "private_key": {"n": private_key[0], "d": private_key[1]},
    }

    if args.output:
        # Atomic write: write to temp file then replace to avoid partial writes
        dirpath = os.path.dirname(os.path.abspath(args.output)) or "."
        with tempfile.NamedTemporaryFile("w", delete=False, dir=dirpath, encoding="utf-8") as tmp:
            json.dump(keys_data, tmp, indent=2)
            tmp_name = tmp.name
        os.replace(tmp_name, args.output)
        print(f"Keys saved to {args.output}")
    else:
        print("Generated RSA Key Pair:")
        print(f"Public Key (n, e): ({public_key[0]}, {public_key[1]})")
        print(f"Private Key (n, d): ({private_key[0]}, {private_key[1]})")
        print("\nJSON Format:")
        print(json.dumps(keys_data, indent=2))


def encrypt_command(args):
    """
    Encrypt a message using RSA encryption with the provided public key and alphabet.

    :param args: Command-line arguments
    :return: None
    """
    alphabet = get_alphabet(args.alphabet)

    if args.key_file:
        with open(args.key_file, "r", encoding="utf-8") as f:
            keys_data = json.load(f)
        n = keys_data["public_key"]["n"]
        e = keys_data["public_key"]["e"]
    else:
        n = args.n
        e = args.e

    if n is None or e is None:
        print(
            "Error: Public key (n, e) must be provided either via --key-file or --n and --e"
        )
        sys.exit(1)

    if args.stdin and not args.message:
        message = sys.stdin.read()
    else:
        message = args.message or input("Enter message to encrypt: ")

    try:
        encrypted = rsa_encrypt(alphabet, n, e, message)
        print(f"Encrypted message: {encrypted}")

        if args.output:
            dirpath = os.path.dirname(os.path.abspath(args.output)) or "."
            with tempfile.NamedTemporaryFile("w", delete=False, dir=dirpath, encoding="utf-8") as tmp:
                tmp.write(encrypted)
                tmp_name = tmp.name
            os.replace(tmp_name, args.output)
            print(f"Encrypted message saved to {args.output}")

    except ValidationError as error:
        print(f"Encryption error: {error}")
        sys.exit(1)


def decrypt_command(args):
    """
    Decrypt a message using RSA decryption with the provided private key and alphabet.

    :param args: Command-line arguments
    :return: None
    """
    alphabet = get_alphabet(args.alphabet)

    if args.key_file:
        with open(args.key_file, "r", encoding="utf-8") as f:
            keys_data = json.load(f)
        n = keys_data["private_key"]["n"]
        d = keys_data["private_key"]["d"]
    else:
        n = args.n
        d = args.d

    if n is None or d is None:
        print(
            "Error: Private key (n, d) must be provided either via --key-file or --n and --d"
        )
        sys.exit(1)

    if args.message:
        encrypted_message = args.message
    elif args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            encrypted_message = f.read().strip()
    elif args.stdin:
        encrypted_message = sys.stdin.read().strip()
    else:
        encrypted_message = input("Enter encrypted message: ")

    try:
        decrypted = rsa_decrypt(alphabet, n, d, encrypted_message)
        print(f"Decrypted message: {decrypted}")

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(decrypted)
            print(f"Decrypted message saved to {args.output}")

    except ValidationError as error:
        print(f"Decryption error: {error}")
        sys.exit(1)


def alphabet_info_command(_args):
    """
    Display available alphabet types and their characters.

    :param args: Command-line arguments
    :return: None
    """
    alphabets = ALPHABETS

    print("Available alphabet types:")
    for name, alphabet in alphabets.items():
        print(f"  {name:10} ({len(alphabet):2} chars): {alphabet}")

    print("\nYou can also specify a custom alphabet as a string.")


def main():
    """
    Main entry point for the RSA Encryption CLI tool.
    """
    parser = argparse.ArgumentParser(
        description="RSA Encryption CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    gen_parser = subparsers.add_parser("generate-keys", help="Generate RSA key pair")
    gen_parser.add_argument("--output", "-o", help="Output file for keys (JSON format)")

    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt a message")
    encrypt_parser.add_argument("--message", "-m", help="Message to encrypt")
    encrypt_parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read message from standard input when no message is provided",
    )
    encrypt_parser.add_argument(
        "--alphabet",
        "-a",
        default="basic",
        help="Alphabet type: basic, extended, full, numeric, or custom string",
    )
    encrypt_parser.add_argument("--key-file", "-k", help="JSON file containing keys")
    encrypt_parser.add_argument(
        "--n", type=int, help="Public key modulus (if not using key file)"
    )
    encrypt_parser.add_argument(
        "--e", type=int, help="Public key exponent (if not using key file)"
    )
    encrypt_parser.add_argument(
        "--output", "-o", help="Output file for encrypted message"
    )

    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt a message")
    decrypt_parser.add_argument("--message", "-m", help="Encrypted message to decrypt")
    decrypt_parser.add_argument(
        "--input", "-i", help="Input file containing encrypted message"
    )
    decrypt_parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read encrypted message from standard input when no message or input file is provided",
    )
    decrypt_parser.add_argument(
        "--alphabet",
        "-a",
        default="basic",
        help="Alphabet type: basic, extended, full, numeric, or custom string",
    )
    decrypt_parser.add_argument("--key-file", "-k", help="JSON file containing keys")
    decrypt_parser.add_argument(
        "--n", type=int, help="Private key modulus (if not using key file)"
    )
    decrypt_parser.add_argument(
        "--d", type=int, help="Private key exponent (if not using key file)"
    )
    decrypt_parser.add_argument(
        "--output", "-o", help="Output file for decrypted message"
    )

    subparsers.add_parser("alphabet-info", help="Show available alphabet types")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "generate-keys":
        generate_keys_command(args)
    elif args.command == "encrypt":
        encrypt_command(args)
    elif args.command == "decrypt":
        decrypt_command(args)
    elif args.command == "alphabet-info":
        alphabet_info_command(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
