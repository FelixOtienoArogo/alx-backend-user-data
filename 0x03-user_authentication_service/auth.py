#!/usr/bin/env python3
"""_hash_password."""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> str:
    """Take in a password string arguments and returns bytes."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Return a string representation of a new UUID."""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initialize the class."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Return a User object."""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)

            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """Check password if valid."""
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode(), user.hashed_password):
                return True
            return False
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """Return the session ID as a string."""
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None

        session_id = _generate_uuid()

        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """Return the user from session id."""
        try:
            user = self._db.find_user_by(session_id=session_id)
        except Exception:
            return None
        return user
