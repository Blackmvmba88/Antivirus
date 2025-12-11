"""
Notification Service - Servicio de Notificaciones

Este módulo implementa el servicio de envío de notificaciones,
distribuyendo alertas a través de diferentes canales (email, SMS, etc.)
según la configuración del usuario.
"""

import logging
from typing import Dict, List, Any, Optional
from enum import Enum


class NotificationChannel(Enum):
    """Canales de notificación disponibles."""
    EMAIL = "email"
    SMS = "sms"
    CONSOLE = "console"
    LOG = "log"


class NotificationService:
    """
    Servicio de envío de notificaciones.
    
    Gestiona el envío de notificaciones sobre alertas y eventos
    del sistema a través de diferentes canales configurados.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa el servicio de notificaciones.
        
        Args:
            config: Configuración opcional del servicio
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        self.enabled_channels = self.config.get('channels', [NotificationChannel.LOG])
        self.recipients = self.config.get('recipients', [])
        self.logger.info("NotificationService inicializado")
    
    def send_notification(
        self,
        message: str,
        channel: NotificationChannel,
        priority: str = "normal"
    ) -> bool:
        """
        Envía una notificación por el canal especificado.
        
        Args:
            message: Mensaje a enviar
            channel: Canal de notificación
            priority: Prioridad de la notificación
            
        Returns:
            bool: True si el envío fue exitoso
        """
        if channel not in self.enabled_channels:
            self.logger.warning(f"Canal {channel.value} no está habilitado")
            return False
        
        self.logger.info(f"Enviando notificación por {channel.value}: {message}")
        
        # Implementación básica - expandir en futuras versiones
        if channel == NotificationChannel.CONSOLE:
            print(f"[NOTIFICACIÓN] {message}")
            return True
        elif channel == NotificationChannel.LOG:
            self.logger.info(f"[NOTIFICACIÓN] {message}")
            return True
        
        return False
    
    def broadcast(self, message: str, priority: str = "normal") -> Dict[str, bool]:
        """
        Envía una notificación por todos los canales habilitados.
        
        Args:
            message: Mensaje a enviar
            priority: Prioridad de la notificación
            
        Returns:
            Diccionario con resultados por canal
        """
        results = {}
        for channel in self.enabled_channels:
            results[channel.value] = self.send_notification(message, channel, priority)
        return results
    
    def add_recipient(self, channel: NotificationChannel, recipient: str) -> bool:
        """
        Añade un destinatario para un canal específico.
        
        Args:
            channel: Canal de notificación
            recipient: Dirección/identificador del destinatario
            
        Returns:
            bool: True si se añadió correctamente
        """
        if channel.value not in self.recipients:
            self.recipients[channel.value] = []
        
        if recipient not in self.recipients[channel.value]:
            self.recipients[channel.value].append(recipient)
            self.logger.info(f"Destinatario {recipient} añadido a {channel.value}")
            return True
        return False
