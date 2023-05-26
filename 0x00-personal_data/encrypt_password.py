#!/usr/bin/env python3
"""Encrypting passwords."""
import bcrypt


def hash_password(password: str) -> bytes:
    """Return a hashed password."""
    encoded = password.encode()
    return bcrypt.hashpw(encoded, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validate that the provided password matches the hashed password."""
    encoded = password.encode()
    if bcrypt.checkpw(encoded, hashed_password):
        return True
    return False
