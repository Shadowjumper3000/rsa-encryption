"""Shared packaged library data: alphabets and primes.

Keeping these small lookup tables in a module makes access fast and
simple (no JSON parsing required) while still being easy to update.
"""

ALPHABETS = {
    "basic": "abcdefghijklmnopqrstuvwxyz ",
    "extended": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ",
    "full": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ",
    "numeric": "0123456789 ",
}


PRIME_NUMBERS = [
    32749,
    32771,
    32783,
    32789,
    32797,
    32801,
    32803,
    32831,
    32833,
    32839,
    32843,
    32869,
    32887,
    32909,
    32911,
    32917,
    32933,
    32939,
    32941,
    32957,
    32969,
    32971,
    32983,
    32987,
    32993,
    32999,
    33013,
    33023,
    33029,
    33037,
]
