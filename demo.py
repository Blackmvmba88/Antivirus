#!/usr/bin/env python3
"""
FIREGUARD AI - Script de Demostración
Este script demuestra las capacidades principales del sistema
"""

import time
from fireguard import __version__
from fireguard.core import PlatformDetector, ConfigManager, Logger
from fireguard.auth import AuthManager
from fireguard.sensors import PortSensor, ProcessSensor, DiskSensor, LogSensor
from fireguard.ai import AlertSystem, AnomalyDetector


def print_header(title):
    """Imprime un encabezado formateado"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")


def demo_platform_detection():
    """Demuestra la detección de plataforma"""
    print_header("🖥️  DETECCIÓN DE PLATAFORMA")
    
    platform = PlatformDetector()
    info = platform.get_info()
    
    print(f"Plataforma detectada: {info['platform_type']}")
    print(f"Sistema: {info['details']['system']}")
    print(f"Release: {info['details']['release']}")
    print(f"Arquitectura: {info['details']['machine']}")
    print(f"Python: {info['details']['python_version']}")
    
    print("\nCaracterísticas soportadas:")
    for feature, supported in info['features'].items():
        status = "✓" if supported else "✗"
        print(f"  {status} {feature}")


def demo_authentication():
    """Demuestra el sistema de autenticación"""
    print_header("🔐 AUTENTICACIÓN")
    
    config = ConfigManager()
    auth_manager = AuthManager(config)
    
    # Intentar autenticación con credenciales por defecto
    print("Intentando autenticación local...")
    token = auth_manager.authenticate_local("admin", "fireguard2024")
    
    if token:
        print(f"✓ Autenticación exitosa!")
        print(f"Token de sesión: {token[:20]}...")
        
        # Obtener información del usuario
        user_info = auth_manager.get_session_user(token)
        print(f"Usuario: {user_info['username']}")
        print(f"Proveedor: {user_info['provider']}")
        print(f"Rol: {user_info.get('role', 'N/A')}")
        
        # Cerrar sesión
        auth_manager.logout(token)
        print("✓ Sesión cerrada")
    else:
        print("✗ Autenticación fallida")


def demo_sensors():
    """Demuestra los sensores de monitoreo"""
    print_header("📡 SENSORES DE MONITOREO")
    
    config = ConfigManager()
    alert_system = AlertSystem(config)
    
    sensors = [
        ("Puertos", PortSensor(config)),
        ("Procesos", ProcessSensor(config)),
        ("Disco", DiskSensor(config)),
        ("Logs", LogSensor(config)),
    ]
    
    for name, sensor in sensors:
        print(f"\nEjecutando sensor: {name}")
        print("-" * 40)
        
        result = sensor.run()
        
        if result['status'] == 'success':
            print(f"✓ Escaneo completado")
            
            alert_count = result.get('alert_count', 0)
            if alert_count > 0:
                print(f"⚠ Detectadas {alert_count} alerta(s)")
                
                # Mostrar primeras 2 alertas
                for alert in result.get('alerts', [])[:2]:
                    severity = alert.get('severity', 'unknown')
                    message = alert.get('message', 'Sin mensaje')
                    print(f"  • [{severity.upper()}] {message}")
                
                # Añadir alertas al sistema
                alert_system.add_alerts(result['alerts'])
            else:
                print("✓ Sin alertas detectadas")
        else:
            print(f"✗ Error: {result.get('error', 'Desconocido')}")
    
    # Resumen de alertas
    print("\n" + "-" * 40)
    summary = alert_system.get_alert_summary()
    print(f"Total de alertas: {summary['total']}")
    
    if summary['by_severity']:
        print("Por severidad:")
        for severity, count in summary['by_severity'].items():
            print(f"  {severity}: {count}")


def demo_anomaly_detection():
    """Demuestra la detección de anomalías"""
    print_header("🤖 DETECCIÓN DE ANOMALÍAS (IA)")
    
    config = ConfigManager()
    anomaly_detector = AnomalyDetector(config)
    
    print("Estado del detector: ", end="")
    if anomaly_detector.enabled:
        print("Habilitado ✓")
    else:
        print("Deshabilitado (habilitar en config)")
        print("Habilitando para demostración...")
        anomaly_detector.enable()
    
    # Simular recopilación de métricas
    print("\nRecopilando métricas del sistema...")
    
    import psutil
    
    for i in range(15):
        metrics = {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "timestamp": time.time()
        }
        anomaly_detector.add_metrics(metrics)
        print(f"  Métrica #{i+1} recopilada", end="\r")
        time.sleep(0.1)
    
    print("\n\nAnalizando métricas para anomalías...")
    
    # Obtener línea base
    baseline = anomaly_detector.get_baseline()
    
    if baseline:
        print("\nLínea base establecida:")
        if 'cpu' in baseline:
            print(f"  CPU promedio: {baseline['cpu']['mean']:.1f}%")
        if 'memory' in baseline:
            print(f"  Memoria promedio: {baseline['memory']['mean']:.1f}%")
    
    # Detectar anomalías con métricas actuales
    current_metrics = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent
    }
    
    anomalies = anomaly_detector.detect_anomalies(current_metrics)
    
    if anomalies:
        print(f"\n⚠ Detectadas {len(anomalies)} anomalía(s):")
        for anomaly in anomalies:
            print(f"  • [{anomaly['severity'].upper()}] {anomaly['message']}")
    else:
        print("\n✓ No se detectaron anomalías")


def main():
    """Función principal"""
    print("\n" + "="*60)
    print("  🔥 FIREGUARD AI - Demostración del Sistema")
    print(f"  Versión {__version__}")
    print("="*60)
    
    # Ejecutar demostraciones
    try:
        demo_platform_detection()
        time.sleep(1)
        
        demo_authentication()
        time.sleep(1)
        
        demo_sensors()
        time.sleep(1)
        
        demo_anomaly_detection()
        
        # Mensaje final
        print_header("✅ DEMOSTRACIÓN COMPLETADA")
        print("El sistema FIREGUARD AI está funcionando correctamente.")
        print("\nPróximos pasos:")
        print("  1. Cambiar las credenciales por defecto")
        print("  2. Configurar sensores según necesidades")
        print("  3. Habilitar detección de anomalías en config")
        print("  4. Configurar OAuth (opcional)")
        print("\nPara más información: fireguard --help")
        print()
        
    except KeyboardInterrupt:
        print("\n\nDemostración interrumpida por el usuario.")
    except Exception as e:
        print(f"\n\nError durante la demostración: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
