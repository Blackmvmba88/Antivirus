"""
Config Loader - Cargador de Configuración

Este módulo implementa la carga y validación de configuración
del sistema desde archivos YAML o JSON, proporcionando acceso
centralizado a la configuración.
"""

import logging
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigLoader:
    """
    Cargador de configuración del sistema.
    
    Lee archivos de configuración en formato YAML o JSON y proporciona
    acceso estructurado a los parámetros del sistema.
    """
    
    def __init__(self):
        """Inicializa el cargador de configuración."""
        self.logger = logging.getLogger(__name__)
        self.config: Dict[str, Any] = {}
    
    def load_from_file(self, config_path: str) -> Dict[str, Any]:
        """
        Carga la configuración desde un archivo.
        
        Args:
            config_path: Ruta al archivo de configuración
            
        Returns:
            Diccionario con la configuración cargada
            
        Raises:
            FileNotFoundError: Si el archivo no existe
            ValueError: Si el formato es inválido
        """
        path = Path(config_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Archivo de configuración no encontrado: {config_path}")
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                if path.suffix in ['.yaml', '.yml']:
                    self.config = yaml.safe_load(f)
                elif path.suffix == '.json':
                    self.config = json.load(f)
                else:
                    raise ValueError(f"Formato de archivo no soportado: {path.suffix}")
            
            self.logger.info(f"Configuración cargada desde: {config_path}")
            return self.config
        
        except Exception as e:
            self.logger.error(f"Error al cargar configuración: {e}")
            raise
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtiene un valor de configuración.
        
        Args:
            key: Clave de configuración (soporta notación punto: 'section.key')
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
    
    def set(self, key: str, value: Any) -> None:
        """
        Establece un valor de configuración.
        
        Args:
            key: Clave de configuración
            value: Valor a establecer
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_all(self) -> Dict[str, Any]:
        """
        Obtiene toda la configuración.
        
        Returns:
            Diccionario completo de configuración
        """
        return self.config.copy()
