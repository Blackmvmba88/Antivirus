"""
Sensor Base - Clase base abstracta para todos los sensores
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
from fireguard.core.logger import Logger
from fireguard.core.config_manager import ConfigManager


class SensorBase(ABC):
    """
    Clase base abstracta para todos los sensores de monitoreo.
    
    Los sensores son módulos expansibles que monitorizan aspectos
    específicos del sistema (puertos, procesos, disco, logs, etc.)
    """
    
    def __init__(self, name: str, config: Optional[ConfigManager] = None):
        """
        Inicializa el sensor.
        
        Args:
            name: Nombre del sensor
            config: Gestor de configuración opcional
        """
        self.name = name
        self.logger = Logger()
        self.config = config or ConfigManager()
        self.enabled = True
        self.last_scan_time: Optional[datetime] = None
        self.last_scan_results: Optional[Dict[str, Any]] = None
    
    @abstractmethod
    def scan(self) -> Dict[str, Any]:
        """
        Realiza un escaneo del recurso que monitorea el sensor.
        
        Returns:
            Dict con los resultados del escaneo
        """
        pass
    
    @abstractmethod
    def analyze(self, scan_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analiza los resultados del escaneo para detectar anomalías.
        
        Args:
            scan_results: Resultados del escaneo
            
        Returns:
            Lista de alertas/anomalías detectadas
        """
        pass
    
    def run(self) -> Dict[str, Any]:
        """
        Ejecuta el sensor: escanea y analiza.
        
        Returns:
            Dict con resultados completos del sensor
        """
        if not self.enabled:
            self.logger.debug(f"Sensor {self.name} está deshabilitado", module=self.name)
            return {"enabled": False, "status": "disabled"}
        
        try:
            self.logger.info(f"Ejecutando sensor {self.name}", module=self.name)
            
            # Escanear
            scan_results = self.scan()
            self.last_scan_time = datetime.now()
            self.last_scan_results = scan_results
            
            # Analizar
            alerts = self.analyze(scan_results)
            
            result = {
                "sensor": self.name,
                "timestamp": self.last_scan_time.isoformat(),
                "status": "success",
                "scan_results": scan_results,
                "alerts": alerts,
                "alert_count": len(alerts)
            }
            
            if alerts:
                self.logger.warning(
                    f"Sensor {self.name} detectó {len(alerts)} alerta(s)",
                    module=self.name
                )
            
            return result
            
        except Exception as e:
            self.logger.exception(f"Error en sensor {self.name}: {e}", module=self.name)
            return {
                "sensor": self.name,
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "error": str(e)
            }
    
    def enable(self):
        """Habilita el sensor"""
        self.enabled = True
        self.logger.info(f"Sensor {self.name} habilitado", module=self.name)
    
    def disable(self):
        """Deshabilita el sensor"""
        self.enabled = False
        self.logger.info(f"Sensor {self.name} deshabilitado", module=self.name)
    
    def get_status(self) -> Dict[str, Any]:
        """
        Obtiene el estado actual del sensor.
        
        Returns:
            Dict con información de estado
        """
        return {
            "name": self.name,
            "enabled": self.enabled,
            "last_scan": self.last_scan_time.isoformat() if self.last_scan_time else None,
            "last_results": self.last_scan_results
        }
