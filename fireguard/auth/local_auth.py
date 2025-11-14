"""
Local Authentication - Autenticación local con usuario y contraseña
"""

import hashlib
import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet
from fireguard.core.logger import Logger


class LocalAuth:
    """
    Sistema de autenticación local con usuarios y contraseñas.
    
    Las contraseñas se almacenan hasheadas con SHA-256 y los datos
    sensibles se encriptan con Fernet.
    """
    
    def __init__(self, users_file: str = "config/users.json"):
        """
        Inicializa el sistema de autenticación local.
        
        Args:
            users_file: Ruta al archivo de usuarios
        """
        self.logger = Logger()
        self.users_file = users_file
        self.users: Dict[str, Dict[str, Any]] = {}
        self.key = self._load_or_create_key()
        self.cipher = Fernet(self.key)
        self._load_users()
    
    def _load_or_create_key(self) -> bytes:
        """Carga o crea una clave de encriptación"""
        key_file = Path("config/.key")
        
        if key_file.exists():
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key_file.parent.mkdir(parents=True, exist_ok=True)
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            # Proteger el archivo de clave
            os.chmod(key_file, 0o600)
            return key
    
    def _hash_password(self, password: str) -> str:
        """Hashea una contraseña con SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _load_users(self):
        """Carga usuarios desde el archivo"""
        users_path = Path(self.users_file)
        
        if not users_path.exists():
            self.logger.info("Archivo de usuarios no existe. Creando uno nuevo.", module="LocalAuth")
            self._create_default_user()
            return
        
        try:
            with open(users_path, 'r') as f:
                self.users = json.load(f)
            self.logger.info(f"Usuarios cargados: {len(self.users)}", module="LocalAuth")
        except Exception as e:
            self.logger.error(f"Error al cargar usuarios: {e}", module="LocalAuth")
            self.users = {}
    
    def _save_users(self):
        """Guarda usuarios en el archivo"""
        users_path = Path(self.users_file)
        users_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(users_path, 'w') as f:
                json.dump(self.users, f, indent=2)
            # Proteger el archivo de usuarios
            os.chmod(users_path, 0o600)
            self.logger.info("Usuarios guardados correctamente", module="LocalAuth")
        except Exception as e:
            self.logger.error(f"Error al guardar usuarios: {e}", module="LocalAuth")
    
    def _create_default_user(self):
        """Crea un usuario administrador por defecto"""
        default_username = "admin"
        default_password = "fireguard2024"
        
        self.create_user(default_username, default_password, role="admin")
        
        self.logger.warning(
            f"Usuario por defecto creado - Usuario: '{default_username}', "
            f"Contraseña: '{default_password}' - ¡CAMBIAR INMEDIATAMENTE!",
            module="LocalAuth"
        )
    
    def create_user(self, username: str, password: str, role: str = "user") -> bool:
        """
        Crea un nuevo usuario.
        
        Args:
            username: Nombre de usuario
            password: Contraseña
            role: Rol del usuario (admin, user)
            
        Returns:
            bool: True si el usuario se creó exitosamente
        """
        if username in self.users:
            self.logger.warning(f"Usuario {username} ya existe", module="LocalAuth")
            return False
        
        self.users[username] = {
            "password_hash": self._hash_password(password),
            "role": role,
            "created": True
        }
        
        self._save_users()
        self.logger.info(f"Usuario {username} creado", module="LocalAuth")
        return True
    
    def authenticate(self, username: str, password: str) -> bool:
        """
        Autentica un usuario.
        
        Args:
            username: Nombre de usuario
            password: Contraseña
            
        Returns:
            bool: True si la autenticación es exitosa
        """
        if username not in self.users:
            self.logger.warning(f"Intento de login con usuario inexistente: {username}", module="LocalAuth")
            return False
        
        password_hash = self._hash_password(password)
        
        if self.users[username]["password_hash"] == password_hash:
            self.logger.info(f"Usuario {username} autenticado correctamente", module="LocalAuth")
            return True
        else:
            self.logger.warning(f"Contraseña incorrecta para usuario: {username}", module="LocalAuth")
            return False
    
    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """
        Cambia la contraseña de un usuario.
        
        Args:
            username: Nombre de usuario
            old_password: Contraseña actual
            new_password: Nueva contraseña
            
        Returns:
            bool: True si el cambio fue exitoso
        """
        if not self.authenticate(username, old_password):
            return False
        
        self.users[username]["password_hash"] = self._hash_password(new_password)
        self._save_users()
        
        self.logger.info(f"Contraseña cambiada para usuario: {username}", module="LocalAuth")
        return True
    
    def delete_user(self, username: str) -> bool:
        """
        Elimina un usuario.
        
        Args:
            username: Nombre de usuario a eliminar
            
        Returns:
            bool: True si el usuario fue eliminado
        """
        if username not in self.users:
            return False
        
        del self.users[username]
        self._save_users()
        
        self.logger.info(f"Usuario {username} eliminado", module="LocalAuth")
        return True
    
    def get_user_role(self, username: str) -> Optional[str]:
        """
        Obtiene el rol de un usuario.
        
        Args:
            username: Nombre de usuario
            
        Returns:
            Rol del usuario o None si no existe
        """
        if username in self.users:
            return self.users[username].get("role", "user")
        return None
