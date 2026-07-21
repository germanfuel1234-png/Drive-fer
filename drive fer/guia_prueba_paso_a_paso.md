# 🧪 Guía de Prueba Paso a Paso - Project Scheduler

> **Objetivo:** Ejecutar `main.py` por primera vez y verificar que crea correctamente la estructura de carpetas y Sheets en Google Drive.
> **Tiempo estimado:** 15-20 minutos.
> **Prerrequisitos:** Tener el proyecto descargado/clonado en tu computadora.

---

## 📋 Checklist de Prerrequisitos (Antes de empezar)

Antes de ejecutar la prueba, asegúrate de tener:

- [ ] **Python 3.8+** instalado (`python --version` o `python3 --version`)
- [ ] **pip** instalado (`pip --version`)
- [ ] Proyecto en tu disco: `/home/german/Escritorio/drive fer/project_scheduler/`
- [ ] Archivo `credentials.json` descargado de Google Cloud Console
- [ ] Archivo `.env` creado a partir de `.env.example`
- [ ] APIs de **Google Drive** y **Google Sheets** habilitadas en Google Cloud
- [ ] Cuenta de servicio creada con rol **Editor**
- [ ] Carpeta `Proyectos_Empresa` en tu Drive compartida con el email de la cuenta de servicio

> ⚠️ **Si te falta alguno de estos pasos,** ve a la guía de instalación (`guia_instalacion_v2_completa.md`) y complétalo primero.

---

## 🔧 Paso 0: Corregir el archivo `main.py` (IMPORTANTE)

Tu archivo `main.py` actual tiene **código duplicado** (dos versiones del programa en uno solo). Esto va a causar errores.

### 0.1 Verificar si tienes el problema

Abre `main.py` en VS Code y desplázate hacia abajo. Si ves que después de la clase `ProjectSchedulerApp` (línea ~169) sigue otra clase `ProjectScheduler` con otro `main()`, tienes código duplicado.

### 0.2 Aplicar la corrección

**Opción A: Reemplazar manualmente**

1. Abre `main.py` en VS Code
2. Selecciona TODO el contenido (`Ctrl + A`)
3. Borra todo
4. Pega el código corregido que te proporcionó tu asistente (o Copilot)
5. Guarda (`Ctrl + S`)

**Opción B: Usar el script de corrección automática**

Si tienes el archivo corregido en otra ubicación, copia y pega.

### 0.3 Verificar que quedó limpio

El archivo `main.py` corregido debe tener **exactamente**:
- Una clase `ProjectSchedulerApp`
- Un bloque `if __name__ == '__main__':` al final
- **NO** debe tener una segunda clase `ProjectScheduler`
- **NO** debe tener un segundo bloque `if __name__ == '__main__':`

> ✅ **Verificación rápida:** El archivo debe tener aproximadamente **250-300 líneas**, no 400+.

---

## 🧪 Paso 1: Verificar que `main.py` está limpio

Abre tu terminal y ejecuta:

```bash
cd "/home/german/Escritorio/drive fer/project_scheduler"

# Verificar que main.py existe y tiene tamaño razonable
ls -la main.py
```

**Resultado esperado:**
```
-rw-r--r-- 1 german german  ~8000 bytes  main.py
```

> Si el archivo pesa más de 15KB, probablemente sigue con código duplicado.

**Verificar que no hay código duplicado:**

```bash
# Contar cuántas veces aparece "class ProjectScheduler"
grep -c "class ProjectScheduler" main.py
```

**Resultado esperado:** `1`

> Si dice `2`, aún tienes código duplicado. Repite el Paso 0.

---

## 🧪 Paso 2: Verificar archivos necesarios

### 2.1 Verificar `credentials.json`

```bash
ls -la credentials.json
```

**Resultado esperado:**
```
-rw-r--r-- 1 german german  ~2300 bytes  credentials.json
```

> Si no existe, descárgalo de Google Cloud Console (ver guía de instalación, Paso 2).

### 2.2 Verificar `.env`

```bash
ls -la .env
```

**Resultado esperado:**
```
-rw-r--r-- 1 german german  ~500 bytes  .env
```

> Si no existe, créalo desde el ejemplo:
> ```bash
> cp .env.example .env
> ```
> Luego edítalo con tus datos.

### 2.3 Verificar que `.env` tiene las variables mínimas

```bash
cat .env
```

**Debe mostrar algo como:**
```bash
GOOGLE_CREDENTIALS_PATH=./credentials.json
DRIVE_ROOT_FOLDER_NAME=Proyectos_Empresa
DRIVE_ROOT_FOLDER_ID=
DEPARTMENTS=Ingeniería,Obras,Mantenimiento
SHEET_INGENIERIA_ID=
SHEET_OBRAS_ID=
SHEET_MANTENIMIENTO_ID=
SHEET_MAESTRO_ID=
ALERT_DAYS_THRESHOLD=3
LOG_FILE_PATH=./alertas_cronograma.log
```

> ⚠️ **Las variables `*_ID` deben estar VACÍAS** la primera vez. El script las llenará automáticamente.

---

## 🧪 Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

**Resultado esperado:**
```
Successfully installed google-api-python-client-2.xxx google-auth-2.xxx ...
```

**Verificar instalación:**

```bash
python -c "import pandas; import googleapiclient; print('✅ Todo instalado')"
```

**Resultado esperado:**
```
✅ Todo instalado
```

> Si falla, prueba:
> ```bash
> pip install --user -r requirements.txt
> # o
> pip3 install -r requirements.txt
> ```

---

## 🧪 Paso 4: Prueba de conexión con Google (Opcional pero recomendada)

Antes de ejecutar `main.py` completo, verifica que puedes conectarte a Google.

Guarda esto como `test_connection.py` en la carpeta del proyecto:

```python
#!/usr/bin/env python3
# Prueba rápida de conexión con Google Drive

import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"
]

try:
    creds = Credentials.from_service_account_file("./credentials.json", scopes=SCOPES)
    drive = build("drive", "v3", credentials=creds)

    # Probar listar archivos
    results = drive.files().list(pageSize=1).execute()
    items = results.get("files", [])

    print("✅ Conexión con Google Drive exitosa")
    print(f"   Encontrados {len(items)} archivos en tu Drive")

    # Probar crear y borrar una carpeta de prueba
    folder = drive.files().create(body={
        "name": "TEST_BORRAR",
        "mimeType": "application/vnd.google-apps.folder"
    }, fields="id").execute()

    drive.files().delete(fileId=folder["id"]).execute()
    print("✅ Crear/borrar carpetas funciona correctamente")
    print("
🎉 Todo listo para ejecutar main.py")

except Exception as e:
    print(f"❌ Error: {e}")
    print("
Posibles causas:")
    print("1. credentials.json inválido o faltante")
    print("2. APIs no habilitadas en Google Cloud")
    print("3. Problema de conexión a internet")
```

**Ejecutar la prueba:**

```bash
python test_connection.py
```

**Resultado esperado:**
```
✅ Conexión con Google Drive exitosa
   Encontrados 1 archivos en tu Drive
✅ Crear/borrar carpetas funciona correctamente

🎉 Todo listo para ejecutar main.py
```

> Si falla, NO ejecutes `main.py` todavía. Arregla el error primero (ver sección de Troubleshooting en la guía de instalación).

---

## 🚀 Paso 5: Primera ejecución de `main.py`

Con todo verificado, ejecuta:

```bash
python main.py
```

### 5.1 Resultado esperado en consola

```
======================================================
STEP 1: Setting up folder structure
======================================================
Root folder created with ID: 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
Ingeniería department folder: 1xxxxx...
Ingeniería clients folder: 1xxxxx...
Obras department folder: 1xxxxx...
Obras clients folder: 1xxxxx...
Mantenimiento department folder: 1xxxxx...
Mantenimiento clients folder: 1xxxxx...

======================================================
STEP 2: Setting up spreadsheets
======================================================
Headers created for Ingeniería
Spreadsheet for Ingeniería: 1xxxxx...
Headers created for Obras
Spreadsheet for Obras: 1xxxxx...
Headers created for Mantenimiento
Spreadsheet for Mantenimiento: 1xxxxx...
Headers created for master schedule
Master schedule spreadsheet: 1xxxxx...

======================================================
STEP 3: Consolidating schedules
======================================================
Read 1 rows from Ingeniería
Read 1 rows from Obras
Read 1 rows from Mantenimiento
Consolidated 0 projects to master schedule

======================================================
STEP 4: Evaluating alerts
======================================================
Total alerts logged: 0

✓ Execution completed successfully
```

> ⏱️ **Tarda 1-2 minutos** la primera vez porque crea todo desde cero.

### 5.2 Si ves errores

| Error | Qué hacer |
|-------|-----------|
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| `FileNotFoundError: credentials.json` | Descargar de Google Cloud Console |
| `HttpError 403` | Compartir carpeta con email de cuenta de servicio |
| `AttributeError: 'Config' has no attribute '...'` | Revisar que `.env` tenga todas las variables |

---

## ✅ Paso 6: Verificar en Google Drive

Abre [https://drive.google.com](https://drive.google.com) en tu navegador.

### 6.1 Verificar estructura de carpetas

Debes ver:

```
📁 Proyectos_Empresa
├── 📁 Ingeniería
│   ├── 📁 Clientes
│   └── 📄 Cronograma_Ingeniería
├── 📁 Obras
│   ├── 📁 Clientes
│   └── 📄 Cronograma_Obras
├── 📁 Mantenimiento
│   ├── 📁 Clientes
│   └── 📄 Cronograma_Mantenimiento
└── 📄 Cronograma_Maestro
```

**Verifica cada elemento:**

| Elemento | ¿Existe? | ¿Dónde? |
|----------|----------|---------|
| Carpeta `Proyectos_Empresa` | ☐ | Raíz de tu Drive |
| Carpeta `Ingeniería` dentro de `Proyectos_Empresa` | ☐ | Dentro de `Proyectos_Empresa` |
| Carpeta `Clientes` dentro de `Ingeniería` | ☐ | Dentro de `Ingeniería` |
| Sheet `Cronograma_Ingeniería` dentro de `Ingeniería` | ☐ | Dentro de `Ingeniería` |
| Carpeta `Obras` dentro de `Proyectos_Empresa` | ☐ | Dentro de `Proyectos_Empresa` |
| Carpeta `Clientes` dentro de `Obras` | ☐ | Dentro de `Obras` |
| Sheet `Cronograma_Obras` dentro de `Obras` | ☐ | Dentro de `Obras` |
| Carpeta `Mantenimiento` dentro de `Proyectos_Empresa` | ☐ | Dentro de `Proyectos_Empresa` |
| Carpeta `Clientes` dentro de `Mantenimiento` | ☐ | Dentro de `Mantenimiento` |
| Sheet `Cronograma_Mantenimiento` dentro de `Mantenimiento` | ☐ | Dentro de `Mantenimiento` |
| Sheet `Cronograma_Maestro` dentro de `Proyectos_Empresa` | ☐ | Dentro de `Proyectos_Empresa` |

> ✅ Marca cada casilla si el elemento existe. Si falta alguno, hay un problema.

---

## ✅ Paso 7: Verificar los Google Sheets

### 7.1 Abrir `Cronograma_Ingeniería`

Haz doble clic en el Sheet. Debe tener estos encabezados en la fila 1:

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| ID_Proyecto | Cliente | Descripcion | Fecha_Inicio | Fecha_Entrega | Estado | Responsable |

**Verifica:**
- [ ] Hay exactamente 7 columnas
- [ ] Los nombres coinciden exactamente (mayúsculas, acentos, etc.)
- [ ] La fila 1 tiene formato de encabezado (negrita, color, etc.)

### 7.2 Abrir `Cronograma_Maestro`

Debe tener estos encabezados en la fila 1:

| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| ID_Proyecto | Cliente | Descripcion | Fecha_Inicio | Fecha_Entrega | Estado | Responsable | Departamento |

**Verifica:**
- [ ] Hay exactamente 8 columnas
- [ ] La columna H se llama `Departamento`
- [ ] Las primeras 7 columnas coinciden con los Sheets departamentales

---

## ✅ Paso 8: Verificar el archivo `.env`

Después de la ejecución, el script debería haber guardado los IDs automáticamente.

```bash
cat .env
```

**Debe mostrar ahora algo como:**

```bash
GOOGLE_CREDENTIALS_PATH=./credentials.json
DRIVE_ROOT_FOLDER_NAME=Proyectos_Empresa
DRIVE_ROOT_FOLDER_ID=1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
DEPARTMENTS=Ingeniería,Obras,Mantenimiento
SHEET_INGENIERIA_ID=1qpyC0XzvTcKT6EISywvqESX3A0MwQoFDEvXq7Yd8iR8
SHEET_OBRAS_ID=1xxxxx...
SHEET_MANTENIMIENTO_ID=1xxxxx...
SHEET_MAESTRO_ID=1xxxxx...
ALERT_DAYS_THRESHOLD=3
LOG_FILE_PATH=./alertas_cronograma.log
```

**Verifica:**
- [ ] `DRIVE_ROOT_FOLDER_ID` tiene un valor (no está vacío)
- [ ] `SHEET_INGENIERIA_ID` tiene un valor
- [ ] `SHEET_OBRAS_ID` tiene un valor
- [ ] `SHEET_MANTENIMIENTO_ID` tiene un valor
- [ ] `SHEET_MAESTRO_ID` tiene un valor

> ⚠️ **Si algún ID sigue vacío,** el script no pudo crear ese elemento. Revisa los logs.

---

## ✅ Paso 9: Verificar el log de ejecución

```bash
cat alertas_cronograma.log
```

O si existe la carpeta `logs/`:

```bash
cat logs/project_scheduler.log
```

**Debes ver mensajes tipo:**

```
[INFO] Application initialized successfully
[INFO] STEP 1: Setting up folder structure
[INFO] Root folder created with ID: 1xxxxx...
[INFO] Ingeniería department folder: 1xxxxx...
...
[INFO] ✓ Execution completed successfully
```

**Verifica:**
- [ ] No hay mensajes `[ERROR]` o `[CRITICAL]`
- [ ] El último mensaje es de éxito
- [ ] Los IDs de carpetas y Sheets se registraron

---

## 🧪 Paso 10: Prueba con datos de ejemplo

Ahora que la estructura existe, vamos a agregar un proyecto de prueba.

### 10.1 Agregar un proyecto en `Cronograma_Ingeniería`

1. Abre el Sheet `Cronograma_Ingeniería` en Google Drive
2. Haz clic en la celda **A2** (fila 2, columna A)
3. Escribe los siguientes datos:

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| PROJ-TEST-001 | Cliente de Prueba | Instalación de prueba | 17/07/2026 | 20/07/2026 | En progreso | test@empresa.com |

> 💡 **Truco para generar alerta:** La fecha de entrega (`20/07/2026`) debe estar dentro de los próximos 3 días desde hoy. Ajusta las fechas según la fecha actual.

**Reglas importantes:**
- [ ] `ID_Proyecto`: cualquier texto, pero único
- [ ] `Fecha_Inicio` y `Fecha_Entrega`: formato **DD/MM/YYYY**
- [ ] `Estado`: exactamente `Pendiente`, `En progreso`, `Completado`, o `Retrasado`
- [ ] `Responsable`: un email válido

### 10.2 Volver a ejecutar el script

```bash
python main.py
```

### 10.3 Verificar resultados

| Qué verificar | Cómo hacerlo | Resultado esperado |
|---------------|------------|-------------------|
| Dato en Maestro | Abre `Cronograma_Maestro` | Fila 2 con los datos del proyecto |
| Columna Departamento | Columna H del Maestro | Dice "Ingeniería" |
| Alerta en log | `cat alertas_cronograma.log` | Mensaje `[WARNING] ALERTA: PROXIMO_A_VENCER` |
| Email (si configuraste SMTP) | Revisa tu bandeja de entrada | Email con la alerta del proyecto |

**Ejemplo de alerta esperada en el log:**

```
[2026-07-17 12:30:15] [WARNING] ALERTA: PROXIMO_A_VENCER
  Proyecto: PROJ-TEST-001
  Cliente: Cliente de Prueba
  Departamento: Ingeniería
  Fecha de entrega: 20/07/2026
  Días restantes: 3
  Estado actual: En progreso
  Responsable: test@empresa.com
  Mensaje: Proyecto PROJ-TEST-001 vence en 3 días
```

---

## 🔄 Paso 11: Segunda ejecución (verificar que no duplica)

Ejecuta el script una segunda vez:

```bash
python main.py
```

**Verifica:**
- [ ] **NO** se crearon carpetas duplicadas (no hay `Proyectos_Empresa (1)`)
- [ ] **NO** se crearon Sheets duplicados
- [ ] El script reutilizó los IDs existentes del `.env`
- [ ] El tiempo de ejecución es mucho más corto (segundos, no minutos)

> ✅ Si no hay duplicados, el sistema de guardado de IDs en `.env` funciona correctamente.

---

## 📊 Resumen de Resultados Esperados

| Prueba | Estado esperado |
|--------|-----------------|
| Estructura de carpetas en Drive | 1 raíz + 3 deptos + 3 Clientes |
| Sheets creados | 3 departamentales + 1 Maestro = 4 Sheets |
| Encabezados correctos | 7 cols en deptos, 8 cols en Maestro |
| IDs guardados en `.env` | 5 IDs llenos (root + 3 deptos + maestro) |
| Log sin errores | Solo `[INFO]` y `[WARNING]` (alertas) |
| Consolidación con datos | Proyecto de prueba aparece en Maestro |
| Alertas funcionan | Log muestra alerta por proximidad |
| No duplicados en 2da ejecución | Reutiliza IDs existentes |

---

## 🆘 Si algo falla

### Error: "No module named 'modules'"

**Causa:** Python no encuentra la carpeta `modules`.

**Solución:** Asegúrate de ejecutar desde la carpeta raíz del proyecto:
```bash
cd "/home/german/Escritorio/drive fer/project_scheduler"
python main.py
```

### Error: "'Config' object has no attribute 'GOOGLE_CREDENTIALS_PATH'"

**Causa:** El archivo `config.py` no tiene la variable esperada.

**Solución:** Revisa que `config.py` lea correctamente del `.env`. Puede que tenga nombres de variables diferentes.

### Error: Las carpetas se crean pero no las veo en MI Drive

**Causa:** Las carpetas pertenecen a la cuenta de servicio, no a tu cuenta personal.

**Solución:**
1. Ve a tu Google Drive
2. Crea manualmente la carpeta `Proyectos_Empresa`
3. Compártela con el email de la cuenta de servicio (Editor)
4. Borra el `.env` y vuelve a ejecutar

### Error: "Consolidated DataFrame is empty"

**Causa:** Los Sheets departamentales están vacíos (solo tienen encabezados).

**Solución:** Esto es **normal** si aún no agregaste proyectos. No es un error. Agrega datos de prueba (Paso 10).

---

## ✅ Checklist Final de la Prueba

Marca cada ítem después de verificarlo:

- [ ] `main.py` está limpio (sin código duplicado)
- [ ] `credentials.json` existe
- [ ] `.env` existe y está configurado
- [ ] Dependencias instaladas (`pip install`)
- [ ] Conexión con Google funciona (`test_connection.py`)
- [ ] Primera ejecución de `main.py` completada sin errores
- [ ] Carpeta `Proyectos_Empresa` visible en Drive
- [ ] 3 subcarpetas de departamentos creadas
- [ ] 3 subcarpetas `Clientes` creadas
- [ ] 4 Google Sheets creados (3 + Maestro)
- [ ] Encabezados correctos en todos los Sheets
- [ ] IDs guardados en `.env`
- [ ] Log sin errores críticos
- [ ] Proyecto de prueba agregado y consolidado
- [ ] Alerta generada en el log
- [ ] Segunda ejecución sin duplicados

> **Si marcaste todos los ítems:** 🎉 ¡El sistema funciona correctamente!
> 
> **Si falta alguno:** Revisa la sección de Troubleshooting o consulta la guía de instalación.

---

*Guía de prueba generada para verificar el funcionamiento del sistema Project Scheduler.*
