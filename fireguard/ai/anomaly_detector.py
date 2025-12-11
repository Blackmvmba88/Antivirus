"""
Anomaly Detector - Base para detección de anomalías con IA
"""

import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime
from fireguard.core.logger import Logger
from fireguard.core.config_manager import ConfigManager


class AnomalyDetector:
    """
    Sistema base para detección de anomalías.
    
    Preparado para integrar modelos de IA en el futuro para
    detectar comportamientos anómalos en el sistema.
    """
    
    def __init__(self, config: Optional[ConfigManager] = None):
        """
        Inicializa el detector de anomalías.
        
        Args:
            config: Gestor de configuración
        """
        self.logger = Logger()
        self.config = config or ConfigManager()
        self.enabled = self.config.get("ai.anomaly_detection", False)
        
        # Historial de métricas para análisis
        self.history: List[Dict[str, Any]] = []
        self.max_history_size = 1000
        
        self.logger.info(
            f"AnomalyDetector inicializado (enabled={self.enabled})",
            module="AnomalyDetector"
        )
    
    def add_metrics(self, metrics: Dict[str, Any]):
        """
        Añade métricas al historial para análisis.
        
        Args:
            metrics: Métricas del sistema a analizar
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics
        }
        
        self.history.append(entry)
        
        # Mantener tamaño del historial
        if len(self.history) > self.max_history_size:
            self.history = self.history[-self.max_history_size:]
    
    def detect_anomalies(self, current_metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detecta anomalías en las métricas actuales.
        
        Args:
            current_metrics: Métricas actuales del sistema
            
        Returns:
            Lista de anomalías detectadas
        """
        if not self.enabled:
            return []
        
        anomalies = []
        
        # Análisis básico usando estadísticas simples
        # En el futuro, aquí se integrarían modelos de ML
        
        # Por ahora, hacemos análisis estadístico simple
        anomalies.extend(self._statistical_analysis(current_metrics))
        
        return anomalies
    
    def _statistical_analysis(self, current_metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Análisis estadístico básico de métricas.
        
        Args:
            current_metrics: Métricas actuales
            
        Returns:
            Lista de anomalías detectadas
        """
        anomalies = []
        
        if len(self.history) < 10:
            # No hay suficiente historial para análisis
            return anomalies
        
        # Analizar CPU
        if "cpu_percent" in current_metrics:
            cpu_values = [
                h["metrics"].get("cpu_percent", 0) 
                for h in self.history 
                if "cpu_percent" in h["metrics"]
            ]
            
            if cpu_values:
                mean_cpu = np.mean(cpu_values)
                std_cpu = np.std(cpu_values)
                current_cpu = current_metrics["cpu_percent"]
                
                # Detectar si el valor actual está fuera de 2 desviaciones estándar
                if abs(current_cpu - mean_cpu) > 2 * std_cpu:
                    anomalies.append({
                        "type": "cpu_anomaly",
                        "severity": "medium",
                        "message": f"Uso de CPU anómalo: {current_cpu:.1f}% (media: {mean_cpu:.1f}%)",
                        "details": {
                            "current": current_cpu,
                            "mean": mean_cpu,
                            "std_dev": std_cpu
                        }
                    })
        
        # Analizar memoria
        if "memory_percent" in current_metrics:
            memory_values = [
                h["metrics"].get("memory_percent", 0) 
                for h in self.history 
                if "memory_percent" in h["metrics"]
            ]
            
            if memory_values:
                mean_memory = np.mean(memory_values)
                std_memory = np.std(memory_values)
                current_memory = current_metrics["memory_percent"]
                
                if abs(current_memory - mean_memory) > 2 * std_memory:
                    anomalies.append({
                        "type": "memory_anomaly",
                        "severity": "medium",
                        "message": f"Uso de memoria anómalo: {current_memory:.1f}% (media: {mean_memory:.1f}%)",
                        "details": {
                            "current": current_memory,
                            "mean": mean_memory,
                            "std_dev": std_memory
                        }
                    })
        
        return anomalies
    
    def get_baseline(self) -> Dict[str, Any]:
        """
        Obtiene la línea base de métricas del sistema.
        
        Returns:
            Dict con métricas promedio del historial
        """
        if not self.history:
            return {}
        
        # Calcular promedios
        cpu_values = [h["metrics"].get("cpu_percent", 0) for h in self.history if "cpu_percent" in h["metrics"]]
        memory_values = [h["metrics"].get("memory_percent", 0) for h in self.history if "memory_percent" in h["metrics"]]
        
        baseline = {}
        
        if cpu_values:
            baseline["cpu"] = {
                "mean": np.mean(cpu_values),
                "std": np.std(cpu_values),
                "min": np.min(cpu_values),
                "max": np.max(cpu_values)
            }
        
        if memory_values:
            baseline["memory"] = {
                "mean": np.mean(memory_values),
                "std": np.std(memory_values),
                "min": np.min(memory_values),
                "max": np.max(memory_values)
            }
        
        return baseline
    
    def enable(self):
        """Habilita el detector de anomalías"""
        self.enabled = True
        self.logger.info("Detector de anomalías habilitado", module="AnomalyDetector")
    
    def disable(self):
        """Deshabilita el detector de anomalías"""
        self.enabled = False
        self.logger.info("Detector de anomalías deshabilitado", module="AnomalyDetector")
