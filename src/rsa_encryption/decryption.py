"""RSA Decryption helpers and public `rsa_decrypt`.

This module splits the decryption logic into small functions with single
responsibilities: validation, size calculation, block splitting, numeric
decryption, formatting, and mapping digits back to characters.
"""

from typing import List, Dict, Tuple

from .exceptions import ValidationError

from .utils import (
    calculate_block_size,
    create_char_mappings,
    split_into_chunks,
    validate_alphabet,
)


def _validate_encrypted_message(
    encrypted_message: str,
    encrypted_block_size: int,
) -> None:
    """Raise ValueError for invalid encrypted input."""
    if not encrypted_message or not encrypted_message.isdigit():
        raise ValidationError("Invalid encrypted message")
    if len(encrypted_message) % encrypted_block_size != 0:
        raise ValidationError("Invalid encrypted message length")


def _calculate_sizes(modulus: int, alphabet_len: int) -> Tuple[int, int]:
    """Return (block_size, encrypted_block_size)."""
    block_size = calculate_block_size(modulus, alphabet_len)
    encrypted_block_size = len(str(modulus))
    return block_size, encrypted_block_size


def _split_encrypted_blocks(
    encrypted_message: str, encrypted_block_size: int
) -> List[str]:
    """Split the full encrypted string into fixed-size numeric blocks."""
    return split_into_chunks(encrypted_message, encrypted_block_size)


def _decrypt_block_value(block_value: int, private_exponent: int, modulus: int) -> int:
    """Perform numeric RSA modular exponentiation for one block."""
    return pow(block_value, private_exponent, modulus)


def _format_decrypted_block(block_value: int, block_size: int) -> str:
    """Return the decrypted block as a zero-padded decimal string."""
    return str(block_value).zfill(block_size)


def _block_to_chars(
    decrypted_block: str,
    num_to_char_map: Dict[str, str],
    pad_token: str,
    symbol_width: int,
) -> str:
    """Convert a decrypted numeric block (decimal string) into characters.

    Padding tokens are allowed only at the tail of the block. Unknown tokens
    and non-tail padding are treated as corruption and raise ValueError.
    """
    out: List[str] = []
    tokens = split_into_chunks(decrypted_block, symbol_width)
    if any(len(token) != symbol_width for token in tokens):
        raise ValidationError("Invalid decrypted block width")

    seen_padding = False
    for token in tokens:
        if token == pad_token:
            seen_padding = True
            continue

        if seen_padding:
            raise ValidationError("Invalid padding sequence")

        if token not in num_to_char_map:
            raise ValidationError("Invalid token in decrypted block")

        out.append(num_to_char_map[token])
    return "".join(out)


def rsa_decrypt(
    alphabet: str, modulus: int, private_exponent: int, encrypted_message: str
) -> str:
    """
    Decrypt an RSA-encrypted message using a custom alphabet.

    Args:
        alphabet (str): The alphabet string to use for decoding.
        modulus (int): RSA modulus (n).
        private_exponent (int): RSA private exponent (d).
        encrypted_message (str): The encrypted message as a numeric string.

    Returns:
        str: The decrypted plaintext message.

    Raises:
        ValueError: If decryption fails or input is invalid.

    Example:
        >>> decrypted = rsa_decrypt("abc ", n, d, encrypted)
    """
    validate_alphabet(alphabet)
    _, num_to_char_map, pad_token, symbol_width = create_char_mappings(alphabet)

    block_size, encrypted_block_size = _calculate_sizes(modulus, len(alphabet))

    _validate_encrypted_message(encrypted_message, encrypted_block_size)

    try:
        encrypted_blocks = _split_encrypted_blocks(
            encrypted_message, encrypted_block_size
        )

        parts: List[str] = []
        for block in encrypted_blocks:
            if not block:
                continue

            block_value = int(block)
            decrypted_value = _decrypt_block_value(
                block_value, private_exponent, modulus
            )
            decrypted_block = _format_decrypted_block(decrypted_value, block_size)
            parts.append(
                _block_to_chars(
                    decrypted_block,
                    num_to_char_map,
                    pad_token,
                    symbol_width,
                )
            )

        return "".join(parts)

    except (ValidationError, KeyError) as e:
        raise ValidationError(f"Decryption failed: {str(e)}") from e
