# Guía de Configuración - Project Scheduler

Esta guía te ayudará a configurar completamente el sistema Project Scheduler para tu empresa.

## Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Crear Proyecto en Google Cloud](#crear-proyecto-en-google-cloud)
3. [Habilitar APIs](#habilitar-apis)
4. [Crear Credenciales de Servicio](#crear-credenciales-de-servicio)
5. [Configuración Local](#configuración-local)
6. [Verificar la Configuración](#verificar-la-configuración)
7. [Solución de Problemas](#solución-de-problemas)

## Requisitos Previos

- Cuenta de Google activa
- Acceso a [Google Cloud Console](https://console.cloud.google.com/)
- Python 3.8+ instalado en tu computadora
- Acceso a línea de comandos (Terminal/CMD)

## Crear Proyecto en Google Cloud

### Paso 1: Acceder a Google Cloud Console

1. Abre [Google Cloud Console](https://console.cloud.google.com/)
2. Inicia sesión con tu cuenta de Google

### Paso 2: Crear un Nuevo Proyecto

1. En la barra superior, haz clic en el selector de proyectos
2. Haz clic en "NEW PROJECT"
3. Introduce el nombre: `Project Scheduler`
4. Haz clic en "CREATE"

### Paso 3: Seleccionar el Proyecto

Una vez creado, selecciona el proyecto recién creado desde el selector de proyectos.

## Habilitar APIs

### Método 1: A través del Console (Recomendado)

1. En Google Cloud Console, abre el menú principal (≡)
2. Ve a "APIs & Services" → "Library"
3. Busca y habilita cada API:

#### Google Drive API
1. Busca "Google Drive API"
2. Haz clic en el resultado
3. Haz clic en "ENABLE"
4. Espera a que se complete

#### Google Sheets API
1. Busca "Google Sheets API"
2. Haz clic en el resultado
3. Haz clic en "ENABLE"
4. Espera a que se complete

#### Gmail API (Opcional - para monitoreo de correos)
1. Busca "Gmail API"
2. Haz clic en el resultado
3. Haz clic en "ENABLE"
4. Espera a que se complete

### Verificar que las APIs están Habilitadas

1. Ve a "APIs & Services" → "Enabled APIs & services"
2. Deberías ver:
   - Google Drive API ✓
   - Google Sheets API ✓
   - Gmail API ✓ (opcional)

## Crear Credenciales de Servicio

### Paso 1: Crear una Cuenta de Servicio

1. Ve a "APIs & Services" → "Credentials"
2. Haz clic en "+ CREATE CREDENTIALS" (botón azul)
3. Selecciona "Service Account"
4. Completa el formulario:
   - **Service account name:** `project-scheduler`
   - **Description:** `Gestor automático de proyectos`
5. Haz clic en "CREATE AND CONTINUE"

### Paso 2: Asignar Roles

1. En "Grant this service account access to project":
   - Selecciona el rol: **Editor**
   - Haz clic en "CONTINUE"
2. Haz clic en "DONE"

### Paso 3: Crear Clave JSON

1. En "Service Accounts", haz clic en el email de la cuenta creada
2. Ve al tab "Keys"
3. Haz clic en "Add Key" → "Create new key"
4. Selecciona "JSON"
5. Haz clic en "CREATE"
6. Se descargará un archivo JSON automáticamente
   - Guárdalo en un lugar seguro

### Paso 4: Preparar el Archivo de Credenciales

1. Descargaste un archivo como `project-scheduler-xxxxx.json`
2. Copia este archivo a la carpeta raíz del proyecto
3. Renómbralo a `credentials.json`

**IMPORTANTE:** No compartas este archivo, contiene secretos de acceso.

## Configuración Local

### Paso 1: Preparar el Archivo .env

1. En la carpeta del proyecto, copia `.env.example` a `.env`:
   ```bash
   cp .env.example .env
   ```

2. Abre `.env` en un editor de texto

### Paso 2: Configurar Rutas de Credenciales

Asegúrate de que la primera línea sea:
```
GOOGLE_APPLICATION_CREDENTIALS=./credentials.json
```

### Paso 3: Crear Carpeta Raíz en Google Drive (Opcional)

Si prefieres especificar la carpeta raíz:

1. Abre [Google Drive](https://drive.google.com)
2. Crea una nueva carpeta llamada "Gestión de Proyectos"
3. Copia el ID de la carpeta desde la URL:
   - URL: `https://drive.google.com/drive/folders/1a2b3c4d5e6f7g8h...`
   - ID: `1a2b3c4d5e6f7g8h...`

4. En `.env`, actualiza:
   ```
   ROOT_FOLDER_ID=1a2b3c4d5e6f7g8h...
   ```

Si dejas esto vacío, el sistema creará la carpeta automáticamente.

### Paso 4: Compartir Carpeta con Servicio (Importante)

1. Abre el archivo `credentials.json` en un editor
2. Busca la línea `"client_email"` y copia el valor
3. En Google Drive, comparte la carpeta raíz con este email:
   - Abre la carpeta
   - Haz clic en "Share"
   - Pega el email
   - Selecciona "Editor"
   - Haz clic en "Share"

## Instalación de Dependencias

```bash
# Desde la carpeta del proyecto
pip install -r requirements.txt
```

Esto instala:
- google-api-python-client
- google-auth
- pandas
- python-dotenv
- Y más...

## Verificar la Configuración

### Prueba 1: Verificar Credenciales

```bash
python -c "
from google.oauth2.service_account import Credentials
credentials = Credentials.from_service_account_file('./credentials.json')
print('✓ Credenciales válidas')
"
```

### Prueba 2: Ejecutar Aplicación

```bash
python main.py
```

**Primera ejecución:**
- Debería crear la estructura de carpetas
- Mostrar los IDs generados
- Crear los cronogramas

### Prueba 3: Verificar en Google Drive

1. Abre [Google Drive](https://drive.google.com)
2. Busca la carpeta "Gestión de Proyectos"
3. Verifica que contenga:
   - Carpeta "Ingeniería"
   - Carpeta "Obras"
   - Carpeta "Mantenimiento"
   - Archivo "Cronograma Maestro"

## Actualizar .env con IDs Generados

Después de la primera ejecución exitosa:

1. Copia los IDs mostrados en la consola
2. Edita `.env` y completa los campos:
   ```env
   ROOT_FOLDER_ID=1a2b3c...
   ENGINEERING_FOLDER_ID=1x2y3z...
   ENGINEERING_SHEET_ID=1abc2def...
   OBRAS_FOLDER_ID=1m2n3o...
   OBRAS_SHEET_ID=1pqr2stu...
   MAINTENANCE_FOLDER_ID=1v2w3x...
   MAINTENANCE_SHEET_ID=1yz1abc...
   MASTER_SCHEDULE_SHEET_ID=1def2ghi...
   ```

## Configuración de Notificaciones (Opcional)

Para habilitar monitoreo de correos:

1. En `.env`, actualiza:
   ```env
   NOTIFICATION_EMAIL=tu_email@gmail.com
   MONITOR_INBOX=true
   INBOX_POLL_INTERVAL=300
   ```

2. Comparte una carpeta de Google Drive con ese email

## Solución de Problemas

### Error: "FileNotFoundError: credentials.json not found"

**Causa:** El archivo no está en la ubicación correcta
**Solución:**
1. Verifica que `credentials.json` está en la carpeta raíz
2. Comprueba que el nombre es exactamente `credentials.json`
3. Verifica la ruta en `.env`

### Error: "Permission denied" o "Insufficient permissions"

**Causa:** La cuenta de servicio no tiene acceso a la carpeta
**Solución:**
1. Obtén el `client_email` de `credentials.json`
2. Comparte la carpeta de Google Drive con ese email como "Editor"
3. Espera 30 segundos y vuelve a intentar

### Error: "API not enabled"

**Causa:** Las APIs no están habilitadas
**Solución:**
1. Ve a Google Cloud Console
2. Busca la API en "Library"
3. Haz clic en "ENABLE"
4. Espera 1-2 minutos

### Error: "Invalid Google Credentials"

**Causa:** El archivo JSON está dañado o es incorrecto
**Solución:**
1. Ve a Google Cloud Console
2. Crea una nueva clave JSON
3. Reemplaza el archivo `credentials.json`

### Google Sheets no aparece en Drive

**Causa:** Permisos insuficientes o error en la API
**Solución:**
1. Verifica que Google Sheets API está habilitada
2. Comprueba los permisos de la carpeta raíz
3. Intenta ejecutar nuevamente

### Error: "Failed to authenticate"

**Causa:** Variables de entorno no configuradas correctamente
**Solución:**
1. Abre `.env` y verifica todas las rutas
2. Asegúrate de que no hay espacios extra
3. Verifica que `credentials.json` existe

## Configuración de Producción

Para usar en producción:

### 1. Usa Variables de Entorno del Sistema

En lugar de `.env`, configura:

```bash
# Linux/Mac
export GOOGLE_APPLICATION_CREDENTIALS=/ruta/a/credentials.json
export ROOT_FOLDER_ID=xxx
export ENGINEERING_FOLDER_ID=xxx
# etc...

# Windows (PowerShell)
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\ruta\a\credentials.json"
```

### 2. Almacena Credenciales de Forma Segura

- Usa Google Secret Manager
- Nunca incluyas credentials.json en control de versiones
- Limita acceso a la clave JSON

### 3. Configura Logging Adecuado

En `.env`:
```env
LOG_LEVEL=INFO
LOG_FILE=/var/log/project_scheduler/app.log
```

## Próximos Pasos

1. ✓ Ejecuta `python examples/example_1_setup.py` para agregar proyectos de prueba
2. ✓ Verifica los datos en Google Sheets
3. ✓ Ejecuta `python examples/example_2_reports.py` para generar reportes
4. ✓ Consulta el [README.md](README.md) para más uso

---

**¿Necesitas ayuda?** Revisa el archivo de log en `logs/project_scheduler.log` para mensajes detallados de error.

**Última actualización:** 2026-07-17
