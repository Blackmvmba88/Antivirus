# 🚀 Guía de Inicio Rápido - FIREGUARD AI

Esta guía te ayudará a poner en marcha FIREGUARD AI en minutos.

## Instalación Rápida

### Linux / macOS

```bash
# 1. Clonar el repositorio
git clone https://github.com/Blackmvmba88/Antivirus.git
cd Antivirus

# 2. Crear entorno virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Instalar FIREGUARD
pip install -e .

# 5. ¡Listo! Ejecutar primer escaneo
fireguard info
fireguard scan
```

### Windows

```cmd
REM 1. Clonar el repositorio
git clone https://github.com/Blackmvmba88/Antivirus.git
cd Antivirus

REM 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate

REM 3. Instalar dependencias
pip install -r requirements.txt

REM 4. Instalar FIREGUARD
pip install -e .

REM 5. Ejecutar primer escaneo
fireguard info
fireguard scan
```

### Android (Termux)

```bash
# 1. Instalar Termux desde F-Droid o Play Store

# 2. Actualizar paquetes
pkg update && pkg upgrade

# 3. Instalar dependencias del sistema
pkg install python git build-essential

# 4. Clonar y instalar
git clone https://github.com/Blackmvmba88/Antivirus.git
cd Antivirus
pip install -r requirements.txt
pip install -e .

# 5. Ejecutar
fireguard info
fireguard scan
```

## Primeros Pasos

### 1. Información del Sistema

```bash
fireguard info
```

Muestra información sobre tu plataforma y características soportadas.

### 2. Escaneo Básico

```bash
# Escaneo completo (todos los sensores)
fireguard scan

# Escaneo de puertos solamente
fireguard scan --sensor ports

# Escaneo de procesos
fireguard scan --sensor processes
```

### 3. Autenticación

```bash
fireguard auth
```

Por defecto, usa:
- Usuario: `admin`
- Contraseña: `fireguard2024`

⚠️ **¡Cámbialo inmediatamente en producción!**

### 4. Generar Reporte

```bash
# Reporte en pantalla
fireguard report

# Guardar reporte en archivo
fireguard report --output reporte_seguridad.json
```

## Uso Básico Programático

```python
# ejemplo_basico.py
from fireguard.sensors import PortSensor, ProcessSensor
from fireguard.core import ConfigManager

# Inicializar
config = ConfigManager()

# Escanear puertos
port_sensor = PortSensor(config)
result = port_sensor.run()

print(f"Alertas encontradas: {result['alert_count']}")

for alert in result['alerts']:
    print(f"- [{alert['severity']}] {alert['message']}")
```

## Configuración Básica

Edita `config/config.yaml`:

```yaml
monitoring:
  enabled: true
  interval: 60  # Escanear cada 60 segundos

alerts:
  threshold: "medium"  # Solo alertas medium, high y critical

security:
  require_authentication: true
```

## Próximos Pasos

1. 📖 Lee la [Documentación Completa](README.md)
2. 🔧 Configura [Autenticación OAuth](docs/AUTHENTICATION.md)
3. 🎨 Personaliza tus [Sensores](docs/SENSORS.md)
4. 🤖 Explora las [Capacidades de IA](docs/AI.md)

## Solución de Problemas

### Error: "No module named 'fireguard'"

```bash
# Asegúrate de haber instalado el paquete
pip install -e .
```

### Error: "Permission denied" en logs

En Linux, algunos logs requieren permisos elevados:

```bash
sudo fireguard scan --sensor logs
```

### Error en Termux: "Cannot compile native extensions"

```bash
# Instalar herramientas de compilación
pkg install build-essential
```

## Ayuda

```bash
# Ayuda general
fireguard --help

# Ayuda de un comando específico
fireguard scan --help
```

---

¿Necesitas más ayuda? Consulta la [documentación completa](README.md) o abre un issue en GitHub.
