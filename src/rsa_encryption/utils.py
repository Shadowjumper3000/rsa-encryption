"""
Utility functions for RSA encryption system.
"""

import math
from typing import List, Tuple


def calculate_block_size(modulus: int, _alphabet_length: int) -> int:
    """
    Calculate the maximum safe block size for the given modulus.
    Uses log-based approach for accurate calculation.

    Args:
        modulus (int): The RSA modulus (n)
        _alphabet_length (int): Length of the alphabet being used

    Returns:
        int: Maximum safe block size in digits
    """
    # Calculate maximum digits that can safely fit in modulus
    max_digits = int(math.log10(modulus)) + 1

    # Ensure even number for proper character pairing
    if max_digits % 2 == 1:
        max_digits -= 1

    # Minimum block size is 2 (one character = 2 digits)
    return max(2, max_digits)


def split_into_chunks(text: str, chunk_size: int) -> List[str]:
    """
    Split a string into chunks of specified size.

    Args:
        text (str): String to split
        chunk_size (int): Size of each chunk

    Returns:
        List[str]: List of string chunks
    """
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


def create_char_mappings(alphabet: str) -> Tuple[dict, dict]:
    """
    Create character-to-number and number-to-character mappings.

    Args:
        alphabet (str): The alphabet to use for encoding

    Returns:
        tuple: (char_to_num_map, num_to_char_map)
    """
    char_to_num_map = {char: str(i).zfill(2) for i, char in enumerate(alphabet)}
    num_to_char_map = {str(i).zfill(2): char for i, char in enumerate(alphabet)}
    return char_to_num_map, num_to_char_map


def gcd(a: int, b: int) -> int:
    """
    Return the greatest common divisor of ``a`` and ``b`` using the Euclidean algorithm.

    This function is used by RSA key generation and is a general-purpose
    utility suitable for placement in this module.
    """
    while b:
        a, b = b, a % b
    return a
