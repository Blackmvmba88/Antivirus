"""
Logger Setup - Configuración de Logging

Este módulo proporciona utilidades para configurar el sistema de logging
del proyecto FIREGUARD AI, estableciendo formatos, niveles y destinos
de los logs.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str = "fireguard",
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    console: bool = True
) -> logging.Logger:
    """
    Configura y retorna un logger para el sistema.
    
    Args:
        name: Nombre del logger
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Ruta opcional al archivo de log
        console: Si True, también muestra logs en consola
        
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Limpiar handlers existentes
    logger.handlers.clear()
    
    # Formato de log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para consola
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # Handler para archivo
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger existente o crea uno nuevo.
    
    Args:
        name: Nombre del logger
        
    Returns:
        Logger
    """
    return logging.getLogger(name)
