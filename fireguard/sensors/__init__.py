"""
Sensors Module - Módulo de Sensores

Este módulo contiene los sensores de monitoreo del sistema,
incluyendo monitoreo de puertos, análisis de logs y detección
de actividades sospechosas en el sistema.
"""

from .port_monitor import PortMonitor
from .log_analyzer import LogAnalyzer

__all__ = ['PortMonitor', 'LogAnalyzer']
