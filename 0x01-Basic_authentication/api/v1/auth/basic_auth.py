#!/usr/bin/env python3
"""Auth."""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Manage the API authentication by Basic Authentication."""
