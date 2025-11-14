"""
Permission Manager - Gestor de Permisos

Este módulo implementa el sistema de permisos y control de acceso,
definiendo qué usuarios pueden realizar qué acciones en el sistema
FIREGUARD AI.
"""

import logging
from typing import Dict, List, Set, Any, Optional
from enum import Enum


class Permission(Enum):
    """Permisos disponibles en el sistema."""
    READ = "read"
    WRITE = "write"
    SCAN = "scan"
    QUARANTINE = "quarantine"
    DELETE = "delete"
    ADMIN = "admin"


class PermissionManager:
    """
    Gestor de permisos y autorización.
    
    Controla qué usuarios tienen acceso a qué funcionalidades
    del sistema FIREGUARD AI.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa el gestor de permisos.
        
        Args:
            config: Configuración opcional del gestor
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        self.user_permissions: Dict[str, Set[Permission]] = {}
        self.logger.info("PermissionManager inicializado")
    
    def grant_permission(self, username: str, permission: Permission) -> bool:
        """
        Otorga un permiso a un usuario.
        
        Args:
            username: Nombre del usuario
            permission: Permiso a otorgar
            
        Returns:
            bool: True si el permiso fue otorgado
        """
        if username not in self.user_permissions:
            self.user_permissions[username] = set()
        
        self.user_permissions[username].add(permission)
        self.logger.info(f"Permiso {permission.value} otorgado a {username}")
        return True
    
    def revoke_permission(self, username: str, permission: Permission) -> bool:
        """
        Revoca un permiso de un usuario.
        
        Args:
            username: Nombre del usuario
            permission: Permiso a revocar
            
        Returns:
            bool: True si el permiso fue revocado
        """
        if username in self.user_permissions:
            self.user_permissions[username].discard(permission)
            self.logger.info(f"Permiso {permission.value} revocado a {username}")
            return True
        return False
    
    def has_permission(self, username: str, permission: Permission) -> bool:
        """
        Verifica si un usuario tiene un permiso específico.
        
        Args:
            username: Nombre del usuario
            permission: Permiso a verificar
            
        Returns:
            bool: True si el usuario tiene el permiso
        """
        if username not in self.user_permissions:
            return False
        return permission in self.user_permissions[username]
    
    def get_user_permissions(self, username: str) -> List[str]:
        """
        Obtiene todos los permisos de un usuario.
        
        Args:
            username: Nombre del usuario
            
        Returns:
            Lista de permisos del usuario
        """
        if username not in self.user_permissions:
            return []
        return [p.value for p in self.user_permissions[username]]
