#!/usr/bin/env python3
"""User module."""
from models.base import Base
from typing import TypeVar, List, Iterable
from os import path
import json
import uuid


class UserSession(Base):
    """User session."""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialise the class."""
        super().__init__(*args, **kwargs)
        self.user_id: str = kwargs.get('user_id')
        self.session_id: str = kwargs.get('session_id')
