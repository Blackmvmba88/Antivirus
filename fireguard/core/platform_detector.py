"""
Platform Detector - Detecta el sistema operativo y plataforma
Soporta: Windows, macOS, Linux, Android (Termux)
"""

import platform
import os
from enum import Enum
from typing import Dict, Any


class PlatformType(Enum):
    """Tipos de plataforma soportados"""
    WINDOWS = "windows"
    MACOS = "macos"
    LINUX = "linux"
    ANDROID = "android"
    UNKNOWN = "unknown"


class PlatformDetector:
    """
    Detector de plataforma multiplataforma.
    
    Detecta automáticamente el sistema operativo y proporciona
    información sobre capacidades y restricciones de la plataforma.
    """
    
    def __init__(self):
        self._platform = self._detect_platform()
        self._details = self._gather_platform_details()
    
    def _detect_platform(self) -> PlatformType:
        """
        Detecta la plataforma actual.
        
        Returns:
            PlatformType: Tipo de plataforma detectada
        """
        system = platform.system().lower()
        
        # Detectar Android/Termux
        if os.path.exists('/system/build.prop') or os.environ.get('ANDROID_ROOT'):
            return PlatformType.ANDROID
        
        # Detectar otros sistemas
        if system == "windows":
            return PlatformType.WINDOWS
        elif system == "darwin":
            return PlatformType.MACOS
        elif system == "linux":
            return PlatformType.LINUX
        else:
            return PlatformType.UNKNOWN
    
    def _gather_platform_details(self) -> Dict[str, Any]:
        """
        Recopila detalles sobre la plataforma.
        
        Returns:
            Dict con información detallada de la plataforma
        """
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
        }
    
    @property
    def platform_type(self) -> PlatformType:
        """Obtiene el tipo de plataforma"""
        return self._platform
    
    @property
    def platform_name(self) -> str:
        """Obtiene el nombre de la plataforma"""
        return self._platform.value
    
    @property
    def details(self) -> Dict[str, Any]:
        """Obtiene detalles de la plataforma"""
        return self._details.copy()
    
    def is_windows(self) -> bool:
        """Verifica si es Windows"""
        return self._platform == PlatformType.WINDOWS
    
    def is_macos(self) -> bool:
        """Verifica si es macOS"""
        return self._platform == PlatformType.MACOS
    
    def is_linux(self) -> bool:
        """Verifica si es Linux"""
        return self._platform == PlatformType.LINUX
    
    def is_android(self) -> bool:
        """Verifica si es Android/Termux"""
        return self._platform == PlatformType.ANDROID
    
    def supports_feature(self, feature: str) -> bool:
        """
        Verifica si la plataforma soporta una característica específica.
        
        Args:
            feature: Nombre de la característica a verificar
            
        Returns:
            bool: True si la característica es soportada
        """
        feature_support = {
            "port_monitoring": True,  # Todas las plataformas
            "process_monitoring": True,  # Todas las plataformas
            "disk_monitoring": True,  # Todas las plataformas
            "log_monitoring": not self.is_android(),  # Limitado en Android
            "system_logs": not self.is_android(),  # No disponible en Android sin root
        }
        
        return feature_support.get(feature, False)
    
    def get_info(self) -> Dict[str, Any]:
        """
        Obtiene información completa de la plataforma.
        
        Returns:
            Dict con toda la información de la plataforma
        """
        return {
            "platform_type": self.platform_name,
            "details": self.details,
            "features": {
                "port_monitoring": self.supports_feature("port_monitoring"),
                "process_monitoring": self.supports_feature("process_monitoring"),
                "disk_monitoring": self.supports_feature("disk_monitoring"),
                "log_monitoring": self.supports_feature("log_monitoring"),
                "system_logs": self.supports_feature("system_logs"),
            }
        }
