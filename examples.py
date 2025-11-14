"""
FIREGUARD AI - Ejemplos de Uso Completos
Este archivo contiene ejemplos prácticos de todas las funcionalidades
"""

# ============================================================================
# EJEMPLO 1: Detección de Plataforma
# ============================================================================

def ejemplo_plataforma():
    """Ejemplo de detección de plataforma"""
    from fireguard.core import PlatformDetector
    
    print("=" * 60)
    print("EJEMPLO 1: Detección de Plataforma")
    print("=" * 60)
    
    # Crear detector
    platform = PlatformDetector()
    
    # Obtener tipo de plataforma
    print(f"Plataforma: {platform.platform_name}")
    
    # Verificar plataforma específica
    if platform.is_linux():
        print("Ejecutando en Linux")
    elif platform.is_windows():
        print("Ejecutando en Windows")
    elif platform.is_macos():
        print("Ejecutando en macOS")
    elif platform.is_android():
        print("Ejecutando en Android/Termux")
    
    # Verificar soporte de características
    if platform.supports_feature("port_monitoring"):
        print("✓ Monitoreo de puertos soportado")
    
    # Obtener información completa
    info = platform.get_info()
    print(f"Python: {info['details']['python_version']}")
    print()


# ============================================================================
# EJEMPLO 2: Configuración
# ============================================================================

def ejemplo_configuracion():
    """Ejemplo de gestión de configuración"""
    from fireguard.core import ConfigManager
    
    print("=" * 60)
    print("EJEMPLO 2: Gestión de Configuración")
    print("=" * 60)
    
    config = ConfigManager()
    
    # Obtener valores con notación punto
    sistema = config.get('system.name')
    intervalo = config.get('monitoring.interval', 60)
    
    print(f"Sistema: {sistema}")
    print(f"Intervalo de monitoreo: {intervalo} segundos")
    
    # Establecer valores
    config.set('monitoring.interval', 120)
    config.set('alerts.threshold', 'high')
    
    # Obtener toda la configuración
    all_config = config.get_all()
    print(f"Configuración tiene {len(all_config)} secciones")
    
    # Guardar cambios
    config.save_config()
    print("✓ Configuración guardada")
    print()


# ============================================================================
# EJEMPLO 3: Autenticación Local
# ============================================================================

def ejemplo_autenticacion_local():
    """Ejemplo de autenticación local"""
    from fireguard.auth import LocalAuth
    import tempfile
    import os
    
    print("=" * 60)
    print("EJEMPLO 3: Autenticación Local")
    print("=" * 60)
    
    # Crear archivo temporal para el ejemplo
    fd, temp_file = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    
    try:
        auth = LocalAuth(users_file=temp_file)
        
        # Crear usuario
        print("Creando usuario 'alice'...")
        auth.create_user("alice", "password123", role="user")
        
        # Autenticar
        print("Autenticando usuario...")
        if auth.authenticate("alice", "password123"):
            print("✓ Autenticación exitosa")
        
        # Verificar rol
        role = auth.get_user_role("alice")
        print(f"Rol de alice: {role}")
        
        # Cambiar contraseña
        print("Cambiando contraseña...")
        auth.change_password("alice", "password123", "new_secure_pass")
        
        # Autenticar con nueva contraseña
        if auth.authenticate("alice", "new_secure_pass"):
            print("✓ Nueva contraseña funciona")
        
        # Eliminar usuario
        auth.delete_user("alice")
        print("✓ Usuario eliminado")
        
    finally:
        os.remove(temp_file)
    
    print()


# ============================================================================
# EJEMPLO 4: Gestión de Sesiones
# ============================================================================

def ejemplo_sesiones():
    """Ejemplo de gestión de sesiones"""
    from fireguard.auth import AuthManager
    from fireguard.core import ConfigManager
    
    print("=" * 60)
    print("EJEMPLO 4: Gestión de Sesiones")
    print("=" * 60)
    
    config = ConfigManager()
    auth_manager = AuthManager(config)
    
    # Autenticar y obtener token
    print("Iniciando sesión...")
    token = auth_manager.authenticate_local("admin", "fireguard2024")
    
    if token:
        print(f"✓ Token de sesión: {token[:20]}...")
        
        # Validar sesión
        if auth_manager.validate_session(token):
            print("✓ Sesión válida")
        
        # Obtener información del usuario
        user_info = auth_manager.get_session_user(token)
        print(f"Usuario autenticado: {user_info['username']}")
        print(f"Rol: {user_info.get('role', 'N/A')}")
        
        # Número de sesiones activas
        active = auth_manager.get_active_sessions_count()
        print(f"Sesiones activas: {active}")
        
        # Cerrar sesión
        auth_manager.logout(token)
        print("✓ Sesión cerrada")
    
    print()


# ============================================================================
# EJEMPLO 5: Sensores Individuales
# ============================================================================

def ejemplo_sensores():
    """Ejemplo de uso de sensores"""
    from fireguard.sensors import PortSensor, ProcessSensor, DiskSensor
    from fireguard.core import ConfigManager
    
    print("=" * 60)
    print("EJEMPLO 5: Sensores de Monitoreo")
    print("=" * 60)
    
    config = ConfigManager()
    
    # Sensor de puertos
    print("\n--- Sensor de Puertos ---")
    port_sensor = PortSensor(config)
    port_result = port_sensor.run()
    
    if port_result['status'] == 'success':
        print(f"Puertos en escucha: {port_result['scan_results'].get('total_listening', 0)}")
        print(f"Conexiones establecidas: {port_result['scan_results'].get('total_established', 0)}")
        print(f"Alertas: {port_result['alert_count']}")
    
    # Sensor de procesos
    print("\n--- Sensor de Procesos ---")
    process_sensor = ProcessSensor(config)
    process_result = process_sensor.run()
    
    if process_result['status'] == 'success':
        print(f"Procesos totales: {process_result['scan_results'].get('total_processes', 0)}")
        print(f"CPU del sistema: {process_result['scan_results'].get('system_cpu_percent', 0):.1f}%")
        print(f"Alertas: {process_result['alert_count']}")
    
    # Sensor de disco
    print("\n--- Sensor de Disco ---")
    disk_sensor = DiskSensor(config)
    disk_result = disk_sensor.run()
    
    if disk_result['status'] == 'success':
        partitions = disk_result['scan_results'].get('partitions', [])
        print(f"Particiones monitoreadas: {len(partitions)}")
        for part in partitions[:2]:  # Mostrar primeras 2
            print(f"  {part['mountpoint']}: {part['percent']:.1f}% usado")
        print(f"Alertas: {disk_result['alert_count']}")
    
    print()


# ============================================================================
# EJEMPLO 6: Sistema de Alertas
# ============================================================================

def ejemplo_alertas():
    """Ejemplo de sistema de alertas"""
    from fireguard.ai import AlertSystem
    from fireguard.core import ConfigManager
    
    print("=" * 60)
    print("EJEMPLO 6: Sistema de Alertas")
    print("=" * 60)
    
    config = ConfigManager()
    alert_system = AlertSystem(config)
    
    # Añadir alertas de diferentes severidades
    alertas = [
        {
            "severity": "low",
            "type": "info",
            "message": "Información del sistema"
        },
        {
            "severity": "medium",
            "type": "warning",
            "message": "Advertencia de uso de recursos"
        },
        {
            "severity": "high",
            "type": "security",
            "message": "Evento de seguridad detectado"
        },
        {
            "severity": "critical",
            "type": "threat",
            "message": "Amenaza crítica detectada"
        }
    ]
    
    print("Añadiendo alertas...")
    for alerta in alertas:
        alert_system.add_alert(alerta)
    
    # Obtener resumen
    summary = alert_system.get_alert_summary()
    print(f"\nTotal de alertas: {summary['total']}")
    print("Por severidad:")
    for severity, count in summary['by_severity'].items():
        print(f"  {severity}: {count}")
    
    # Obtener alertas específicas
    critical_alerts = alert_system.get_alerts(severity="critical")
    print(f"\nAlertas críticas: {len(critical_alerts)}")
    
    # Cambiar umbral
    alert_system.set_threshold("high")
    print("✓ Umbral cambiado a 'high'")
    
    # Limpiar alertas
    alert_system.clear_alerts()
    print("✓ Alertas limpiadas")
    print()


# ============================================================================
# EJEMPLO 7: Detección de Anomalías
# ============================================================================

def ejemplo_anomalias():
    """Ejemplo de detección de anomalías"""
    from fireguard.ai import AnomalyDetector
    from fireguard.core import ConfigManager
    import psutil
    import time
    
    print("=" * 60)
    print("EJEMPLO 7: Detección de Anomalías")
    print("=" * 60)
    
    config = ConfigManager()
    detector = AnomalyDetector(config)
    detector.enable()
    
    print("Recopilando métricas base...")
    
    # Recopilar métricas históricas
    for i in range(10):
        metrics = {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent
        }
        detector.add_metrics(metrics)
        time.sleep(0.1)
    
    print("✓ Métricas recopiladas")
    
    # Obtener línea base
    baseline = detector.get_baseline()
    if 'cpu' in baseline:
        print(f"CPU promedio: {baseline['cpu']['mean']:.1f}%")
    if 'memory' in baseline:
        print(f"Memoria promedio: {baseline['memory']['mean']:.1f}%")
    
    # Detectar anomalías
    current = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent
    }
    
    anomalies = detector.detect_anomalies(current)
    print(f"\nAnomalías detectadas: {len(anomalies)}")
    
    for anomaly in anomalies:
        print(f"  [{anomaly['severity']}] {anomaly['message']}")
    
    print()


# ============================================================================
# EJEMPLO 8: Escaneo Completo con Reporte
# ============================================================================

def ejemplo_escaneo_completo():
    """Ejemplo de escaneo completo del sistema"""
    from fireguard.core import ConfigManager
    from fireguard.sensors import PortSensor, ProcessSensor, DiskSensor
    from fireguard.ai import AlertSystem
    import json
    
    print("=" * 60)
    print("EJEMPLO 8: Escaneo Completo del Sistema")
    print("=" * 60)
    
    config = ConfigManager()
    alert_system = AlertSystem(config)
    
    # Lista de sensores a ejecutar
    sensors = [
        PortSensor(config),
        ProcessSensor(config),
        DiskSensor(config)
    ]
    
    print("\nEjecutando escaneo completo...")
    results = []
    
    for sensor in sensors:
        print(f"  Escaneando con {sensor.name}...", end="")
        result = sensor.run()
        results.append(result)
        
        # Añadir alertas al sistema
        if 'alerts' in result:
            alert_system.add_alerts(result['alerts'])
        
        print(f" ✓ ({result['alert_count']} alertas)")
    
    # Generar reporte
    print("\n--- REPORTE ---")
    summary = alert_system.get_alert_summary()
    
    print(f"Total de alertas: {summary['total']}")
    if summary['by_severity']:
        print("Por severidad:")
        for severity, count in summary['by_severity'].items():
            print(f"  {severity}: {count}")
    
    # Exportar a JSON
    reporte = {
        "sensors": results,
        "summary": summary
    }
    
    print("\nReporte JSON:")
    print(json.dumps(reporte, indent=2)[:500] + "...")
    print()


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Ejecuta todos los ejemplos"""
    print("\n" + "=" * 60)
    print("  FIREGUARD AI - Ejemplos de Uso")
    print("=" * 60 + "\n")
    
    ejemplos = [
        ejemplo_plataforma,
        ejemplo_configuracion,
        ejemplo_autenticacion_local,
        ejemplo_sesiones,
        ejemplo_sensores,
        ejemplo_alertas,
        ejemplo_anomalias,
        ejemplo_escaneo_completo
    ]
    
    for ejemplo in ejemplos:
        try:
            ejemplo()
            input("Presiona Enter para continuar...")
        except KeyboardInterrupt:
            print("\n\n¡Ejemplos interrumpidos!")
            break
        except Exception as e:
            print(f"Error en ejemplo: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("  ✓ Ejemplos completados")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
