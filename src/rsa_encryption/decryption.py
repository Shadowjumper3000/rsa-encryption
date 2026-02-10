"""RSA Decryption helpers and public `rsa_decrypt`.

This module splits the decryption logic into small functions with single
responsibilities: validation, size calculation, block splitting, numeric
decryption, formatting, and mapping digits back to characters.
"""

from .utils import calculate_block_size, create_char_mappings, split_into_chunks


def _validate_encrypted_message(encrypted_message: str) -> None:
    """Raise ValueError for invalid encrypted input."""
    if not encrypted_message or not encrypted_message.isdigit():
        raise ValueError("Invalid encrypted message")


def _calculate_sizes(modulus: int, alphabet_len: int) -> tuple[int, int]:
    """Return (block_size, encrypted_block_size)."""
    block_size = calculate_block_size(modulus, alphabet_len)
    encrypted_block_size = len(str(modulus))
    return block_size, encrypted_block_size


def _split_encrypted_blocks(
    encrypted_message: str, encrypted_block_size: int
) -> list[str]:
    """Split the full encrypted string into fixed-size numeric blocks."""
    return split_into_chunks(encrypted_message, encrypted_block_size)


def _decrypt_block_value(block_value: int, private_exponent: int, modulus: int) -> int:
    """Perform numeric RSA modular exponentiation for one block."""
    return pow(block_value, private_exponent, modulus)


def _format_decrypted_block(block_value: int, block_size: int) -> str:
    """Return the decrypted block as a zero-padded decimal string."""
    return str(block_value).zfill(block_size)


def _block_to_chars(decrypted_block: str, num_to_char_map: dict[str, str]) -> str:
    """Convert a decrypted numeric block (decimal string) into characters.

    Pairs that are not present in `num_to_char_map` are treated as padding
    and skipped.
    """
    out: list[str] = []
    for i in range(0, len(decrypted_block), 2):
        pair = decrypted_block[i : i + 2]
        if pair in num_to_char_map:
            out.append(num_to_char_map[pair])
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
    _, num_to_char_map = create_char_mappings(alphabet)

    block_size, encrypted_block_size = _calculate_sizes(modulus, len(alphabet))

    _validate_encrypted_message(encrypted_message)

    try:
        encrypted_blocks = _split_encrypted_blocks(
            encrypted_message, encrypted_block_size
        )

        parts: list[str] = []
        for block in encrypted_blocks:
            if not block:
                continue

            block_value = int(block)
            decrypted_value = _decrypt_block_value(
                block_value, private_exponent, modulus
            )
            decrypted_block = _format_decrypted_block(decrypted_value, block_size)
            parts.append(_block_to_chars(decrypted_block, num_to_char_map))

        return "".join(parts)

    except (ValueError, KeyError) as e:
        raise ValueError(f"Decryption failed: {str(e)}") from e
