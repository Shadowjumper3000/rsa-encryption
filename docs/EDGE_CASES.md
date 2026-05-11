# Edge Cases and Validation Rules

## Alphabet Rules

- Alphabet must be a non-empty string.
- Alphabet characters must be unique.
- Duplicate characters are rejected to avoid ambiguous decoding.

## Message Rules

- Empty messages are rejected.
- Any character not present in selected alphabet is rejected.
- Newlines, null bytes, emojis, and punctuation are valid only when included in alphabet.

## Ciphertext Rules

- Ciphertext must be numeric.
- Ciphertext length must be divisible by encrypted block width.
- Unknown decoded tokens are treated as corruption and rejected.
- Padding tokens are valid only at tail of a decrypted block.

## Block Sizing Rules

- Plaintext block digit-length is selected so every plaintext block integer is strictly less than modulus.
- Block length is aligned to complete symbol token width.
- If modulus is too small for chosen alphabet token width, encryption/decryption raises `ValueError`.

## Long and Short Messages

- One-character and short messages are supported.
- Multi-block long messages are supported.
- Mixed-space messages are supported.

## Security Scope

- Project is educational and intentionally simple.
- OAEP and production hardening are out of scope.
