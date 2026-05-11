"""RSA Encryption helpers and public `rsa_encrypt`.

Refactored into small, testable functions: validation, mapping to numeric,
chunking, padding, numeric encryption, and formatting.
"""

from typing import List, Dict

from .exceptions import ValidationError

from .utils import (
    calculate_block_size,
    create_char_mappings,
    split_into_chunks,
    validate_alphabet,
)


def _validate_message(message: str) -> None:
    """Raise ValueError when the message is empty."""
    if not isinstance(message, str) or len(message) == 0:
        raise ValidationError("Error: Empty message!")


def _map_message_to_numeric(message: str, char_to_num_map: Dict[str, str]) -> str:
    """Map characters in `message` to their zero-padded numeric pairs.

    Raises ValueError for characters not in the alphabet.
    """
    out: List[str] = []
    for char in message:
        if char not in char_to_num_map:
            raise ValidationError(f"Error: Character '{char}' not in the alphabet!")
        out.append(char_to_num_map[char])
    return "".join(out)


def _pad_block(block: str, block_size: int, pad_pair: str) -> str:
    """Pad a numeric block with `pad_pair` until it reaches `block_size`."""
    while len(block) < block_size:
        block += pad_pair
    return block


def _encrypt_block_value(block_value: int, public_exponent: int, modulus: int) -> int:
    """Apply RSA modular exponentiation to a block value."""
    return pow(block_value, public_exponent, modulus)


def _format_encrypted_block(encrypted_value: int, modulus: int) -> str:
    """Return encrypted block as zero-padded decimal string consistent with modulus."""
    return str(encrypted_value).zfill(len(str(modulus)))


def rsa_encrypt(alphabet: str, modulus: int, public_exponent: int, message: str) -> str:
    """
    Encrypt a message using RSA and a custom alphabet.

    Args:
        alphabet (str): The alphabet string to use for encoding.
        modulus (int): RSA modulus (n).
        public_exponent (int): RSA public exponent (e).
        message (str): The plaintext message to encrypt.

    Returns:
        str: The encrypted message as a numeric string.

    Example:
        >>> encrypted = rsa_encrypt("abc ", n, e, "cab")
    """
    _validate_message(message)
    validate_alphabet(alphabet)

    char_to_num_map, _, pad_token, _ = create_char_mappings(alphabet)

    numeric_message = _map_message_to_numeric(message, char_to_num_map)

    block_size = calculate_block_size(modulus, len(alphabet))
    blocks = split_into_chunks(numeric_message, block_size)

    encrypted_blocks: List[str] = []

    for block in blocks:
        block = _pad_block(block, block_size, pad_token)
        block_value = int(block)
        if block_value >= modulus:
            raise ValidationError("Error: Block value exceeds modulus!")

        encrypted_value = _encrypt_block_value(block_value, public_exponent, modulus)
        encrypted_blocks.append(_format_encrypted_block(encrypted_value, modulus))

    return "".join(encrypted_blocks)
