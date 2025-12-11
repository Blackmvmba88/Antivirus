# Configuración de FIREGUARD AI

Este directorio contiene los archivos de configuración del sistema.

## Archivos

- `config.yaml` - Configuración principal del sistema
- `config.example.yaml` - Archivo de ejemplo con todas las opciones disponibles
- `users.json` - Base de datos de usuarios (generado automáticamente)
- `.key` - Clave de encriptación (generado automáticamente)

## Seguridad

⚠️ **IMPORTANTE**: Los siguientes archivos contienen información sensible y NO deben ser incluidos en control de versiones:

- `.key` - Clave de encriptación
- `users.json` - Base de datos de usuarios
- `secrets.json` - Credenciales OAuth (si se usa)
- `local.json` - Configuración local específica

Estos archivos están incluidos en `.gitignore` para tu seguridad.

## Configuración Inicial

Al iniciar FIREGUARD por primera vez, se generará automáticamente:

1. Un archivo `config.yaml` con configuración por defecto
2. Un archivo `.key` con la clave de encriptación
3. Un archivo `users.json` con el usuario administrador por defecto

## Usuario por Defecto

- **Usuario**: `admin`
- **Contraseña**: `fireguard2024`

⚠️ **DEBE cambiar estas credenciales inmediatamente** usando:

```python
from fireguard.auth import LocalAuth

local_auth = LocalAuth()
local_auth.change_password("admin", "fireguard2024", "tu_nueva_contraseña_segura")
```

## Personalizar Configuración

1. Copiar `config.example.yaml` a `config.yaml`
2. Editar `config.yaml` según tus necesidades
3. Reiniciar FIREGUARD para aplicar cambios

## Backup

Es recomendable hacer backup regular de:
- `config.yaml` - Tu configuración personalizada
- `users.json` - Base de datos de usuarios (si tienes usuarios importantes)

**NUNCA** comparta públicamente los archivos `.key` o `users.json`.
