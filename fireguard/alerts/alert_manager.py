"""
Alert Manager - Gestor de Alertas

Este módulo implementa el sistema de gestión de alertas,
clasificando, priorizando y procesando alertas de seguridad
detectadas por el sistema FIREGUARD AI.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class AlertLevel(Enum):
    """Niveles de severidad de alertas."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class Alert:
    """
    Representa una alerta del sistema.
    
    Attributes:
        id: Identificador único de la alerta
        level: Nivel de severidad
        message: Mensaje descriptivo
        timestamp: Momento de generación
        source: Origen de la alerta
    """
    
    def __init__(self, level: AlertLevel, message: str, source: str):
        """
        Crea una nueva alerta.
        
        Args:
            level: Nivel de severidad
            message: Mensaje descriptivo
            source: Origen de la alerta
        """
        self.id = hash(f"{datetime.now()}{message}")
        self.level = level
        self.message = message
        self.source = source
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la alerta a diccionario."""
        return {
            "id": self.id,
            "level": self.level.value,
            "message": self.message,
            "source": self.source,
            "timestamp": self.timestamp.isoformat()
        }


class AlertManager:
    """
    Gestor central de alertas del sistema.
    
    Gestiona la creación, almacenamiento y procesamiento de alertas
    de seguridad generadas por los diferentes módulos.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa el gestor de alertas.
        
        Args:
            config: Configuración opcional del gestor
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        self.alerts: List[Alert] = []
        self.logger.info("AlertManager inicializado")
    
    def create_alert(self, level: AlertLevel, message: str, source: str) -> Alert:
        """
        Crea y registra una nueva alerta.
        
        Args:
            level: Nivel de severidad
            message: Mensaje descriptivo
            source: Origen de la alerta
            
        Returns:
            Alert: La alerta creada
        """
        alert = Alert(level, message, source)
        self.alerts.append(alert)
        self.logger.log(
            self._get_log_level(level),
            f"[{source}] {message}"
        )
        return alert
    
    def get_alerts(self, level: Optional[AlertLevel] = None) -> List[Alert]:
        """
        Obtiene alertas, opcionalmente filtradas por nivel.
        
        Args:
            level: Nivel de severidad para filtrar (opcional)
            
        Returns:
            Lista de alertas
        """
        if level:
            return [a for a in self.alerts if a.level == level]
        return self.alerts
    
    def clear_alerts(self) -> int:
        """
        Limpia todas las alertas almacenadas.
        
        Returns:
            int: Número de alertas eliminadas
        """
        count = len(self.alerts)
        self.alerts.clear()
        self.logger.info(f"Alertas limpiadas: {count}")
        return count
    
    def _get_log_level(self, alert_level: AlertLevel) -> int:
        """Convierte AlertLevel a nivel de logging."""
        mapping = {
            AlertLevel.INFO: logging.INFO,
            AlertLevel.WARNING: logging.WARNING,
            AlertLevel.CRITICAL: logging.CRITICAL,
            AlertLevel.EMERGENCY: logging.CRITICAL
        }
        return mapping.get(alert_level, logging.INFO)
