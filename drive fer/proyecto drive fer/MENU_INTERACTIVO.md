## 📧 Menú Interactivo de Selección de Gmail

El proyecto ahora incluye un **menú interactivo** para seleccionar la cuenta de Gmail que deseas conectar antes de ejecutar el scheduler.

### 🚀 Uso Básico

```bash
cd "proyecto drive fer"
python main.py
```

**Esto abrirá el menú interactivo que te preguntará:**

1. **Cuentas guardadas** - Muestra cuentas previamente guardadas
2. **Agregar nueva cuenta** - Para registrar una nueva cuenta de Gmail
3. **Gestionar cuentas** - Editar/eliminar cuentas guardadas

### 📝 Opciones del Menú

#### Opción 1: Usar Cuenta Guardada
Si ya tienes cuentas guardadas, selecciona una del listado:
```
📌 SAVED ACCOUNTS:
  1. personal@gmail.com (Personal)
  2. work@gmail.com (Work)
  3. ➕ Add New Account
  4. ❌ Exit
```

#### Opción 2: Agregar Nueva Cuenta
Al seleccionar "Agregar Nueva Cuenta", se te pedirá:
1. **Email de Gmail**: `correo@gmail.com`
2. **Nombre/Descripción**: `Personal`, `Work`, `Empresa`, etc.
3. **Ruta del archivo de credenciales**: Ruta al archivo JSON de Google Cloud

El menú **guarda automáticamente** la cuenta para futuras ejecuciones.

### 🛠️ Ejecución Avanzada

Si quieres **saltarte el menú** y usar directamente un archivo de credenciales:

```bash
python main.py /ruta/a/credenciales.json
```

### 📁 Archivo de Configuración

Las cuentas guardadas se guardan en: `.gmail_accounts.json`

Contenido de ejemplo:
```json
[
  {
    "email": "personal@gmail.com",
    "name": "Personal",
    "credentials_path": "/home/user/creds_personal.json",
    "created_at": "2026-07-18T10:30:00"
  },
  {
    "email": "work@gmail.com",
    "name": "Work",
    "credentials_path": "/home/user/creds_work.json",
    "created_at": "2026-07-18T11:00:00"
  }
]
```

### ✨ Características

- ✅ **Interfaz amigable** con emojis y colores
- ✅ **Validación de entrada** - Verifica emails y rutas de archivos
- ✅ **Guardado persistente** - Recuerda tus cuentas
- ✅ **Gestión de cuentas** - Agregar, ver y eliminar cuentas
- ✅ **Flexible** - Acepta argumentos de línea de comandos también

### 🔧 Gestión de Cuentas

Para acceder a las opciones de gestión (desde el código):

```python
from menu import GmailAccountSelector

selector = GmailAccountSelector()
selector.manage_accounts()  # Interfaz interactiva para editar
```

### 📋 Requisitos

Las dependencias ya están incluidas en `requirements.txt`:
- google-api-python-client
- google-auth
- google-auth-oauthlib
- google-auth-httplib2

### ❓ Troubleshooting

**Problema**: "No saved accounts found"
- **Solución**: Agrega una nueva cuenta la primera vez

**Problema**: "File not found: ..."
- **Solución**: Verifica que la ruta del archivo de credenciales sea correcta

**Problema**: "Invalid email format"
- **Solución**: Asegúrate de ingresar un email válido (ej: user@gmail.com)

---

**Creado**: 2026-07-18
**Módulo**: `menu.py`
**Integrado en**: `main.py`
