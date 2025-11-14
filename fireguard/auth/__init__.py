"""
Authentication module initialization
"""

from fireguard.auth.auth_manager import AuthManager
from fireguard.auth.local_auth import LocalAuth
from fireguard.auth.github_auth import GitHubAuth
from fireguard.auth.google_auth import GoogleAuth

__all__ = [
    "AuthManager",
    "LocalAuth",
    "GitHubAuth",
    "GoogleAuth",
]
