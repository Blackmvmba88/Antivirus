# 🔥 FIREGUARD AI

**Sistema Modular Multiplataforma de Vigilancia y Seguridad con IA**

FIREGUARD AI es un sistema de monitoreo de seguridad modular y expansible diseñado para vigilar puertos, logs, disco y procesos en múltiples plataformas. Incluye autenticación robusta y está preparado para integrar capacidades de inteligencia artificial para detección de anomalías.

## 🌟 Características

### 🖥️ Multiplataforma
- ✅ **macOS** - Soporte completo
- ✅ **Windows** - Soporte completo
- ✅ **Linux** - Soporte completo
- ✅ **Android/Termux** - Soporte con limitaciones

### 🔒 Seguridad y Autenticación
- **Autenticación Local** - Usuario y contraseña con encriptación
- **GitHub OAuth** - Autenticación con cuenta de GitHub
- **Google OAuth** - Autenticación con cuenta de Google
- **Gestión de Sesiones** - Sistema seguro de tokens y sesiones

### 📡 Sensores de Monitoreo
Los sensores son módulos expansibles que monitorizan aspectos específicos del sistema:

1. **PortSensor** - Vigilancia de puertos abiertos y conexiones
   - Detecta puertos peligrosos
   - Monitorea conexiones establecidas
   - Identifica servicios en ejecución

2. **ProcessSensor** - Monitoreo de procesos en ejecución
   - Detecta procesos sospechosos
   - Monitorea uso de CPU y memoria
   - Identifica sobrecarga del sistema

3. **DiskSensor** - Monitoreo de espacio en disco
   - Detecta bajo espacio en disco
   - Monitorea particiones
   - Alertas de espacio crítico

4. **LogSensor** - Análisis de logs del sistema
   - Busca patrones sospechosos
   - Detecta intentos de autenticación fallidos
   - Identifica eventos de seguridad

### 🤖 Preparado para IA
- **AnomalyDetector** - Base para detección de anomalías con machine learning
- **AlertSystem** - Sistema centralizado de gestión de alertas
- Análisis estadístico de métricas del sistema
- Arquitectura lista para integrar modelos de ML/IA

## 🚀 Instalación

### Requisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación básica

```bash
# Clonar el repositorio
git clone https://github.com/Blackmvmba88/Antivirus.git
cd Antivirus

# Instalar dependencias
pip install -r requirements.txt

# Instalar FIREGUARD
pip install -e .
```

### Instalación en Termux (Android)

```bash
# Actualizar paquetes
pkg update && pkg upgrade

# Instalar Python
pkg install python

# Instalar dependencias del sistema
pkg install build-essential

# Instalar FIREGUARD
pip install -r requirements.txt
pip install -e .
```

## 📖 Uso

### CLI - Interfaz de Línea de Comandos

FIREGUARD proporciona una interfaz de línea de comandos completa:

```bash
# Mostrar información del sistema
fireguard info

# Ejecutar escaneo de seguridad (todos los sensores)
fireguard scan

# Escanear sensor específico
fireguard scan --sensor ports
fireguard scan --sensor processes
fireguard scan --sensor disk
fireguard scan --sensor logs

# Generar reporte en formato JSON
fireguard scan --format json

# Autenticación
fireguard auth

# Generar reporte completo
fireguard report

# Guardar reporte en archivo
fireguard report --output report.json

# Mostrar configuración
fireguard config

# Mostrar ayuda
fireguard --help
```

### Uso Programático

```python
from fireguard.core import PlatformDetector, ConfigManager, Logger
from fireguard.sensors import PortSensor, ProcessSensor, DiskSensor
from fireguard.auth import AuthManager
from fireguard.ai import AlertSystem, AnomalyDetector

# Detectar plataforma
platform = PlatformDetector()
print(f"Plataforma: {platform.platform_name}")

# Inicializar configuración
config = ConfigManager()

# Autenticación
auth_manager = AuthManager(config)
token = auth_manager.authenticate_local("admin", "password")

# Ejecutar sensores
port_sensor = PortSensor(config)
result = port_sensor.run()

# Sistema de alertas
alert_system = AlertSystem(config)
alert_system.add_alerts(result['alerts'])

# Detección de anomalías
anomaly_detector = AnomalyDetector(config)
anomaly_detector.enable()
```

## 🏗️ Arquitectura

### Estructura del Proyecto

```
fireguard/
├── core/                    # Núcleo del sistema
│   ├── platform_detector.py  # Detección de plataforma
│   ├── config_manager.py     # Gestión de configuración
│   ├── logger.py             # Sistema de logging
│   └── sensor_base.py        # Clase base para sensores
├── auth/                    # Sistema de autenticación
│   ├── auth_manager.py       # Gestor central de autenticación
│   ├── local_auth.py         # Autenticación local
│   ├── github_auth.py        # OAuth GitHub
│   └── google_auth.py        # OAuth Google
├── sensors/                 # Sensores de monitoreo
│   ├── port_sensor.py        # Sensor de puertos
│   ├── process_sensor.py     # Sensor de procesos
│   ├── disk_sensor.py        # Sensor de disco
│   └── log_sensor.py         # Sensor de logs
├── ai/                      # Capacidades de IA
│   ├── anomaly_detector.py   # Detector de anomalías
│   └── alert_system.py       # Sistema de alertas
└── cli/                     # Interfaz de línea de comandos
    └── main.py               # CLI principal
```

### Diseño Modular

El sistema está diseñado con una arquitectura modular que permite:

1. **Expansibilidad** - Fácil adición de nuevos sensores
2. **Mantenibilidad** - Código claro y bien documentado
3. **Flexibilidad** - Configuración adaptable a diferentes necesidades
4. **Escalabilidad** - Preparado para crecer con nuevas capacidades

## 🔧 Configuración

El sistema utiliza archivos de configuración YAML/JSON:

```yaml
system:
  name: "FIREGUARD AI"
  version: "0.1.0"
  log_level: "INFO"

monitoring:
  enabled: true
  interval: 60  # segundos
  sensors:
    ports: true
    processes: true
    disk: true
    logs: true

security:
  require_authentication: true
  auth_methods: ["local"]  # local, github, google
  session_timeout: 3600

alerts:
  enabled: true
  threshold: "medium"  # low, medium, high, critical

ai:
  enabled: false
  anomaly_detection: false
```

### Autenticación OAuth

Para usar GitHub o Google OAuth, configure las credenciales:

```yaml
auth:
  github:
    client_id: "your_github_client_id"
    client_secret: "your_github_client_secret"
  google:
    client_id: "your_google_client_id"
    client_secret: "your_google_client_secret"
```

## 🔐 Seguridad

### Usuario por Defecto

⚠️ **IMPORTANTE**: Al instalar, se crea un usuario administrador por defecto:
- **Usuario**: `admin`
- **Contraseña**: `fireguard2024`

**DEBE cambiar estas credenciales inmediatamente** en producción.

### Mejores Prácticas

1. Cambie las credenciales por defecto
2. Use autenticación OAuth cuando sea posible
3. Configure umbrales de alertas apropiados
4. Revise los logs regularmente
5. Mantenga el sistema actualizado

## 🛠️ Desarrollo

### Crear un Nuevo Sensor

```python
from fireguard.core.sensor_base import SensorBase
from typing import Dict, Any, List

class MiSensor(SensorBase):
    def __init__(self, config=None):
        super().__init__("MiSensor", config)
    
    def scan(self) -> Dict[str, Any]:
        # Implementar lógica de escaneo
        return {"data": "..."}
    
    def analyze(self, scan_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        # Implementar análisis y detección de anomalías
        alerts = []
        return alerts
```

### Ejecutar Tests

```bash
# Instalar dependencias de desarrollo
pip install pytest pytest-cov

# Ejecutar tests
pytest

# Con cobertura
pytest --cov=fireguard
```

## 📊 Ejemplo de Reporte

```json
{
  "timestamp": "2024-11-14T10:00:00",
  "version": "0.1.0",
  "platform": {
    "platform_type": "linux",
    "details": {...}
  },
  "sensors": [
    {
      "sensor": "PortSensor",
      "status": "success",
      "alerts": [...]
    }
  ],
  "alert_summary": {
    "total": 5,
    "by_severity": {
      "high": 2,
      "medium": 3
    }
  }
}
```

## 🤝 Contribuir

Las contribuciones son bienvenidas! Para contribuir:

1. Fork el proyecto
2. Cree una rama para su característica (`git checkout -b feature/AmazingFeature`)
3. Commit sus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abra un Pull Request

## 📝 Licencia

Este proyecto está licenciado bajo la Licencia Apache 2.0 - vea el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- Comunidad de código abierto
- Contribuidores del proyecto
- Herramientas y librerías utilizadas (psutil, click, colorama, etc.)

## 📧 Contacto

Para preguntas, sugerencias o reportar problemas:
- Abra un issue en GitHub
- Consulte la documentación en `docs/`

---

**FIREGUARD AI** - Protegiendo tu sistema con inteligencia 🔥🛡️
