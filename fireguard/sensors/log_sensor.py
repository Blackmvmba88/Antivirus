"""
Log Sensor - Monitoreo de logs del sistema
"""

import os
import re
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime, timedelta
from fireguard.core.sensor_base import SensorBase
from fireguard.core.platform_detector import PlatformDetector


class LogSensor(SensorBase):
    """
    Sensor para monitorear logs del sistema.
    
    Analiza logs en busca de errores, advertencias y eventos
    de seguridad sospechosos.
    """
    
    def __init__(self, config=None):
        """Inicializa el sensor de logs"""
        super().__init__("LogSensor", config)
        
        self.platform = PlatformDetector()
        
        # Patrones sospechosos en logs
        self.suspicious_patterns = [
            r"failed password",
            r"authentication failure",
            r"invalid user",
            r"unauthorized",
            r"permission denied",
            r"access denied",
            r"error.*security",
            r"attack",
            r"intrusion",
            r"malware",
        ]
        
        # Configurar rutas de logs según la plataforma
        self.log_paths = self._get_log_paths()
    
    def _get_log_paths(self) -> List[str]:
        """
        Obtiene las rutas de logs según la plataforma.
        
        Returns:
            Lista de rutas de logs
        """
        if self.platform.is_linux():
            return [
                "/var/log/auth.log",
                "/var/log/syslog",
                "/var/log/messages",
            ]
        elif self.platform.is_macos():
            return [
                "/var/log/system.log",
            ]
        elif self.platform.is_windows():
            # En Windows se usarían APIs de Windows Event Log
            return []
        else:
            return []
    
    def scan(self) -> Dict[str, Any]:
        """
        Escanea los logs del sistema.
        
        Returns:
            Dict con información de logs
        """
        if not self.platform.supports_feature("log_monitoring"):
            return {
                "supported": False,
                "message": "Monitoreo de logs no soportado en esta plataforma",
                "log_entries": []
            }
        
        try:
            log_entries = []
            
            for log_path in self.log_paths:
                if not os.path.exists(log_path):
                    continue
                
                try:
                    # Leer las últimas líneas del log
                    with open(log_path, 'r', errors='ignore') as f:
                        lines = f.readlines()
                        
                        # Analizar las últimas 100 líneas
                        recent_lines = lines[-100:] if len(lines) > 100 else lines
                        
                        for line in recent_lines:
                            log_entries.append({
                                "source": log_path,
                                "content": line.strip(),
                                "timestamp": datetime.now().isoformat()
                            })
                            
                except PermissionError:
                    self.logger.warning(
                        f"Sin permisos para leer: {log_path}",
                        module=self.name
                    )
                    continue
            
            return {
                "supported": True,
                "log_entries": log_entries,
                "total_entries": len(log_entries),
                "sources_scanned": len([p for p in self.log_paths if os.path.exists(p)])
            }
            
        except Exception as e:
            self.logger.error(f"Error al escanear logs: {e}", module=self.name)
            return {
                "error": str(e),
                "log_entries": [],
                "total_entries": 0
            }
    
    def analyze(self, scan_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analiza los resultados del escaneo de logs.
        
        Args:
            scan_results: Resultados del escaneo
            
        Returns:
            Lista de alertas detectadas
        """
        if not scan_results.get("supported", False):
            return []
        
        alerts = []
        log_entries = scan_results.get("log_entries", [])
        
        for entry in log_entries:
            content = entry['content'].lower()
            
            # Buscar patrones sospechosos
            for pattern in self.suspicious_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    alerts.append({
                        "severity": "medium",
                        "type": "suspicious_log_entry",
                        "message": f"Entrada sospechosa en log: {pattern}",
                        "details": {
                            "source": entry['source'],
                            "content": entry['content'][:200],  # Limitar longitud
                            "pattern_matched": pattern
                        }
                    })
                    break  # Solo una alerta por entrada
        
        return alerts
