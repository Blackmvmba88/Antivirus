"""
Alerts Module - Módulo de Alertas

Este módulo gestiona el sistema de alertas y notificaciones,
incluyendo la generación, categorización y envío de alertas
sobre amenazas detectadas y eventos del sistema.
"""

from .alert_manager import AlertManager
from .notification_service import NotificationService

__all__ = ['AlertManager', 'NotificationService']
