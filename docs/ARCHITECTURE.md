# 🏗️ Arquitectura de FIREGUARD AI

Este documento describe la arquitectura técnica del sistema FIREGUARD AI.

## Visión General

FIREGUARD AI está diseñado con una arquitectura modular de tres capas:

```
┌─────────────────────────────────────────────────────────────┐
│                      CLI / Interfaz                          │
│              (fireguard.cli.main)                            │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────┴─────────────────────────────────────┐
│                   Capa de Aplicación                         │
│  ┌──────────────┐  ┌───────────────┐  ┌─────────────┐      │
│  │     Auth     │  │   Sensors     │  │     AI      │      │
│  │   Manager    │  │   (4 tipos)   │  │  Detector   │      │
│  └──────────────┘  └───────────────┘  └─────────────┘      │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────┴─────────────────────────────────────┐
│                      Capa Core                               │
│  ┌──────────────┐  ┌───────────────┐  ┌─────────────┐      │
│  │  Platform    │  │    Config     │  │   Logger    │      │
│  │  Detector    │  │   Manager     │  │             │      │
│  └──────────────┘  └───────────────┘  └─────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## Componentes Principales

### 1. Core (Núcleo)

#### PlatformDetector
- **Responsabilidad**: Detecta el sistema operativo y plataforma
- **Soporta**: Windows, macOS, Linux, Android/Termux
- **Proporciona**: Información de capacidades por plataforma

```python
from fireguard.core import PlatformDetector

platform = PlatformDetector()
if platform.is_linux():
    # Código específico de Linux
```

#### ConfigManager
- **Responsabilidad**: Gestión centralizada de configuración
- **Formatos**: YAML (preferido) y JSON
- **Características**: 
  - Carga/guardado automático
  - Configuración por defecto
  - Notación punto para acceso anidado

```python
from fireguard.core import ConfigManager

config = ConfigManager()
value = config.get('monitoring.interval', 60)
config.set('alerts.threshold', 'high')
```

#### Logger
- **Responsabilidad**: Sistema de logging centralizado
- **Características**:
  - Patrón Singleton
  - Múltiples niveles (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - Rotación de archivos por día
  - Salida a archivo y consola

```python
from fireguard.core import Logger

logger = Logger()
logger.info("Mensaje informativo", module="MiModulo")
logger.error("Error detectado", module="MiModulo")
```

#### SensorBase
- **Responsabilidad**: Clase base abstracta para sensores
- **Patrón**: Template Method
- **Métodos requeridos**: `scan()`, `analyze()`

```python
from fireguard.core.sensor_base import SensorBase

class MiSensor(SensorBase):
    def scan(self):
        # Implementar escaneo
        return {"data": "..."}
    
    def analyze(self, results):
        # Implementar análisis
        return []
```

### 2. Authentication (Autenticación)

#### AuthManager
- **Responsabilidad**: Coordina múltiples métodos de autenticación
- **Soporta**: Local, GitHub OAuth, Google OAuth
- **Gestiona**: Sesiones con tokens y expiración

```python
from fireguard.auth import AuthManager

auth = AuthManager()
token = auth.authenticate_local(username, password)
user = auth.get_session_user(token)
```

#### LocalAuth
- **Responsabilidad**: Autenticación con usuario/contraseña local
- **Seguridad**:
  - Contraseñas hasheadas con SHA-256
  - Datos encriptados con Fernet (AES)
  - Archivos con permisos restringidos (600)

#### GitHubAuth / GoogleAuth
- **Responsabilidad**: OAuth 2.0 para GitHub/Google
- **Flujo**:
  1. Generar URL de autorización
  2. Usuario autoriza en navegador
  3. Intercambiar código por token
  4. Obtener información del usuario

### 3. Sensors (Sensores)

Todos heredan de `SensorBase` e implementan el mismo patrón:

#### PortSensor
- **Monitorea**: Puertos abiertos y conexiones de red
- **Detecta**:
  - Puertos peligrosos (Telnet, SMB, RDP)
  - Puertos inusuales
  - Alto número de conexiones

#### ProcessSensor
- **Monitorea**: Procesos en ejecución
- **Detecta**:
  - Procesos con nombres sospechosos
  - Alto uso de CPU/memoria
  - Sobrecarga del sistema

#### DiskSensor
- **Monitorea**: Espacio en disco y particiones
- **Detecta**:
  - Espacio crítico (>90%)
  - Advertencia de espacio bajo (>80%)
  - Menos de 1GB libre

#### LogSensor
- **Monitorea**: Logs del sistema
- **Detecta**:
  - Patrones sospechosos
  - Intentos de autenticación fallidos
  - Eventos de seguridad

**Implementación de Sensor:**
```python
def run(self) -> Dict[str, Any]:
    """Plantilla de ejecución"""
    scan_results = self.scan()      # 1. Escanear
    alerts = self.analyze(scan_results)  # 2. Analizar
    return {
        "sensor": self.name,
        "status": "success",
        "scan_results": scan_results,
        "alerts": alerts
    }
```

### 4. AI (Inteligencia Artificial)

#### AnomalyDetector
- **Responsabilidad**: Detectar comportamientos anómalos
- **Método actual**: Análisis estadístico (media ± 2σ)
- **Futuro**: Integración de modelos ML/DL

```python
from fireguard.ai import AnomalyDetector

detector = AnomalyDetector()
detector.enable()

# Recopilar historial
detector.add_metrics({"cpu_percent": 45.2, "memory_percent": 60.1})

# Detectar anomalías
anomalies = detector.detect_anomalies(current_metrics)
```

#### AlertSystem
- **Responsabilidad**: Gestión centralizada de alertas
- **Características**:
  - Niveles de severidad (low, medium, high, critical)
  - Umbrales configurables
  - Sistema de callbacks para notificaciones

```python
from fireguard.ai import AlertSystem

alerts = AlertSystem()
alerts.add_alert({
    "severity": "high",
    "type": "security_event",
    "message": "Evento detectado"
})
```

### 5. CLI (Interfaz de Línea de Comandos)

Construido con Click, proporciona comandos para todas las operaciones:

- `info` - Información del sistema
- `scan` - Ejecutar sensores
- `auth` - Autenticación
- `report` - Generar reportes
- `config` - Ver configuración

## Flujo de Ejecución

### Escaneo Completo

```
1. Usuario ejecuta: fireguard scan
           ↓
2. CLI inicializa:
   - ConfigManager
   - Logger
   - AlertSystem
           ↓
3. Para cada sensor habilitado:
   a. Sensor.scan() → Recopila datos
   b. Sensor.analyze() → Detecta anomalías
   c. Genera alertas
           ↓
4. AlertSystem agrega alertas
           ↓
5. CLI muestra resultados
```

### Autenticación

```
1. Usuario intenta autenticarse
           ↓
2. AuthManager recibe credenciales
           ↓
3. Según método seleccionado:
   - Local: LocalAuth.authenticate()
   - GitHub: GitHubAuth.authenticate()
   - Google: GoogleAuth.authenticate()
           ↓
4. Si exitoso:
   - Genera token de sesión
   - Almacena en memoria
   - Configura expiración
           ↓
5. Retorna token al usuario
```

## Patrones de Diseño

### Singleton
- **Usado en**: Logger
- **Razón**: Una sola instancia de logger para toda la aplicación

### Template Method
- **Usado en**: SensorBase
- **Razón**: Define estructura común, implementación específica en subclases

### Strategy
- **Usado en**: AuthManager
- **Razón**: Diferentes estrategias de autenticación intercambiables

### Observer (preparado)
- **Usado en**: AlertSystem (callbacks)
- **Razón**: Notificaciones a múltiples observadores

## Extensibilidad

### Añadir un Nuevo Sensor

1. Crear clase heredando de `SensorBase`
2. Implementar métodos `scan()` y `analyze()`
3. Registrar en `fireguard/sensors/__init__.py`
4. Añadir configuración en `config.yaml`

```python
# fireguard/sensors/mi_sensor.py
from fireguard.core.sensor_base import SensorBase

class MiSensor(SensorBase):
    def __init__(self, config=None):
        super().__init__("MiSensor", config)
    
    def scan(self):
        # Tu lógica de escaneo
        return {"resultado": "datos"}
    
    def analyze(self, scan_results):
        # Tu lógica de análisis
        alerts = []
        # Detectar problemas y añadir a alerts
        return alerts
```

### Añadir Método de Autenticación

1. Crear clase en `fireguard/auth/`
2. Implementar método `authenticate()`
3. Integrar en `AuthManager`
4. Añadir configuración

### Integrar Modelo de IA

1. Extender `AnomalyDetector`
2. Cargar modelo pre-entrenado
3. Implementar predicción en `detect_anomalies()`
4. Configurar umbrales

```python
class MLAnomalyDetector(AnomalyDetector):
    def __init__(self, config, model_path):
        super().__init__(config)
        self.model = load_model(model_path)
    
    def detect_anomalies(self, metrics):
        prediction = self.model.predict(metrics)
        # Procesar predicción
        return anomalies
```

## Consideraciones de Seguridad

### Datos Sensibles
- Contraseñas: Hasheadas con SHA-256
- Tokens: Generados con `secrets.token_urlsafe()`
- Datos encriptados: Fernet (AES)

### Archivos Protegidos
- `config/.key`: Permisos 600
- `config/users.json`: Permisos 600
- Excluidos del control de versiones

### Validación
- Validación de entrada en CLI
- Timeouts en sesiones
- Limpieza de sesiones expiradas

## Dependencias

### Principales
- `psutil`: Información del sistema
- `pyyaml`: Configuración
- `click`: CLI
- `cryptography`: Encriptación
- `requests`: OAuth

### Desarrollo
- `pytest`: Testing
- `pytest-cov`: Cobertura

## Rendimiento

### Optimizaciones
- Sensores ejecutan en paralelo cuando es posible
- Cache de configuración
- Singleton para logger
- Limpieza periódica de historial

### Recursos
- CPU: Bajo impacto (<5% en idle)
- Memoria: ~50-100MB típico
- Disco: Logs rotan diariamente

## Roadmap Futuro

### Corto Plazo
- [ ] Más sensores (red, firewall, antimalware)
- [ ] API REST para integración
- [ ] Dashboard web

### Medio Plazo
- [ ] Modelos de ML pre-entrenados
- [ ] Detección de amenazas en tiempo real
- [ ] Notificaciones (email, Slack, etc.)

### Largo Plazo
- [ ] Clustering para análisis distribuido
- [ ] IA generativa para análisis de logs
- [ ] Respuesta automática a incidentes

## Contribuir

Para contribuir a la arquitectura:

1. Mantener patrones de diseño consistentes
2. Documentar nuevos componentes
3. Seguir estructura modular
4. Añadir tests unitarios
5. Actualizar diagramas de arquitectura

---

Para más información técnica, consulta el código fuente ampliamente documentado.
