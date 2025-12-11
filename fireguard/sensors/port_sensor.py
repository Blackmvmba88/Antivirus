"""
Port Sensor - Monitoreo de puertos abiertos en el sistema
"""

import psutil
from typing import Dict, Any, List
from fireguard.core.sensor_base import SensorBase


class PortSensor(SensorBase):
    """
    Sensor para monitorear puertos abiertos en el sistema.
    
    Detecta conexiones activas, puertos en escucha y posibles
    actividades sospechosas en la red.
    """
    
    def __init__(self, config=None):
        """Inicializa el sensor de puertos"""
        super().__init__("PortSensor", config)
        
        # Puertos comunes que deberían monitorearse
        self.common_ports = {
            20: "FTP Data",
            21: "FTP Control",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            143: "IMAP",
            443: "HTTPS",
            445: "SMB",
            3306: "MySQL",
            3389: "RDP",
            5432: "PostgreSQL",
            8080: "HTTP Alt",
        }
        
        # Puertos conocidos como peligrosos
        self.dangerous_ports = [23, 445, 3389]
    
    def scan(self) -> Dict[str, Any]:
        """
        Escanea los puertos abiertos en el sistema.
        
        Returns:
            Dict con información de puertos y conexiones
        """
        try:
            connections = psutil.net_connections(kind='inet')
            
            listening_ports = []
            established_connections = []
            
            for conn in connections:
                if conn.status == 'LISTEN':
                    port_info = {
                        "port": conn.laddr.port,
                        "address": conn.laddr.ip,
                        "pid": conn.pid,
                        "service": self.common_ports.get(conn.laddr.port, "Unknown")
                    }
                    listening_ports.append(port_info)
                
                elif conn.status == 'ESTABLISHED':
                    conn_info = {
                        "local_port": conn.laddr.port,
                        "remote_addr": conn.raddr.ip if conn.raddr else "N/A",
                        "remote_port": conn.raddr.port if conn.raddr else 0,
                        "pid": conn.pid,
                        "status": conn.status
                    }
                    established_connections.append(conn_info)
            
            return {
                "listening_ports": listening_ports,
                "established_connections": established_connections,
                "total_listening": len(listening_ports),
                "total_established": len(established_connections)
            }
            
        except Exception as e:
            self.logger.error(f"Error al escanear puertos: {e}", module=self.name)
            return {
                "error": str(e),
                "listening_ports": [],
                "established_connections": []
            }
    
    def analyze(self, scan_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analiza los resultados del escaneo de puertos.
        
        Args:
            scan_results: Resultados del escaneo
            
        Returns:
            Lista de alertas detectadas
        """
        alerts = []
        
        listening_ports = scan_results.get("listening_ports", [])
        
        for port_info in listening_ports:
            port = port_info["port"]
            
            # Detectar puertos peligrosos abiertos
            if port in self.dangerous_ports:
                alerts.append({
                    "severity": "high",
                    "type": "dangerous_port",
                    "message": f"Puerto peligroso abierto: {port} ({port_info['service']})",
                    "details": port_info
                })
            
            # Detectar puertos no estándar en escucha
            if port > 1024 and port not in self.common_ports:
                alerts.append({
                    "severity": "medium",
                    "type": "unusual_port",
                    "message": f"Puerto inusual en escucha: {port}",
                    "details": port_info
                })
        
        # Detectar gran número de conexiones establecidas
        established_count = scan_results.get("total_established", 0)
        if established_count > 50:
            alerts.append({
                "severity": "medium",
                "type": "high_connection_count",
                "message": f"Número elevado de conexiones establecidas: {established_count}",
                "details": {"count": established_count}
            })
        
        return alerts
