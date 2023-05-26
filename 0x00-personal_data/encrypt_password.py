#!/usr/bin/env python3
"""Encrypting passwords."""
import bcrypt


def hash_password(password: str) -> bytes:
    """Return a hashed password."""
    encoded = password.encode()
    return bcrypt.hashpw(encoded, bcrypt.gensalt())
