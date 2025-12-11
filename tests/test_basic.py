"""
Tests básicos para FIREGUARD AI
"""

import pytest
from fireguard.core.platform_detector import PlatformDetector, PlatformType
from fireguard.core.config_manager import ConfigManager
from fireguard.core.logger import Logger
from fireguard.auth.local_auth import LocalAuth


def test_platform_detector():
    """Test del detector de plataforma"""
    platform = PlatformDetector()
    
    # Verificar que se detecta una plataforma válida
    assert platform.platform_type in [
        PlatformType.WINDOWS,
        PlatformType.MACOS,
        PlatformType.LINUX,
        PlatformType.ANDROID
    ]
    
    # Verificar que hay detalles de plataforma
    details = platform.details
    assert 'system' in details
    assert 'python_version' in details


def test_config_manager():
    """Test del gestor de configuración"""
    config = ConfigManager()
    
    # Verificar valores por defecto
    assert config.get('system.name') == 'FIREGUARD AI'
    assert config.get('system.version') == '0.1.0'
    assert config.get('monitoring.enabled') is True
    
    # Test de set y get
    config.set('test.value', 'test_data')
    assert config.get('test.value') == 'test_data'


def test_logger():
    """Test del sistema de logging"""
    logger = Logger()
    
    # Verificar que el logger se inicializa correctamente
    assert logger.logger is not None
    
    # Test de diferentes niveles de log (no deberían lanzar excepciones)
    logger.info("Test info message")
    logger.debug("Test debug message")
    logger.warning("Test warning message")


def test_local_auth():
    """Test de autenticación local"""
    import tempfile
    import os
    
    # Crear archivo temporal para usuarios
    fd, temp_users_file = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    
    try:
        local_auth = LocalAuth(users_file=temp_users_file)
        
        # Crear usuario de prueba
        assert local_auth.create_user("testuser", "testpass", role="user") is True
        
        # Autenticar correctamente
        assert local_auth.authenticate("testuser", "testpass") is True
        
        # Autenticar con contraseña incorrecta
        assert local_auth.authenticate("testuser", "wrongpass") is False
        
        # Verificar rol
        assert local_auth.get_user_role("testuser") == "user"
        
        # Cambiar contraseña
        assert local_auth.change_password("testuser", "testpass", "newpass") is True
        assert local_auth.authenticate("testuser", "newpass") is True
        
        # Eliminar usuario
        assert local_auth.delete_user("testuser") is True
        assert local_auth.authenticate("testuser", "newpass") is False
        
    finally:
        # Limpiar archivo temporal
        if os.path.exists(temp_users_file):
            os.remove(temp_users_file)


def test_sensor_interface():
    """Test de la interfaz base de sensores"""
    from fireguard.sensors import PortSensor, ProcessSensor, DiskSensor
    
    config = ConfigManager()
    
    # Crear sensores
    port_sensor = PortSensor(config)
    process_sensor = ProcessSensor(config)
    disk_sensor = DiskSensor(config)
    
    # Verificar nombres
    assert port_sensor.name == "PortSensor"
    assert process_sensor.name == "ProcessSensor"
    assert disk_sensor.name == "DiskSensor"
    
    # Verificar que están habilitados por defecto
    assert port_sensor.enabled is True
    assert process_sensor.enabled is True
    assert disk_sensor.enabled is True


def test_alert_system():
    """Test del sistema de alertas"""
    from fireguard.ai import AlertSystem
    
    config = ConfigManager()
    alert_system = AlertSystem(config)
    
    # Añadir alerta
    alert = {
        "severity": "high",
        "type": "test_alert",
        "message": "Test alert message"
    }
    
    alert_system.add_alert(alert)
    
    # Verificar que se añadió
    alerts = alert_system.get_alerts()
    assert len(alerts) > 0
    
    # Obtener resumen
    summary = alert_system.get_alert_summary()
    assert summary['total'] > 0
    assert 'high' in summary['by_severity']
    
    # Limpiar alertas
    alert_system.clear_alerts()
    assert len(alert_system.get_alerts()) == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
