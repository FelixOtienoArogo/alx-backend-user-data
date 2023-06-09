#!/usr/bin/env python3
"""SessionExpAuth."""
from datetime import datetime, timedelta, timedelta
from api.v1.auth.session_auth import SessionAuth
from os import getenv


class SessionExpAuth(SessionAuth):
    """Add an expiration date to a Session ID."""

    def __init__(self):
        """Initialise the class."""
        try:
            session_duration = int(getenv("SESSION_DURATION"))
        except Exception:
            session_duration = 0
        self.session_duration = session_duration

    def create_session(self, user_id=None):
        """Create a Session ID."""
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        session_dictionary = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Overloading the function."""
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None
        session_dictionary = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dictionary["user_id"]
        if "created_at" not in session_dictionary.keys():
            return None
        created_at = session_dictionary["created_at"]
        session_duration = timedelta(seconds=self.session_duration)
        if (created_at + session_duration) < datetime.now():
            return None
        return session_dictionary["user_id"]
