#!/usr/bin/env python3
"""
Module filter_datum.

Module for handling Personal Data.
"""

from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Return the log message obfuscated."""
    for f in fields:
        out = re.sub(f'{f}=.*?{separator}',
                     f'{f}={redaction}{separator}', message)
    return message
