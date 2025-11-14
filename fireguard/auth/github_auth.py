"""
GitHub OAuth Authentication - Autenticación con GitHub
"""

import requests
from typing import Optional, Dict, Any
from fireguard.core.logger import Logger


class GitHubAuth:
    """
    Sistema de autenticación con GitHub OAuth.
    
    Permite autenticar usuarios usando sus cuentas de GitHub.
    """
    
    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None):
        """
        Inicializa la autenticación de GitHub.
        
        Args:
            client_id: ID de la aplicación OAuth de GitHub
            client_secret: Secret de la aplicación OAuth de GitHub
        """
        self.logger = Logger()
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_url = "https://github.com/login/oauth/authorize"
        self.token_url = "https://github.com/login/oauth/access_token"
        self.api_url = "https://api.github.com"
    
    def get_authorization_url(self, redirect_uri: str, state: str) -> str:
        """
        Genera la URL de autorización para GitHub.
        
        Args:
            redirect_uri: URI de redirección después de la autenticación
            state: Estado único para prevenir CSRF
            
        Returns:
            URL de autorización
        """
        if not self.client_id:
            self.logger.error("Client ID de GitHub no configurado", module="GitHubAuth")
            return ""
        
        params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "state": state,
            "scope": "read:user user:email"
        }
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{self.auth_url}?{query_string}"
    
    def exchange_code_for_token(self, code: str, redirect_uri: str) -> Optional[str]:
        """
        Intercambia el código de autorización por un token de acceso.
        
        Args:
            code: Código de autorización de GitHub
            redirect_uri: URI de redirección
            
        Returns:
            Token de acceso o None si falla
        """
        if not self.client_id or not self.client_secret:
            self.logger.error("Credenciales de GitHub no configuradas", module="GitHubAuth")
            return None
        
        try:
            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "redirect_uri": redirect_uri
            }
            
            headers = {"Accept": "application/json"}
            
            response = requests.post(self.token_url, data=data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                token_data = response.json()
                return token_data.get("access_token")
            else:
                self.logger.error(f"Error al obtener token: {response.status_code}", module="GitHubAuth")
                return None
                
        except Exception as e:
            self.logger.error(f"Error en intercambio de token: {e}", module="GitHubAuth")
            return None
    
    def get_user_info(self, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene información del usuario autenticado.
        
        Args:
            access_token: Token de acceso de GitHub
            
        Returns:
            Diccionario con información del usuario o None si falla
        """
        try:
            headers = {
                "Authorization": f"token {access_token}",
                "Accept": "application/json"
            }
            
            response = requests.get(f"{self.api_url}/user", headers=headers, timeout=10)
            
            if response.status_code == 200:
                user_data = response.json()
                return {
                    "id": user_data.get("id"),
                    "username": user_data.get("login"),
                    "name": user_data.get("name"),
                    "email": user_data.get("email"),
                    "avatar_url": user_data.get("avatar_url"),
                    "provider": "github"
                }
            else:
                self.logger.error(f"Error al obtener info de usuario: {response.status_code}", module="GitHubAuth")
                return None
                
        except Exception as e:
            self.logger.error(f"Error al obtener info de usuario: {e}", module="GitHubAuth")
            return None
    
    def authenticate(self, code: str, redirect_uri: str) -> Optional[Dict[str, Any]]:
        """
        Autentica un usuario con GitHub.
        
        Args:
            code: Código de autorización
            redirect_uri: URI de redirección
            
        Returns:
            Información del usuario autenticado o None si falla
        """
        token = self.exchange_code_for_token(code, redirect_uri)
        
        if not token:
            return None
        
        user_info = self.get_user_info(token)
        
        if user_info:
            self.logger.info(f"Usuario autenticado con GitHub: {user_info['username']}", module="GitHubAuth")
            user_info["access_token"] = token
            return user_info
        
        return None
