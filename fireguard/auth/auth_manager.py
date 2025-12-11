"""
Authentication Manager - Gestor central de autenticación
"""

import secrets
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from fireguard.core.logger import Logger
from fireguard.core.config_manager import ConfigManager
from fireguard.auth.local_auth import LocalAuth
from fireguard.auth.github_auth import GitHubAuth
from fireguard.auth.google_auth import GoogleAuth


class AuthManager:
    """
    Gestor central de autenticación que coordina múltiples métodos.
    
    Soporta autenticación local, GitHub OAuth y Google OAuth.
    Maneja sesiones y tokens de acceso.
    """
    
    def __init__(self, config: Optional[ConfigManager] = None):
        """
        Inicializa el gestor de autenticación.
        
        Args:
            config: Gestor de configuración
        """
        self.logger = Logger()
        self.config = config or ConfigManager()
        
        # Inicializar proveedores de autenticación
        self.local_auth = LocalAuth()
        
        # GitHub Auth (requiere configuración)
        github_client_id = self.config.get("auth.github.client_id")
        github_client_secret = self.config.get("auth.github.client_secret")
        self.github_auth = GitHubAuth(github_client_id, github_client_secret)
        
        # Google Auth (requiere configuración)
        google_client_id = self.config.get("auth.google.client_id")
        google_client_secret = self.config.get("auth.google.client_secret")
        self.google_auth = GoogleAuth(google_client_id, google_client_secret)
        
        # Almacenamiento de sesiones (en memoria por ahora)
        self.sessions: Dict[str, Dict[str, Any]] = {}
        
        self.logger.info("AuthManager inicializado", module="AuthManager")
    
    def authenticate_local(self, username: str, password: str) -> Optional[str]:
        """
        Autentica con credenciales locales.
        
        Args:
            username: Nombre de usuario
            password: Contraseña
            
        Returns:
            Token de sesión o None si falla
        """
        if self.local_auth.authenticate(username, password):
            return self._create_session({
                "username": username,
                "provider": "local",
                "role": self.local_auth.get_user_role(username)
            })
        return None
    
    def authenticate_github(self, code: str, redirect_uri: str) -> Optional[str]:
        """
        Autentica con GitHub OAuth.
        
        Args:
            code: Código de autorización
            redirect_uri: URI de redirección
            
        Returns:
            Token de sesión o None si falla
        """
        user_info = self.github_auth.authenticate(code, redirect_uri)
        
        if user_info:
            return self._create_session(user_info)
        return None
    
    def authenticate_google(self, code: str, redirect_uri: str) -> Optional[str]:
        """
        Autentica con Google OAuth.
        
        Args:
            code: Código de autorización
            redirect_uri: URI de redirección
            
        Returns:
            Token de sesión o None si falla
        """
        user_info = self.google_auth.authenticate(code, redirect_uri)
        
        if user_info:
            return self._create_session(user_info)
        return None
    
    def _create_session(self, user_info: Dict[str, Any]) -> str:
        """
        Crea una nueva sesión de usuario.
        
        Args:
            user_info: Información del usuario autenticado
            
        Returns:
            Token de sesión
        """
        token = secrets.token_urlsafe(32)
        timeout = self.config.get("security.session_timeout", 3600)
        
        self.sessions[token] = {
            "user_info": user_info,
            "created": datetime.now(),
            "expires": datetime.now() + timedelta(seconds=timeout)
        }
        
        self.logger.info(
            f"Sesión creada para usuario: {user_info.get('username')}",
            module="AuthManager"
        )
        
        return token
    
    def validate_session(self, token: str) -> bool:
        """
        Valida un token de sesión.
        
        Args:
            token: Token de sesión a validar
            
        Returns:
            bool: True si la sesión es válida
        """
        if token not in self.sessions:
            return False
        
        session = self.sessions[token]
        
        # Verificar expiración
        if datetime.now() > session["expires"]:
            self.logger.info("Sesión expirada", module="AuthManager")
            del self.sessions[token]
            return False
        
        return True
    
    def get_session_user(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene información del usuario de una sesión.
        
        Args:
            token: Token de sesión
            
        Returns:
            Información del usuario o None si la sesión no es válida
        """
        if self.validate_session(token):
            return self.sessions[token]["user_info"]
        return None
    
    def logout(self, token: str) -> bool:
        """
        Cierra una sesión.
        
        Args:
            token: Token de sesión a cerrar
            
        Returns:
            bool: True si se cerró la sesión
        """
        if token in self.sessions:
            username = self.sessions[token]["user_info"].get("username")
            del self.sessions[token]
            self.logger.info(f"Sesión cerrada para usuario: {username}", module="AuthManager")
            return True
        return False
    
    def cleanup_expired_sessions(self):
        """Limpia sesiones expiradas"""
        now = datetime.now()
        expired_tokens = [
            token for token, session in self.sessions.items()
            if now > session["expires"]
        ]
        
        for token in expired_tokens:
            del self.sessions[token]
        
        if expired_tokens:
            self.logger.info(
                f"Limpiadas {len(expired_tokens)} sesiones expiradas",
                module="AuthManager"
            )
    
    def get_active_sessions_count(self) -> int:
        """
        Obtiene el número de sesiones activas.
        
        Returns:
            Número de sesiones activas
        """
        self.cleanup_expired_sessions()
        return len(self.sessions)
