"""
Core module initialization
"""

from fireguard.core.platform_detector import PlatformDetector
from fireguard.core.config_manager import ConfigManager
from fireguard.core.logger import Logger
from fireguard.core.sensor_base import SensorBase

__all__ = [
    "PlatformDetector",
    "ConfigManager",
    "Logger",
    "SensorBase",
]
