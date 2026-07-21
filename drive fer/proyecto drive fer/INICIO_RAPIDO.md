# PROJECT SCHEDULER
# Sistema de Gestión de Planificación de Proyectos
# Version 1.0.0
# 2026-07-17

## DESCRIPCIÓN GENERAL

Este es un **sistema automatizado en Python** para gestionar proyectos de múltiples departamentos
utilizando Google Drive y Google Sheets. Fue diseñado para empresas con tres departamentos 
independientes: Ingeniería, Obras y Mantenimiento.

## CARACTERÍSTICAS PRINCIPALES

✅ **Gestión Automática de Carpetas**
   - Crea estructura de carpetas en Google Drive
   - Organiza por departamento y cliente
   - Automatiza la creación inicial

✅ **Cronogramas Integrados**
   - Un Google Sheet por departamento
   - Consolidación en "Cronograma Maestro"
   - Seguimiento en tiempo real

✅ **Sistema de Alertas**
   - Monitoreo de correos de solicitud
   - Alertas de plazos próximos
   - Registro de eventos

✅ **Reportes Automáticos**
   - Reporte diario de proyectos
   - Exportación a CSV
   - Análisis consolidado

## ESTRUCTURA DEL PROYECTO

```
project_scheduler/
├── main.py                      # Aplicación principal
├── config.py                    # Configuración centralizada
├── quickstart.py                # Verificación rápida
├── test_suite.py                # Suite de pruebas
├── requirements.txt             # Dependencias
├── .env.example                 # Plantilla de variables
│
├── modules/
│   ├── drive_manager.py         # Gestión de Drive
│   ├── sheets_manager.py        # Gestión de Sheets
│   ├── scheduler_manager.py     # Cronogramas
│   └── notifications.py         # Alertas
│
├── examples/
│   ├── example_1_setup.py       # Ejemplo 1: Setup
│   ├── example_2_reports.py     # Ejemplo 2: Reportes
│   ├── example_3_notifications.py # Ejemplo 3: Alertas
│   └── example_4_export.py      # Ejemplo 4: Exportar
│
├── logs/                        # Archivos de log
├── README.md                    # Documentación completa
├── SETUP.md                     # Guía de configuración
└── .gitignore                   # Archivos a ignorar
```

## REQUISITOS

- Python 3.8 o superior
- Cuenta de Google Cloud
- APIs habilitadas: Drive, Sheets, Gmail (opcional)
- Credenciales de servicio (JSON)

## INSTALACIÓN RÁPIDA

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Obtener credenciales de Google Cloud:**
   - Ve a https://console.cloud.google.com/
   - Crea un proyecto
   - Habilita Drive API, Sheets API, Gmail API
   - Crea una cuenta de servicio
   - Descarga el JSON como `credentials.json`

3. **Verificar configuración:**
   ```bash
   python quickstart.py
   ```

4. **Ejecutar aplicación:**
   ```bash
   python main.py
   ```

5. **Probar con ejemplos:**
   ```bash
   python examples/example_1_setup.py
   ```

## DOCUMENTACIÓN

- **README.md** - Documentación completa y API
- **SETUP.md** - Guía paso a paso de configuración
- **examples/** - 4 ejemplos prácticos de uso
- **Código comentado** - Cada módulo tiene docstrings detallados

## CARACTERÍSTICAS TÉCNICAS

### Módulos Disponibles

**DriveManager**
- Crear carpetas
- Listar carpetas
- Compartir acceso
- Crear estructura departamental

**SheetsManager**
- Crear spreadsheets
- Escribir/leer datos
- Formatear celdas
- Crear hojas nuevas

**SchedulerManager**
- Gestionar proyectos
- Consolidar cronogramas
- Exportar a CSV
- Generar resúmenes

**NotificationManager**
- Monitorear correos
- Detectar deadlines
- Registrar eventos
- Generar alertas

### Dependencias Principales

```
google-api-python-client==2.104.0
google-auth==2.27.0
pandas==2.1.4
python-dotenv==1.0.0
```

## FLUJO DE TRABAJO TÍPICO

```
1. INICIALIZACIÓN
   └─ python main.py
      ├─ Crea carpetas en Drive
      ├─ Crea Sheets por departamento
      └─ Crea Cronograma Maestro

2. AGREGAR PROYECTOS
   └─ scheduler.add_project_to_department(dept, project_data)

3. CONSOLIDAR
   └─ scheduler.consolidate_master_schedule()

4. MONITOREAR
   └─ scheduler.check_approaching_deadlines()
   └─ scheduler.check_service_requests()

5. REPORTAR
   └─ scheduler.generate_schedules_report()
```

## CONFIGURACIÓN DE PROYECTOS

Cada proyecto requiere estos campos:

```python
{
    'id': 'PRY-DEPT-001',           # ID único
    'client': 'Nombre Cliente',      # Cliente
    'description': 'Descripción',    # Qué es
    'start_date': '2026-07-20',     # Inicio (YYYY-MM-DD)
    'end_date': '2026-08-20',       # Fin (YYYY-MM-DD)
    'status': 'En Progreso',        # Estado
    'responsible': 'Nombre',        # Responsable
    'budget': '$50,000',            # Presupuesto
    'progress': 50,                 # Progreso (%)
    'notes': 'Observaciones'        # Notas
}
```

## VARIABLES DE ENTORNO

```env
# Credenciales
GOOGLE_APPLICATION_CREDENTIALS=./credentials.json

# Carpetas y Sheets
ROOT_FOLDER_ID=...
ENGINEERING_FOLDER_ID=...
ENGINEERING_SHEET_ID=...
OBRAS_FOLDER_ID=...
OBRAS_SHEET_ID=...
MAINTENANCE_FOLDER_ID=...
MAINTENANCE_SHEET_ID=...
MASTER_SCHEDULE_SHEET_ID=...

# Notificaciones
NOTIFICATION_EMAIL=tu_email@gmail.com
MONITOR_INBOX=true
INBOX_POLL_INTERVAL=300

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/project_scheduler.log
```

## SEGURIDAD

⚠️ **IMPORTANTE:**
- Nunca compartas `credentials.json`
- Nunca commits `.env` a control de versiones
- La carpeta en Drive debe ser compartida solo con la cuenta de servicio
- Usa variables de entorno en producción

## EXPANSIONES FUTURAS

El código está diseñado para ser escalable. Puedes:

- ✅ Agregar nuevos departamentos (edita config.py)
- ✅ Crear reportes personalizados (extiende SchedulerManager)
- ✅ Integrar webhooks (usa Google Drive API webhooks)
- ✅ Agregar autenticación de usuario (crea auth_manager.py)
- ✅ Conectar con otras plataformas (crea nuevos managers)

## TROUBLESHOOTING

**Problema:** `credentials.json not found`
**Solución:** Descarga el JSON desde Google Cloud Console y guárdalo en la carpeta raíz

**Problema:** `Permission denied`
**Solución:** Comparte la carpeta de Drive con el email del servicio (client_email en JSON)

**Problema:** `API not enabled`
**Solución:** Ve a Google Cloud Console y habilita las APIs en Library

**Problema:** Los datos no aparecen en Sheets
**Solución:** Verifica que los IDs en .env son correctos

## SOPORTE Y AYUDA

1. Lee **README.md** para documentación completa
2. Lee **SETUP.md** para instrucciones paso a paso
3. Ejecuta **quickstart.py** para verificar configuración
4. Revisa **logs/project_scheduler.log** para detalles de errores
5. Consulta los **examples/** para casos de uso

## LICENCIA

Este proyecto se proporciona como está, sin garantías.

## VERSIÓN

- Versión: 1.0.0
- Fecha: 2026-07-17
- Python: 3.8+

---

## PRÓXIMOS PASOS

1. ✓ Lee SETUP.md para configuración completa
2. ✓ Ejecuta quickstart.py para verificar todo
3. ✓ Descarga credenciales de Google Cloud
4. ✓ Ejecuta python main.py
5. ✓ Prueba los ejemplos en examples/
6. ✓ Comienza a usar con tus departamentos

¡Listo para automatizar tu gestión de proyectos!
