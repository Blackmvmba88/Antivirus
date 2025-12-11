"""
Disk Sensor - Monitoreo de disco y archivos
"""

import psutil
import os
from pathlib import Path
from typing import Dict, Any, List
from fireguard.core.sensor_base import SensorBase


class DiskSensor(SensorBase):
    """
    Sensor para monitorear el uso de disco y archivos del sistema.
    
    Detecta problemas de espacio en disco, particiones con alto uso
    y posibles problemas de almacenamiento.
    """
    
    def __init__(self, config=None):
        """Inicializa el sensor de disco"""
        super().__init__("DiskSensor", config)
        
        # Umbrales de uso de disco
        self.warning_threshold = 80.0  # Porcentaje
        self.critical_threshold = 90.0  # Porcentaje
    
    def scan(self) -> Dict[str, Any]:
        """
        Escanea el uso de disco en el sistema.
        
        Returns:
            Dict con información de discos y particiones
        """
        try:
            partitions = []
            
            for partition in psutil.disk_partitions(all=False):
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    
                    partition_info = {
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "fstype": partition.fstype,
                        "total_gb": usage.total / (1024 ** 3),
                        "used_gb": usage.used / (1024 ** 3),
                        "free_gb": usage.free / (1024 ** 3),
                        "percent": usage.percent
                    }
                    partitions.append(partition_info)
                    
                except PermissionError:
                    continue
            
            # Información de I/O de disco
            disk_io = psutil.disk_io_counters()
            
            return {
                "partitions": partitions,
                "total_partitions": len(partitions),
                "disk_io": {
                    "read_count": disk_io.read_count if disk_io else 0,
                    "write_count": disk_io.write_count if disk_io else 0,
                    "read_bytes": disk_io.read_bytes if disk_io else 0,
                    "write_bytes": disk_io.write_bytes if disk_io else 0,
                } if disk_io else None
            }
            
        except Exception as e:
            self.logger.error(f"Error al escanear disco: {e}", module=self.name)
            return {
                "error": str(e),
                "partitions": [],
                "total_partitions": 0
            }
    
    def analyze(self, scan_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analiza los resultados del escaneo de disco.
        
        Args:
            scan_results: Resultados del escaneo
            
        Returns:
            Lista de alertas detectadas
        """
        alerts = []
        
        partitions = scan_results.get("partitions", [])
        
        for partition in partitions:
            percent = partition['percent']
            mountpoint = partition['mountpoint']
            
            # Alerta crítica: espacio de disco muy bajo
            if percent >= self.critical_threshold:
                alerts.append({
                    "severity": "critical",
                    "type": "disk_critical",
                    "message": f"Espacio crítico en disco {mountpoint}: {percent:.1f}% usado",
                    "details": partition
                })
            
            # Alerta de advertencia: espacio de disco bajo
            elif percent >= self.warning_threshold:
                alerts.append({
                    "severity": "high",
                    "type": "disk_warning",
                    "message": f"Espacio bajo en disco {mountpoint}: {percent:.1f}% usado",
                    "details": partition
                })
            
            # Alerta de espacio libre muy bajo
            if partition['free_gb'] < 1.0:
                alerts.append({
                    "severity": "critical",
                    "type": "disk_almost_full",
                    "message": f"Menos de 1 GB libre en {mountpoint}",
                    "details": partition
                })
        
        return alerts
