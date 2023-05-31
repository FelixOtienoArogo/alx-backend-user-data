#!/usr/bin/env python3
"""Auth."""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User


class SessionAuth(Auth):
    """Manage the API authentication by Session Authentication."""
