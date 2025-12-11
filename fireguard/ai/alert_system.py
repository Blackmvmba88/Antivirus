"""
Alert System - Sistema de gestión de alertas
"""

from typing import Dict, Any, List, Callable, Optional
from datetime import datetime
from fireguard.core.logger import Logger
from fireguard.core.config_manager import ConfigManager


class AlertSystem:
    """
    Sistema de gestión y notificación de alertas.
    
    Centraliza todas las alertas del sistema y permite configurar
    acciones y notificaciones.
    """
    
    def __init__(self, config: Optional[ConfigManager] = None):
        """
        Inicializa el sistema de alertas.
        
        Args:
            config: Gestor de configuración
        """
        self.logger = Logger()
        self.config = config or ConfigManager()
        self.enabled = self.config.get("alerts.enabled", True)
        
        # Umbrales de severidad
        self.threshold = self.config.get("alerts.threshold", "medium")
        self.severity_levels = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4
        }
        
        # Almacenamiento de alertas
        self.alerts: List[Dict[str, Any]] = []
        self.max_alerts = 1000
        
        # Callbacks para notificaciones
        self.alert_callbacks: List[Callable] = []
        
        self.logger.info(
            f"AlertSystem inicializado (threshold={self.threshold})",
            module="AlertSystem"
        )
    
    def add_alert(self, alert: Dict[str, Any]):
        """
        Añade una nueva alerta al sistema.
        
        Args:
            alert: Diccionario con información de la alerta
        """
        if not self.enabled:
            return
        
        # Verificar si la alerta cumple con el umbral
        alert_severity = alert.get("severity", "low")
        threshold_level = self.severity_levels.get(self.threshold, 2)
        alert_level = self.severity_levels.get(alert_severity, 1)
        
        if alert_level < threshold_level:
            return  # Alerta por debajo del umbral
        
        # Añadir timestamp si no existe
        if "timestamp" not in alert:
            alert["timestamp"] = datetime.now().isoformat()
        
        # Añadir la alerta
        self.alerts.append(alert)
        
        # Mantener límite de alertas
        if len(self.alerts) > self.max_alerts:
            self.alerts = self.alerts[-self.max_alerts:]
        
        # Log de la alerta
        severity = alert.get("severity", "unknown")
        message = alert.get("message", "Sin mensaje")
        self.logger.warning(
            f"[{severity.upper()}] {message}",
            module="AlertSystem"
        )
        
        # Ejecutar callbacks
        self._notify_callbacks(alert)
    
    def add_alerts(self, alerts: List[Dict[str, Any]]):
        """
        Añade múltiples alertas al sistema.
        
        Args:
            alerts: Lista de alertas
        """
        for alert in alerts:
            self.add_alert(alert)
    
    def register_callback(self, callback: Callable):
        """
        Registra un callback para notificaciones de alertas.
        
        Args:
            callback: Función a llamar cuando hay una nueva alerta
        """
        self.alert_callbacks.append(callback)
        self.logger.info("Callback de alerta registrado", module="AlertSystem")
    
    def _notify_callbacks(self, alert: Dict[str, Any]):
        """
        Notifica a los callbacks registrados.
        
        Args:
            alert: Alerta a notificar
        """
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                self.logger.error(
                    f"Error en callback de alerta: {e}",
                    module="AlertSystem"
                )
    
    def get_alerts(
        self,
        severity: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Obtiene alertas del sistema.
        
        Args:
            severity: Filtrar por severidad (opcional)
            limit: Límite de alertas a retornar (opcional)
            
        Returns:
            Lista de alertas
        """
        alerts = self.alerts
        
        # Filtrar por severidad si se especifica
        if severity:
            alerts = [a for a in alerts if a.get("severity") == severity]
        
        # Aplicar límite si se especifica
        if limit:
            alerts = alerts[-limit:]
        
        return alerts
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """
        Obtiene un resumen de las alertas.
        
        Returns:
            Dict con estadísticas de alertas
        """
        summary = {
            "total": len(self.alerts),
            "by_severity": {},
            "by_type": {}
        }
        
        for alert in self.alerts:
            # Contar por severidad
            severity = alert.get("severity", "unknown")
            summary["by_severity"][severity] = summary["by_severity"].get(severity, 0) + 1
            
            # Contar por tipo
            alert_type = alert.get("type", "unknown")
            summary["by_type"][alert_type] = summary["by_type"].get(alert_type, 0) + 1
        
        return summary
    
    def clear_alerts(self):
        """Limpia todas las alertas"""
        count = len(self.alerts)
        self.alerts = []
        self.logger.info(f"Limpiadas {count} alertas", module="AlertSystem")
    
    def set_threshold(self, threshold: str):
        """
        Establece el umbral de severidad de alertas.
        
        Args:
            threshold: Umbral ('low', 'medium', 'high', 'critical')
        """
        if threshold in self.severity_levels:
            self.threshold = threshold
            self.logger.info(
                f"Umbral de alertas cambiado a: {threshold}",
                module="AlertSystem"
            )
        else:
            self.logger.warning(
                f"Umbral inválido: {threshold}",
                module="AlertSystem"
            )
    
    def enable(self):
        """Habilita el sistema de alertas"""
        self.enabled = True
        self.logger.info("Sistema de alertas habilitado", module="AlertSystem")
    
    def disable(self):
        """Deshabilita el sistema de alertas"""
        self.enabled = False
        self.logger.info("Sistema de alertas deshabilitado", module="AlertSystem")
