"""
Process Sensor - Monitoreo de procesos en ejecución
"""

import psutil
from typing import Dict, Any, List
from fireguard.core.sensor_base import SensorBase


class ProcessSensor(SensorBase):
    """
    Sensor para monitorear procesos en ejecución en el sistema.
    
    Detecta procesos sospechosos, uso elevado de recursos y
    posibles amenazas de seguridad.
    """
    
    def __init__(self, config=None):
        """Inicializa el sensor de procesos"""
        super().__init__("ProcessSensor", config)
        
        # Procesos conocidos como peligrosos o sospechosos
        self.suspicious_names = [
            "cryptominer", "miner", "xmrig", "backdoor",
            "keylogger", "trojan", "malware", "virus"
        ]
        
        # Umbrales de uso de recursos
        self.cpu_threshold = 80.0  # Porcentaje
        self.memory_threshold = 80.0  # Porcentaje
    
    def scan(self) -> Dict[str, Any]:
        """
        Escanea los procesos en ejecución.
        
        Returns:
            Dict con información de procesos
        """
        try:
            processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
                try:
                    proc_info = proc.info
                    processes.append({
                        "pid": proc_info['pid'],
                        "name": proc_info['name'],
                        "username": proc_info['username'],
                        "cpu_percent": proc_info['cpu_percent'] or 0.0,
                        "memory_percent": proc_info['memory_percent'] or 0.0
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Información general del sistema
            cpu_count = psutil.cpu_count()
            memory_info = psutil.virtual_memory()
            
            return {
                "processes": processes,
                "total_processes": len(processes),
                "system_cpu_percent": psutil.cpu_percent(interval=1),
                "system_memory_percent": memory_info.percent,
                "cpu_count": cpu_count
            }
            
        except Exception as e:
            self.logger.error(f"Error al escanear procesos: {e}", module=self.name)
            return {
                "error": str(e),
                "processes": [],
                "total_processes": 0
            }
    
    def analyze(self, scan_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analiza los resultados del escaneo de procesos.
        
        Args:
            scan_results: Resultados del escaneo
            
        Returns:
            Lista de alertas detectadas
        """
        alerts = []
        
        processes = scan_results.get("processes", [])
        
        for proc in processes:
            # Detectar nombres sospechosos
            proc_name_lower = proc['name'].lower()
            for suspicious in self.suspicious_names:
                if suspicious in proc_name_lower:
                    alerts.append({
                        "severity": "critical",
                        "type": "suspicious_process",
                        "message": f"Proceso sospechoso detectado: {proc['name']}",
                        "details": proc
                    })
            
            # Detectar alto uso de CPU
            if proc['cpu_percent'] > self.cpu_threshold:
                alerts.append({
                    "severity": "medium",
                    "type": "high_cpu_usage",
                    "message": f"Proceso con uso elevado de CPU: {proc['name']} ({proc['cpu_percent']:.1f}%)",
                    "details": proc
                })
            
            # Detectar alto uso de memoria
            if proc['memory_percent'] > self.memory_threshold:
                alerts.append({
                    "severity": "medium",
                    "type": "high_memory_usage",
                    "message": f"Proceso con uso elevado de memoria: {proc['name']} ({proc['memory_percent']:.1f}%)",
                    "details": proc
                })
        
        # Detectar uso elevado del sistema
        system_cpu = scan_results.get("system_cpu_percent", 0)
        if system_cpu > 90:
            alerts.append({
                "severity": "high",
                "type": "system_overload",
                "message": f"Uso elevado de CPU del sistema: {system_cpu:.1f}%",
                "details": {"cpu_percent": system_cpu}
            })
        
        system_memory = scan_results.get("system_memory_percent", 0)
        if system_memory > 90:
            alerts.append({
                "severity": "high",
                "type": "memory_overload",
                "message": f"Uso elevado de memoria del sistema: {system_memory:.1f}%",
                "details": {"memory_percent": system_memory}
            })
        
        return alerts
