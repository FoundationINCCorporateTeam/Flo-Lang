"""
JSON module for Flo
Provides JSON parsing and serialization
"""

import json as _json


def parse(text: str):
    """Parse JSON string to object"""
    return _json.loads(text)


def stringify(obj, indent=None):
    """Convert object to JSON string"""
    return _json.dumps(obj, indent=indent)


def encode(obj):
    """Alias for stringify"""
    return stringify(obj)


def decode(text: str):
    """Alias for parse"""
    return parse(text)
