#!/usr/bin/env python3
"""Auth."""
from flask.globals import session
from typing import List, TypeVar, Dict
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
import uuid


class SessionAuth(Auth):
    """Manage the API authentication by Session Authentication."""

    user_id_by_session_id: Dict[str, str] = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a Session ID for a user_id."""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a User ID based on a Session ID."""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None):
        """Return a User instance based on a cookie value."""
        cookie = self.session_cookie(request)
        session_user_id = self.user_id_for_session_id(cookie)
        print(session_user_id)
        user_id = User.get(session_user_id)
        return user_id

    def destroy_session(self, request=None):
        """Delete the user session / logout."""
        if request is None:
            return False

        cookie_data = self.session_cookie(request)

        if cookie_data is None:
            return False

        if not self.user_id_for_session_id(cookie_data):
            return False

        del self.user_id_by_session_id[cookie_data]
        return True
