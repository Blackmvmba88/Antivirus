"""
Logger - Sistema de logging centralizado para FIREGUARD
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class Logger:
    """
    Sistema de logging centralizado con soporte para múltiples niveles
    y rotación de archivos.
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Implementa patrón Singleton"""
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Inicializa el logger si no ha sido inicializado"""
        if not Logger._initialized:
            self._setup_logger()
            Logger._initialized = True
    
    def _setup_logger(self, log_dir: str = "logs", log_level: int = logging.INFO):
        """
        Configura el sistema de logging.
        
        Args:
            log_dir: Directorio para almacenar logs
            log_level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        # Crear directorio de logs si no existe
        log_path = Path(log_dir)
        log_path.mkdir(exist_ok=True)
        
        # Nombre del archivo de log con timestamp
        log_filename = log_path / f"fireguard_{datetime.now().strftime('%Y%m%d')}.log"
        
        # Configurar formato
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'
        
        # Configurar logging básico
        logging.basicConfig(
            level=log_level,
            format=log_format,
            datefmt=date_format,
            handlers=[
                logging.FileHandler(log_filename, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger('FIREGUARD')
        self.logger.setLevel(log_level)
    
    def debug(self, message: str, module: Optional[str] = None):
        """Log mensaje de debug"""
        if module:
            self.logger.debug(f"[{module}] {message}")
        else:
            self.logger.debug(message)
    
    def info(self, message: str, module: Optional[str] = None):
        """Log mensaje informativo"""
        if module:
            self.logger.info(f"[{module}] {message}")
        else:
            self.logger.info(message)
    
    def warning(self, message: str, module: Optional[str] = None):
        """Log mensaje de advertencia"""
        if module:
            self.logger.warning(f"[{module}] {message}")
        else:
            self.logger.warning(message)
    
    def error(self, message: str, module: Optional[str] = None):
        """Log mensaje de error"""
        if module:
            self.logger.error(f"[{module}] {message}")
        else:
            self.logger.error(message)
    
    def critical(self, message: str, module: Optional[str] = None):
        """Log mensaje crítico"""
        if module:
            self.logger.critical(f"[{module}] {message}")
        else:
            self.logger.critical(message)
    
    def exception(self, message: str, module: Optional[str] = None):
        """Log excepción con traceback"""
        if module:
            self.logger.exception(f"[{module}] {message}")
        else:
            self.logger.exception(message)
    
    def set_level(self, level: str):
        """
        Establece el nivel de logging.
        
        Args:
            level: Nivel de logging ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        """
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        
        log_level = level_map.get(level.upper(), logging.INFO)
        self.logger.setLevel(log_level)
