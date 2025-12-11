"""
Authentication Module - Módulo de Autenticación

Este módulo maneja la autenticación y autorización del sistema,
incluyendo gestión de usuarios, permisos y control de acceso
a las funciones del antivirus.
"""

from .authenticator import Authenticator
from .permissions import PermissionManager, Permission

__all__ = ['Authenticator', 'PermissionManager', 'Permission']
