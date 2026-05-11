# API Reference

## generate_keys

Signature:

```python
generate_keys(use_crypto=False, bits=16, prefer="auto", prime_provider=None)
```

Description:

- Generates an RSA key pair and returns `((n, e), (n, d))`.
- Default mode (`use_crypto=False`) uses the packaged static prime list for educational reproducibility.
- Internal probabilistic prime generation is available with `use_crypto=True` and larger `bits`.
- `prime_provider` enables dependency injection for custom strategies.

Validation:

- Raises `ValueError` when `bits < 2`.
- Raises `ValueError` when `prefer` is not one of `auto`, `internal`, `static`.

Notes:

- This library is educational and does not provide modern production-grade cryptographic safeguards.

## rsa_encrypt

Signature:

```python
rsa_encrypt(alphabet, modulus, public_exponent, message)
```

Description:

- Encrypts plaintext to a digit-only ciphertext string.
- Uses fixed-width symbol tokens derived from alphabet size.
- Splits encoded message into safe RSA blocks and zero-pads encrypted blocks.

Validation:

- Raises `ValueError` for empty or non-string message.
- Raises `ValueError` for invalid alphabet (empty or duplicate characters).
- Raises `ValueError` when message contains a character not present in alphabet.
- Raises `ValueError` when modulus is too small for selected alphabet.

## rsa_decrypt

Signature:

```python
rsa_decrypt(alphabet, modulus, private_exponent, encrypted_message)
```

Description:

- Decrypts digit-only ciphertext string to plaintext.
- Enforces strict ciphertext structure and strict padding behavior.

Validation:

- Raises `ValueError` when ciphertext is empty or non-numeric.
- Raises `ValueError` when ciphertext length is not a multiple of encrypted block size.
- Raises `ValueError` for invalid alphabet (empty or duplicate characters).
- Raises `ValueError` when decrypted token stream contains unknown tokens.
- Raises `ValueError` when non-padding data appears after padding tokens.

## Constants

- `ALPHABETS`: packaged convenience alphabet presets.
- `PRIME_NUMBERS`: packaged prime list used in default key generation mode.
