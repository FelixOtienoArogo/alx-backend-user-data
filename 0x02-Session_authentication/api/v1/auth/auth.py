#!/usr/bin/env python3
"""Auth."""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """Manage the API authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Return if path in exluded_paths."""
        valid = False
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path not in excluded_paths:
            valid = True
        if path + "/" in excluded_paths:
            valid = False

        astericks = [stars[:-1]
                     for stars in excluded_paths if stars[-1] == '*']
        for stars in astericks:
            if path.startswith(stars):
                return False
        return valid

    def authorization_header(self, request=None) -> str:
        """Return None."""
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Return None."""
        return None

    def session_cookie(self, request=None):
        """Return a cookie value from a request."""
        if request is None:
            return None
        session = getenv('SESSION_NAME')
        return request.cookies.get(session)
