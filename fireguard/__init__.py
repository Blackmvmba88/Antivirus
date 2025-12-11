"""
FIREGUARD AI - Sistema Modular de Vigilancia y Seguridad
Version: 0.1.0

Sistema multiplataforma para monitoreo de seguridad con capacidades de IA.
"""

__version__ = "0.1.0"
__author__ = "FIREGUARD Team"

from fireguard.core.platform_detector import PlatformDetector
from fireguard.core.config_manager import ConfigManager
from fireguard.core.logger import Logger

__all__ = [
    "PlatformDetector",
    "ConfigManager", 
    "Logger",
    "__version__",
]
