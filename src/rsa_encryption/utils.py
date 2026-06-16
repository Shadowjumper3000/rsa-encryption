"""Utility functions for the RSA encryption system."""

from typing import Dict, List, Tuple

from .exceptions import ValidationError


def validate_alphabet(alphabet: str) -> None:
    """Validate alphabet constraints used by encoder/decoder.

    Rules:
    - must be a non-empty string
    - every character must be unique
    """
    if not isinstance(alphabet, str) or not alphabet:
        raise ValidationError("Alphabet must be a non-empty string")

    if len(set(alphabet)) != len(alphabet):
        raise ValidationError("Alphabet must not contain duplicate characters")


def calculate_symbol_width(alphabet_length: int) -> int:
    """Return fixed token width needed to encode one alphabet index.

    Width is at least 2 digits for backward compatibility with existing
    alphabets and automatically grows when alphabet size is 100+.
    """
    if alphabet_length <= 0:
        raise ValidationError("Alphabet length must be positive")
    return max(2, len(str(alphabet_length)))


def calculate_block_size(modulus: int, alphabet_length: int) -> int:
    """
    Calculate the maximum safe block size for the given modulus.

    The computed size is always a multiple of the symbol token width,
    which keeps encoded character boundaries aligned.

    Args:
        modulus (int): The RSA modulus (n)
        alphabet_length (int): Length of the alphabet being used

    Returns:
        int: Maximum safe block size in digits
    """
    if modulus <= 10:
        raise ValidationError("Modulus is too small")

    symbol_width = calculate_symbol_width(alphabet_length)

    # We need block_value < modulus. Using one digit less than modulus length
    # guarantees the resulting integer is always below modulus.
    max_digits = len(str(modulus)) - 1

    # Align to full symbol boundaries.
    max_digits -= max_digits % symbol_width

    if max_digits < symbol_width:
        raise ValidationError("Modulus is too small for the selected alphabet")

    return max_digits


def split_into_chunks(text: str, chunk_size: int) -> List[str]:
    """
    Split a string into chunks of specified size.

    Args:
        text (str): String to split
        chunk_size (int): Size of each chunk

    Returns:
        List[str]: List of string chunks
    """
    if chunk_size <= 0:
        raise ValidationError("chunk_size must be greater than zero")
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


def create_char_mappings(
    alphabet: str,
) -> Tuple[Dict[str, str], Dict[str, str], str, int]:
    """
    Create character-to-number and number-to-character mappings.

    Returns a tuple of:
    - char_to_num_map
    - num_to_char_map
    - pad_token (reserved token for block padding)
    - symbol_width

    Args:
        alphabet (str): The alphabet to use for encoding

    Returns:
        tuple: (char_to_num_map, num_to_char_map)
    """
    validate_alphabet(alphabet)
    symbol_width = calculate_symbol_width(len(alphabet))

    char_to_num_map: Dict[str, str] = {
        char: str(i).zfill(symbol_width) for i, char in enumerate(alphabet)
    }
    num_to_char_map: Dict[str, str] = {
        str(i).zfill(symbol_width): char for i, char in enumerate(alphabet)
    }
    pad_token = str(len(alphabet)).zfill(symbol_width)
    return char_to_num_map, num_to_char_map, pad_token, symbol_width


def gcd(a: int, b: int) -> int:
    """
    Return the greatest common divisor of ``a`` and ``b`` using the Euclidean algorithm.

    This function is used by RSA key generation and is a general-purpose
    utility suitable for placement in this module.
    """
    while b:
        a, b = b, a % b
    return a
