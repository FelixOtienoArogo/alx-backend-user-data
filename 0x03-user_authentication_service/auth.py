#!/usr/bin/env python3
"""_hash_password."""
import bcrypt


def _hash_password(password: str) -> str:
    """Take in a password string arguments and returns bytes."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())