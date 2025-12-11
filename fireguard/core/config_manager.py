"""
Configuration Manager - Gestión de configuración del sistema
"""

import os
import json
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from fireguard.core.logger import Logger


class ConfigManager:
    """
    Gestor de configuración para FIREGUARD.
    
    Maneja la carga, guardado y acceso a la configuración del sistema
    desde archivos YAML o JSON.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Inicializa el gestor de configuración.
        
        Args:
            config_path: Ruta al archivo de configuración
        """
        self.logger = Logger()
        self.config_path = config_path or self._get_default_config_path()
        self.config: Dict[str, Any] = {}
        self._load_config()
    
    def _get_default_config_path(self) -> str:
        """Obtiene la ruta por defecto del archivo de configuración"""
        return os.path.join("config", "config.yaml")
    
    def _load_config(self):
        """Carga la configuración desde el archivo"""
        config_file = Path(self.config_path)
        
        if not config_file.exists():
            self.logger.warning(
                f"Archivo de configuración no encontrado: {self.config_path}. "
                "Usando configuración por defecto.",
                module="ConfigManager"
            )
            self._create_default_config()
            return
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                if config_file.suffix == '.json':
                    self.config = json.load(f)
                else:  # yaml
                    self.config = yaml.safe_load(f) or {}
            
            self.logger.info(
                f"Configuración cargada desde: {self.config_path}",
                module="ConfigManager"
            )
        except Exception as e:
            self.logger.error(
                f"Error al cargar configuración: {e}",
                module="ConfigManager"
            )
            self._create_default_config()
    
    def _create_default_config(self):
        """Crea una configuración por defecto"""
        self.config = {
            "system": {
                "name": "FIREGUARD AI",
                "version": "0.1.0",
                "log_level": "INFO",
            },
            "monitoring": {
                "enabled": True,
                "interval": 60,  # segundos
                "sensors": {
                    "ports": True,
                    "processes": True,
                    "disk": True,
                    "logs": True,
                }
            },
            "security": {
                "require_authentication": True,
                "auth_methods": ["local"],  # local, github, google
                "session_timeout": 3600,  # segundos
            },
            "alerts": {
                "enabled": True,
                "threshold": "medium",  # low, medium, high, critical
            },
            "ai": {
                "enabled": False,  # Preparado para futuras capacidades de IA
                "anomaly_detection": False,
            }
        }
        
        # Guardar configuración por defecto
        self.save_config()
    
    def save_config(self, config_path: Optional[str] = None):
        """
        Guarda la configuración en el archivo.
        
        Args:
            config_path: Ruta opcional para guardar la configuración
        """
        save_path = config_path or self.config_path
        config_file = Path(save_path)
        
        # Crear directorio si no existe
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                if config_file.suffix == '.json':
                    json.dump(self.config, f, indent=2)
                else:  # yaml
                    yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
            
            self.logger.info(
                f"Configuración guardada en: {save_path}",
                module="ConfigManager"
            )
        except Exception as e:
            self.logger.error(
                f"Error al guardar configuración: {e}",
                module="ConfigManager"
            )
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtiene un valor de configuración.
        
        Args:
            key: Clave de configuración (soporta notación punto, ej: 'system.name')
            default: Valor por defecto si la clave no existe
            
        Returns:
            Valor de configuración o default
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """
        Establece un valor de configuración.
        
        Args:
            key: Clave de configuración (soporta notación punto)
            value: Valor a establecer
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_all(self) -> Dict[str, Any]:
        """Obtiene toda la configuración"""
        return self.config.copy()
    
    def reload(self):
        """Recarga la configuración desde el archivo"""
        self._load_config()
