# Project Scheduler - Sistema de Gestión de Planificación de Proyectos

Un sistema completo en Python para gestionar proyectos de tres departamentos independientes (Ingeniería, Obras, Mantenimiento) utilizando Google Drive y Google Sheets.

## Características

✅ **Gestión de Carpetas en Google Drive**
- Estructura automática de carpetas por departamento
- Subcarpetas para clientes
- Fácil compartición de acceso

✅ **Cronogramas en Google Sheets**
- Un cronograma independiente por departamento
- Cronograma maestro consolidado
- Seguimiento de proyectos en tiempo real

✅ **Notificaciones y Alertas**
- Monitoreo de solicitudes de servicio por correo
- Alertas de plazos próximos
- Registro de eventos y notificaciones

✅ **Reportes y Análisis**
- Reportes de estado de proyectos
- Exportación a CSV
- Resumen diario consolidado

✅ **Arquitectura Modular**
- Componentes reutilizables
- Fácil extensión y mantenimiento
- Separación de responsabilidades

## Estructura del Proyecto

```
project_scheduler/
├── main.py                          # Aplicación principal
├── config.py                        # Configuración centralizada
├── requirements.txt                 # Dependencias de Python
├── .env.example                     # Plantilla de variables de entorno
│
├── modules/
│   ├── __init__.py
│   ├── drive_manager.py             # Gestión de Google Drive
│   ├── sheets_manager.py            # Gestión de Google Sheets
│   ├── scheduler_manager.py         # Lógica de cronogramas
│   └── notifications.py             # Sistema de notificaciones
│
├── examples/
│   ├── example_1_setup.py           # Inicialización y agregar proyectos
│   ├── example_2_reports.py         # Generar reportes
│   ├── example_3_notifications.py   # Notificaciones y alertas
│   └── example_4_export.py          # Exportar datos
│
├── logs/
│   └── project_scheduler.log        # Archivo de registro
│
└── README.md                        # Este archivo
```

## Instalación

### Requisitos Previos

- Python 3.8+
- Cuenta de Google Cloud con APIs habilitadas
- Credenciales de servicio de Google Cloud (JSON)

### Paso 1: Clonar/Descargar el Proyecto

```bash
cd /ruta/del/proyecto
```

### Paso 2: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 3: Configurar Credenciales de Google Cloud

Consulta la sección **Configuración de Google Cloud** más abajo.

### Paso 4: Configurar Variables de Entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con tus IDs de Google Cloud
# (Después de la primera ejecución)
```

## Configuración de Google Cloud

### 1. Crear un Proyecto en Google Cloud Console

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto: `Project Scheduler`
3. Selecciona el proyecto

### 2. Habilitar APIs Requeridas

En "APIs & Services" → "Library", busca y habilita:
- **Google Drive API**
- **Google Sheets API**
- **Gmail API** (si usarás monitoreo de correos)

### 3. Crear Credenciales de Servicio

1. Ve a "APIs & Services" → "Credentials"
2. Haz clic en "Create Credentials" → "Service Account"
3. Completa la información del servicio
4. En el tab "Keys", crea una nueva clave JSON
5. Descarga el archivo JSON (se llamará algo como `project-scheduler-xxxxx.json`)
6. Renombra el archivo a `credentials.json` y colócalo en la raíz del proyecto

### 4. Compartir Google Drive con la Cuenta de Servicio

1. Abre el archivo `credentials.json` descargado
2. Copia el valor de `client_email`
3. Crea una carpeta en Google Drive (o usa una existente)
4. Comparte la carpeta con el email del servicio con permisos de **Editor**

## Primeros Pasos

### Ejecución Inicial

```bash
python main.py
```

La primera vez, el script:
1. ✓ Creará la estructura de carpetas en Google Drive
2. ✓ Creará los cronogramas de cada departamento
3. ✓ Creará el cronograma maestro
4. ✓ Mostrará los IDs necesarios para actualizar `.env`

**Importante:** Copia los IDs mostrados y actualiza tu archivo `.env`

### Actualizar .env con los IDs Generados

Después de la primera ejecución, actualiza `.env` con los IDs mostrados:

```env
ROOT_FOLDER_ID=1a2b3c4d5e6f7g8h...
ENGINEERING_FOLDER_ID=...
ENGINEERING_SHEET_ID=...
OBRAS_FOLDER_ID=...
OBRAS_SHEET_ID=...
MAINTENANCE_FOLDER_ID=...
MAINTENANCE_SHEET_ID=...
MASTER_SCHEDULE_SHEET_ID=...
```

## Uso

### Opción 1: Usar los Ejemplos Proporcionados

```bash
# Ejemplo 1: Configuración y agregar proyectos
python examples/example_1_setup.py

# Ejemplo 2: Generar reportes
python examples/example_2_reports.py

# Ejemplo 3: Notificaciones y alertas
python examples/example_3_notifications.py

# Ejemplo 4: Exportar datos
python examples/example_4_export.py
```

### Opción 2: Usar en tu Propio Código

```python
from main import ProjectScheduler
from datetime import datetime, timedelta

# Inicializar
scheduler = ProjectScheduler()

# Agregar un proyecto
project = {
    'id': 'PRY-ENG-001',
    'client': 'Mi Cliente',
    'description': 'Descripción del proyecto',
    'start_date': datetime.now().strftime('%Y-%m-%d'),
    'end_date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
    'status': 'En Progreso',
    'responsible': 'Nombre del responsable',
    'budget': '$50,000',
    'progress': 25,
    'notes': 'Notas adicionales'
}

scheduler.add_project_to_department('Ingeniería', project)

# Consolidar cronogramas
scheduler.consolidate_master_schedule()

# Generar reporte
report = scheduler.generate_schedules_report()
print(report)
```

## API Disponible

### ProjectScheduler

#### `setup_initial_structure()`
Configura la estructura inicial de carpetas y cronogramas.

#### `add_project_to_department(department, project_data)`
Agrega un nuevo proyecto a un departamento.
- `department`: 'Ingeniería', 'Obras' o 'Mantenimiento'
- `project_data`: Diccionario con información del proyecto

#### `consolidate_master_schedule()`
Consolida todos los cronogramas departamentales en el maestro.

#### `generate_schedules_report()`
Genera un reporte consolidado de todos los cronogramas.

#### `check_service_requests()`
Verifica el correo para solicitudes de servicio.

#### `check_approaching_deadlines(days_threshold=7)`
Identifica proyectos con plazos próximos.

#### `log_notification(notification_type, department, client, message, project_id=None)`
Registra una notificación en el log del sistema.

## Campos del Proyecto

Cada proyecto debe incluir los siguientes campos:

```python
{
    'id': 'PRY-DEPT-001',        # ID único del proyecto
    'client': 'Nombre del Cliente',
    'description': 'Descripción breve',
    'start_date': '2026-07-20',  # Formato: YYYY-MM-DD
    'end_date': '2026-08-20',    # Formato: YYYY-MM-DD
    'status': 'En Progreso',     # En Progreso, Completado, En Pausa, Planificación
    'responsible': 'Nombre responsable',
    'budget': '$50,000',
    'progress': 50,              # Porcentaje (0-100)
    'notes': 'Observaciones adicionales'
}
```

## Configuración Avanzada

### Cambiar Nivel de Logging

En `.env`:
```env
LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Intervalo de Monitoreo de Correos

En `.env`:
```env
INBOX_POLL_INTERVAL=300  # segundos
```

### Desactivar Monitoreo de Correos

En `.env`:
```env
MONITOR_INBOX=false
```

## Troubleshooting

### "FileNotFoundError: credentials.json"
- Verifica que el archivo `credentials.json` está en la carpeta raíz
- Asegúrate de que se descargó correctamente de Google Cloud Console

### "Permission denied" al acceder a Google Drive
- La carpeta debe estar compartida con el email del servicio
- El email debe tener permisos de **Editor**

### "Invalid Credentials"
- Verifica que la clave JSON no está corrupta
- Intenta descargar una nueva clave desde Google Cloud Console

### Los cronogramas no aparecen en Google Drive
- Verifica que las APIs están habilitadas
- Comprueba los permisos de la carpeta compartida

## Extensiones Futuras

El código está diseñado para ser modular y escalable. Puedes fácilmente:

- **Agregar nuevos departamentos:** Añade claves a `DEPARTMENTS` en `config.py`
- **Crear reportes personalizados:** Extiende `SchedulerManager`
- **Integrar con otras plataformas:** Usa los módulos base como referencia
- **Agregar autenticación de usuario:** Crea un módulo `auth_manager.py`
- **Implementar webhooks:** Monitorea cambios en tiempo real con Google Drive API webhooks

## Estructura de Carpetas en Google Drive

```
Gestión de Proyectos/
├── Ingeniería/
│   ├── Clientes/
│   └── Cronograma Ingeniería (Sheet)
├── Obras/
│   ├── Clientes/
│   └── Cronograma Obras (Sheet)
├── Mantenimiento/
│   ├── Clientes/
│   └── Cronograma Mantenimiento (Sheet)
└── Cronograma Maestro (Sheet)
```

## Logging

Todos los eventos se registran en `logs/project_scheduler.log`:
- Inicializaciones
- Creaciones de archivos
- Errores y excepciones
- Notificaciones

## Contribución y Mejoras

Para mejorar o extender el sistema:

1. Crea ramas específicas para cada feature
2. Mantén la estructura modular
3. Documenta cambios significativos
4. Prueba con múltiples escenarios

## Soporte

Para preguntas o problemas:
1. Revisa los archivos de ejemplo
2. Consulta el archivo de log (`logs/project_scheduler.log`)
3. Verifica la configuración de Google Cloud

## Licencia

Este proyecto se proporciona como está, sin garantías.

---

**Última actualización:** 2026-07-17
**Versión:** 1.0.0
