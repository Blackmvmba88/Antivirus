# 🔐 Guía de Autenticación - FIREGUARD AI

FIREGUARD soporta múltiples métodos de autenticación para garantizar la seguridad de tu sistema.

## Métodos de Autenticación

### 1. Autenticación Local

Sistema de usuario y contraseña almacenado localmente.

#### Uso desde CLI

```bash
fireguard auth
# Seleccionar opción 1
# Ingresar usuario: admin
# Ingresar contraseña: fireguard2024
```

#### Uso Programático

```python
from fireguard.auth import AuthManager

auth_manager = AuthManager()

# Autenticar
token = auth_manager.authenticate_local("admin", "fireguard2024")

if token:
    print(f"Token de sesión: {token}")
    
    # Validar sesión
    if auth_manager.validate_session(token):
        print("Sesión válida")
        
        # Obtener info del usuario
        user_info = auth_manager.get_session_user(token)
        print(f"Usuario: {user_info['username']}")
        print(f"Rol: {user_info['role']}")
    
    # Cerrar sesión
    auth_manager.logout(token)
```

#### Gestión de Usuarios Locales

```python
from fireguard.auth import LocalAuth

local_auth = LocalAuth()

# Crear nuevo usuario
local_auth.create_user("nuevo_usuario", "contraseña_segura", role="user")

# Cambiar contraseña
local_auth.change_password("nuevo_usuario", "contraseña_segura", "nueva_contraseña")

# Eliminar usuario
local_auth.delete_user("nuevo_usuario")

# Obtener rol
role = local_auth.get_user_role("admin")
```

#### Seguridad

- Las contraseñas se hashean con SHA-256
- Los datos sensibles se encriptan con Fernet
- Los archivos de usuarios tienen permisos restringidos (600)
- La clave de encriptación se genera automáticamente

### 2. GitHub OAuth

Autenticación usando cuenta de GitHub.

#### Configuración

1. Crear una OAuth App en GitHub:
   - Ir a: https://github.com/settings/developers
   - Click en "New OAuth App"
   - Authorization callback URL: `http://localhost:8080/callback`
   - Copiar Client ID y Client Secret

2. Configurar en `config/config.yaml`:

```yaml
auth:
  github:
    client_id: "tu_client_id"
    client_secret: "tu_client_secret"
```

#### Uso Programático

```python
from fireguard.auth import GitHubAuth
import webbrowser

github_auth = GitHubAuth(
    client_id="tu_client_id",
    client_secret="tu_client_secret"
)

# Generar URL de autorización
redirect_uri = "http://localhost:8080/callback"
state = "random_state_string"
auth_url = github_auth.get_authorization_url(redirect_uri, state)

# Abrir navegador para autenticación
webbrowser.open(auth_url)

# Después de que el usuario autorice, obtendrás un 'code'
# Intercambiar código por token
code = "codigo_de_github"
user_info = github_auth.authenticate(code, redirect_uri)

if user_info:
    print(f"Usuario: {user_info['username']}")
    print(f"Email: {user_info['email']}")
```

### 3. Google OAuth

Autenticación usando cuenta de Google.

#### Configuración

1. Crear credenciales OAuth en Google Cloud Console:
   - Ir a: https://console.cloud.google.com/apis/credentials
   - Crear nuevo proyecto (si es necesario)
   - Crear credenciales OAuth 2.0
   - Authorized redirect URIs: `http://localhost:8080/callback`
   - Copiar Client ID y Client Secret

2. Configurar en `config/config.yaml`:

```yaml
auth:
  google:
    client_id: "tu_client_id"
    client_secret: "tu_client_secret"
```

#### Uso Programático

```python
from fireguard.auth import GoogleAuth
import webbrowser

google_auth = GoogleAuth(
    client_id="tu_client_id",
    client_secret="tu_client_secret"
)

# Generar URL de autorización
redirect_uri = "http://localhost:8080/callback"
state = "random_state_string"
auth_url = google_auth.get_authorization_url(redirect_uri, state)

# Abrir navegador para autenticación
webbrowser.open(auth_url)

# Después de que el usuario autorice, obtendrás un 'code'
code = "codigo_de_google"
user_info = google_auth.authenticate(code, redirect_uri)

if user_info:
    print(f"Usuario: {user_info['username']}")
    print(f"Email: {user_info['email']}")
```

## Gestión de Sesiones

### Configuración de Sesiones

```yaml
security:
  require_authentication: true
  session_timeout: 3600  # segundos (1 hora)
```

### Uso de Sesiones

```python
from fireguard.auth import AuthManager

auth_manager = AuthManager()

# Crear sesión
token = auth_manager.authenticate_local("admin", "password")

# Validar sesión
is_valid = auth_manager.validate_session(token)

# Obtener usuario de la sesión
user = auth_manager.get_session_user(token)

# Cerrar sesión
auth_manager.logout(token)

# Limpiar sesiones expiradas
auth_manager.cleanup_expired_sessions()

# Obtener número de sesiones activas
active_sessions = auth_manager.get_active_sessions_count()
```

## Mejores Prácticas de Seguridad

### 1. Credenciales por Defecto

⚠️ **CRÍTICO**: Cambiar inmediatamente las credenciales por defecto:

```python
from fireguard.auth import LocalAuth

local_auth = LocalAuth()

# Cambiar contraseña del admin
local_auth.change_password("admin", "fireguard2024", "tu_contraseña_segura")
```

### 2. Contraseñas Seguras

- Mínimo 12 caracteres
- Incluir mayúsculas, minúsculas, números y símbolos
- No reutilizar contraseñas
- Usar gestor de contraseñas

### 3. Tokens de Sesión

- Nunca compartir tokens
- Renovar tokens regularmente
- Cerrar sesiones al terminar
- Limpiar sesiones expiradas periódicamente

### 4. OAuth

- Usar HTTPS en producción
- Validar el parámetro `state` para prevenir CSRF
- Renovar tokens regularmente
- Revocar acceso cuando no se necesite

### 5. Almacenamiento

- Los archivos de usuarios se guardan en `config/users.json` (permisos 600)
- La clave de encriptación se guarda en `config/.key` (permisos 600)
- **NO** commits estos archivos al control de versiones
- Backup de usuarios de forma segura

### 6. Logs de Seguridad

Los intentos de autenticación se registran en los logs:

```python
from fireguard.core import Logger

logger = Logger()
logger.set_level("INFO")  # Para logs de autenticación
```

## Desactivar Autenticación (Solo Desarrollo)

⚠️ Solo para desarrollo/testing:

```yaml
security:
  require_authentication: false
```

## Ejemplo Completo de Flujo de Autenticación

```python
from fireguard.auth import AuthManager
from fireguard.core import ConfigManager

# Inicializar
config = ConfigManager()
auth_manager = AuthManager(config)

# Autenticar usuario
username = input("Usuario: ")
password = input("Contraseña: ")

token = auth_manager.authenticate_local(username, password)

if token:
    print("✓ Autenticación exitosa")
    
    # Verificar permisos
    user_info = auth_manager.get_session_user(token)
    
    if user_info['role'] == 'admin':
        print("✓ Permisos de administrador")
        # Ejecutar operaciones administrativas
    else:
        print("✓ Permisos de usuario estándar")
        # Ejecutar operaciones normales
    
    # Al finalizar
    auth_manager.logout(token)
    print("✓ Sesión cerrada")
else:
    print("✗ Autenticación fallida")
```

## Solución de Problemas

### Error: "Usuario no encontrado"

Verificar que el archivo `config/users.json` existe y contiene usuarios.

### Error: "Permission denied" en archivos de configuración

```bash
chmod 600 config/users.json
chmod 600 config/.key
```

### OAuth no funciona

1. Verificar Client ID y Client Secret
2. Verificar redirect URI configurada correctamente
3. Comprobar conectividad a internet
4. Revisar logs para más detalles

---

Para más información, consulta la [documentación principal](../README.md).
