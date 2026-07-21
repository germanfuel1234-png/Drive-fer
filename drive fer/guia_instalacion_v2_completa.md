# 🚀 Guía de Instalación y Puesta en Marcha - Project Scheduler

> **Para:** Usuario final del sistema de planificación de proyectos
> **Contexto:** El proyecto ya fue generado y refactorizado por Copilot siguiendo el brief técnico. Esta guía explica paso a paso cómo instalar dependencias, configurar Google Cloud, ejecutar el script y verificar que todo funcione.

---

## 📚 Documentación Relacionada

> **Nota:** Esta es la guía de instalación. Si quieres entender cómo se estructuró el código, lee primero:
> - 📄 `RESUMEN_FINAL.md` — Resumen ejecutivo del proyecto
> - 📄 `BRIEF_APLICACION.md` — Mapeo punto-a-punto del brief técnico al código
> - 📄 `INDEX_DOCUMENTACION.md` — Guía de navegación por toda la documentación
> - 🐍 `validate_brief_application.py` — Script para validar que todo se implementó correctamente

---

## 📁 Mapa Visual de la Estructura del Proyecto

Antes de empezar, conoce dónde está cada archivo:

```
/home/german/Escritorio/drive fer/project_scheduler/
│
├── 📄 main.py                      ← Orquestador principal. Ejecuta todo el flujo.
├── 📄 config.py                    ← Configuración centralizada (lee .env)
├── 📄 requirements.txt             ← Dependencias de Python
├── 📄 .env.example                 ← Plantilla de variables de entorno
├── 📄 .env                         ← Tu configuración real (se crea del ejemplo)
├── 📄 .gitignore                   ← Protege archivos sensibles
├── 📄 credentials.json             ← Clave de Google Cloud (tú lo descargas)
│
├── 📁 modules/
│   ├── 📄 auth.py                  ← Autenticación con Google (Cuenta de Servicio)
│   ├── 📄 drive_manager.py         ← Crea y gestiona carpetas en Google Drive
│   ├── 📄 sheets_manager.py        ← Crea y gestiona Google Sheets
│   ├── 📄 scheduler.py             ← Lógica de fechas, plazos y alertas
│   ├── 📄 consolidator.py          ← Une datos de los 3 departamentos con pandas
│   └── 📄 notifier.py            ← Alertas por log y email (SMTP)
│
├── 📁 examples/
│   ├── 📄 example_1_setup.py       ← Ejemplo: inicializar y agregar proyectos
│   ├── 📄 example_2_reports.py   ← Ejemplo: generar reportes consolidados
│   ├── 📄 example_3_notifications.py ← Ejemplo: alertas y notificaciones
│   └── 📄 example_4_export.py      ← Ejemplo: exportar datos a CSV
│
├── 📁 docs/
│   ├── 📄 SETUP.md                 ← Guía de Google Cloud Console
│   ├── 📄 README.md                ← Documentación completa de la API
│   ├── 📄 INICIO_RAPIDO.md         ← Resumen ejecutivo
│   ├── 📄 INDEX.md                 ← Índice de navegación
│   ├── 📄 BRIEF_APLICACION.md      ← Mapeo exacto brief → código
│   ├── 📄 RESUMEN_FINAL.md         ← Resumen del estado del proyecto
│   └── 📄 CHANGELOG.md             ← Historial de cambios
│
├── 📄 quickstart.py                ← Verificación rápida de configuración
├── 📄 test_suite.py                ← Tests unitarios del sistema
├── 📄 validate_brief_application.py ← Valida que el brief se aplicó correctamente
│
└── 📁 logs/
    └── 📄 alertas_cronograma.log   ← Registro de alertas y eventos
```

> 💡 **Tip:** Los archivos en `examples/` son scripts de Python que puedes ejecutar para ver cómo funciona cada parte del sistema sin tocar `main.py`.

---

## 📊 Estado del Proyecto (Resumen de Copilot)

| Aspecto | Estado | Detalle |
|---------|--------|---------|
| **Estructura modular** | ✅ | 4 módulos nuevos + 3 refactorizados |
| **`pandas` para consolidación** | ✅ | `consolidator.py` con `pd.concat()` |
| **`datetime` para fechas** | ✅ | `scheduler.py` con formato DD/MM/YYYY |
| **Cuenta de Servicio** | ✅ | `auth.py` con `GoogleAuth` |
| **Schema exacto (7+1 columnas)** | ✅ | 8 columnas validadas |
| **Estados válidos** | ✅ | 4 valores exactos |
| **Flujo de 10 pasos** | ✅ | Implementado en `main.py` |
| **Documentación** | ✅ | 5 documentos nuevos |
| **Tests/Validación** | ⚠️ | 7/8 pasaron (faltan dependencias) |

**La única falla** es que las librerías de Google no están instaladas — esto es **normal y esperado** porque aún no has ejecutado `pip install`. No es un error del código.

---

## 🔧 Paso 1: Instalar Dependencias

Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
cd "/home/german/Escritorio/drive fer/project_scheduler"
pip install -r requirements.txt
```

> **Si usas Linux/Mac y tienes problemas de permisos, prueba:**
> ```bash
> pip install --user -r requirements.txt
> ```
> **O si usas Python 3 explícitamente:**
> ```bash
> pip3 install -r requirements.txt
> ```

**Verifica que se instalaron correctamente:**

```bash
python -c "import pandas; import googleapiclient; print('✅ Todo instalado')"
```

---

## 🔐 Paso 2: Configurar Credenciales de Google Cloud

Necesitas crear una **Cuenta de Servicio** en Google Cloud Console. Sigue estos pasos:

### 2.1 Crear un proyecto en Google Cloud

1. Ve a [https://console.cloud.google.com/](https://console.cloud.google.com/)
2. Inicia sesión con tu cuenta de Google
3. En la barra superior, haz clic en el selector de proyecto y luego en **"Nuevo proyecto"**
4. Dale un nombre (ej: `Proyectos-Empresa-2026`)
5. Haz clic en **"Crear"**

### 2.2 Habilitar las APIs necesarias

1. En el menú lateral, ve a **"APIs y servicios" → Biblioteca**
2. Busca y habilita cada una de estas APIs:
   - ✅ **Google Drive API**
   - ✅ **Google Sheets API**
3. Haz clic en cada una y presiona **"Habilitar"**

### 2.3 Crear la Cuenta de Servicio

1. Ve a **"APIs y servicios" → Credenciales**
2. Haz clic en **"Crear credenciales" → "Cuenta de servicio"**
3. En **"Detalles de la cuenta de servicio"**:
   - Nombre: `project-scheduler`
   - ID: se genera automático
   - Descripción: `Sistema de planificación de proyectos`
4. Haz clic en **"Crear y continuar"**
5. En **"Otorgar acceso a este proyecto"**, selecciona el rol:
   - **Editor** (o si prefieres más restrictivo: **Propietario de datos de Drive** + **Editor de Google Sheets**)
6. Haz clic en **"Continuar"** y luego **"Listo"**

### 2.4 Descargar la clave JSON

1. En la lista de cuentas de servicio, haz clic en la que acabas de crear
2. Ve a la pestaña **"Claves"**
3. Haz clic en **"Agregar clave" → "Crear clave nueva"**
4. Selecciona tipo **JSON**
5. Se descargará automáticamente un archivo `.json`
6. **Muévelo** a la carpeta de tu proyecto y renómbralo a `credentials.json`

> 📁 Ubicación final: `/home/german/Escritorio/drive fer/project_scheduler/credentials.json`

---

## ⚙️ Paso 3: Configurar el Archivo `.env`

Copia el archivo de ejemplo y edítalo con tus datos:

```bash
cp .env.example .env
```

Luego abre `.env` con tu editor de texto y completa así:

```bash
# === AUTENTICACIÓN GOOGLE ===
GOOGLE_CREDENTIALS_PATH=./credentials.json

# === DRIVE ===
DRIVE_ROOT_FOLDER_NAME=Proyectos_Empresa
# Deja vacío la primera vez; el script lo llenará automáticamente:
DRIVE_ROOT_FOLDER_ID=

# === DEPARTAMENTOS ===
DEPARTMENTS=Ingeniería,Obras,Mantenimiento

# === SHEETS (dejar vacío la primera vez) ===
SHEET_INGENIERIA_ID=
SHEET_OBRAS_ID=
SHEET_MANTENIMIENTO_ID=
SHEET_MAESTRO_ID=

# === ALERTAS ===
ALERT_DAYS_THRESHOLD=3
LOG_FILE_PATH=./alertas_cronograma.log

# === EMAIL SMTP (opcional) ===
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu_email@gmail.com
SMTP_PASSWORD=tu_app_password
ALERT_RECIPIENTS=gestor1@empresa.com,gestor2@empresa.com
```

### Nota importante sobre rutas relativas

- `./credentials.json` significa **"en la misma carpeta donde está `main.py`"**.
- Si moves el archivo `credentials.json` a otra carpeta, debes poner la ruta completa. Ejemplos:
  - Linux/Mac: `GOOGLE_CREDENTIALS_PATH=/home/german/Documentos/credentials.json`
  - Windows: `GOOGLE_CREDENTIALS_PATH=C:\Users\german\Documents\credentials.json`

### Nota importante sobre Gmail

Si usas Gmail para las alertas por email, **NO uses tu contraseña normal**. Necesitas una **"App Password"** (contraseña de aplicación):

1. Ve a [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Inicia sesión con tu cuenta de Google
3. En **"Seleccionar app"**, elige **"Otra"** y escribe `Project Scheduler`
4. Haz clic en **"Generar"**
5. Copia la contraseña de 16 caracteres y pégala en `SMTP_PASSWORD`

> Si no quieres usar alertas por email, deja las variables SMTP vacías. El sistema seguirá registrando alertas en el archivo de log.

---

## 📁 Paso 4: Compartir la Carpeta Raíz con la Cuenta de Servicio

Este paso es **CRÍTICO** y muchos lo olvidan. Si no lo haces, el script creará la carpeta pero **tú no la verás** en tu Drive personal.

### 4.1 Obtener el email de la cuenta de servicio

1. Ve a [https://console.cloud.google.com/iam-admin/serviceaccounts](https://console.cloud.google.com/iam-admin/serviceaccounts)
2. Haz clic en tu cuenta de servicio (`project-scheduler`)
3. Copia el **"Dirección de correo electrónico"**
4. Tiene este formato: `project-scheduler@proyectos-empresa-2026.iam.gserviceaccount.com`

### 4.2 Compartir en Google Drive

1. Ve a tu [Google Drive](https://drive.google.com)
2. Crea una carpeta llamada `Proyectos_Empresa` (o usa la que ya tengas)
3. Haz **clic derecho** sobre la carpeta → **"Compartir"**
4. Pega el email de la cuenta de servicio
5. En permisos, selecciona **"Editor"**
6. Haz clic en **"Enviar"**

> ✅ Ahora la cuenta de servicio puede crear, leer y modificar archivos dentro de esa carpeta.

---

## 🚀 Paso 5: Ejecutar por Primera Vez

Con todo configurado, ejecuta:

```bash
python main.py
```

### Lo que debería pasar automáticamente:

1. ✅ **Autentica** con Google usando `credentials.json`
2. ✅ **Crea/encuentra** la carpeta `Proyectos_Empresa`
3. ✅ **Crea** las 3 subcarpetas de departamentos: `Ingeniería`, `Obras`, `Mantenimiento`
4. ✅ **Crea** las subcarpetas `Clientes` dentro de cada departamento
5. ✅ **Crea** 3 Google Sheets de cronograma (uno por departamento) con los 7 encabezados
6. ✅ **Crea** el Cronograma Maestro con los 8 encabezados
7. ✅ **Guarda** todos los IDs en `.env` automáticamente
8. ✅ **Lee** datos (vacíos al inicio) y los consolida
9. ✅ **Evalúa** alertas (ninguna al inicio)
10. ✅ **Registra** la ejecución en el log

> ⏱️ La primera ejecución puede tardar 1-2 minutos porque crea todo desde cero.

---

## ✅ Paso 6: Verificar que Todo se Creó Correctamente

Después de ejecutar, revisa cada uno de estos puntos:

### 6.1 Revisar Google Drive

| Qué buscar | Dónde encontrarlo |
|------------|-------------------|
| Carpeta raíz | Tu Google Drive → `Proyectos_Empresa` |
| Subcarpetas departamentos | Dentro de `Proyectos_Empresa` → `Ingeniería`, `Obras`, `Mantenimiento` |
| Subcarpetas Clientes | Dentro de cada departamento → `Clientes` |

### 6.2 Revisar Google Sheets

| Qué buscar | Dónde encontrarlo |
|------------|-------------------|
| Cronograma Ingeniería | Dentro de la carpeta `Ingeniería` en Drive |
| Cronograma Obras | Dentro de la carpeta `Obras` en Drive |
| Cronograma Mantenimiento | Dentro de la carpeta `Mantenimiento` en Drive |
| Cronograma Maestro | Dentro de la carpeta `Proyectos_Empresa` en Drive |

**Verifica los encabezados de cada Sheet departamental:**

```
A1: ID_Proyecto
B1: Cliente
C1: Descripcion
D1: Fecha_Inicio
E1: Fecha_Entrega
F1: Estado
G1: Responsable
```

**Verifica los encabezados del Maestro (8 columnas):**

```
A1: ID_Proyecto
B1: Cliente
C1: Descripcion
D1: Fecha_Inicio
E1: Fecha_Entrega
F1: Estado
G1: Responsable
H1: Departamento
```

### 6.3 Revisar el archivo `.env`

Abre `.env` y verifica que ahora tiene los IDs llenos automáticamente:

```bash
DRIVE_ROOT_FOLDER_ID=1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
SHEET_INGENIERIA_ID=1qpyC0XzvTcKT6EISywvqESX3A0MwQoFDEvXq7Yd8iR8
SHEET_OBRAS_ID=1xxxxx...
SHEET_MANTENIMIENTO_ID=1xxxxx...
SHEET_MAESTRO_ID=1xxxxx...
```

> ✅ Estos IDs se reutilizarán en futuras ejecuciones. No borrarlos.

### 6.4 Revisar el log de ejecución

```bash
cat alertas_cronograma.log
# o
cat logs/project_scheduler.log
```

Deberías ver mensajes tipo:
```
[INFO] Iniciando Project Scheduler
[INFO] Carpeta 'Proyectos_Empresa' creada con ID: 1xxxxx...
[INFO] Sheet 'Cronograma_Ingeniería' creado con ID: 1xxxxx...
[INFO] Consolidación completada: 0 proyectos
[INFO] Alertas evaluadas: 0 alertas generadas
[INFO] Ejecución finalizada exitosamente
```

---

## 🧪 Paso 7: Probar con Datos de Ejemplo

Para verificar que la consolidación y las alertas funcionan, agrega un proyecto de prueba:

### 7.1 Agregar un proyecto en el Sheet de Ingeniería

1. Abre el Google Sheet **"Cronograma_Ingeniería"**
2. En la fila 2 (debajo de los encabezados), escribe:

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| PROJ-001 | Constructora XYZ | Instalación eléctrica edificio A | 15/07/2026 | 20/07/2026 | En progreso | juan@empresa.com |

> 💡 **Truco:** Pon la `Fecha_Entrega` dentro de los próximos 3 días desde hoy para que genere una alerta. Por ejemplo, si hoy es 17/07/2026, pon `20/07/2026`.

### 7.2 Volver a ejecutar el script

```bash
python main.py
```

### 7.3 Verificar resultados

| Qué verificar | Cómo verificar |
|---------------|----------------|
| ✅ Dato aparece en Maestro | Abre el Sheet "Cronograma_Maestro" → fila 2 |
| ✅ Columna "Departamento" dice "Ingeniería" | Columna H del Maestro |
| ✅ Alerta generada en log | `cat alertas_cronograma.log` → busca "PROXIMO_A_VENCER" |
| ✅ Email enviado (si configuraste SMTP) | Revisa la bandeja de entrada de los destinatarios |

**Ejemplo de alerta esperada en el log:**
```
[WARNING] ALERTA: PROXIMO_A_VENCER
  Proyecto: PROJ-001
  Cliente: Constructora XYZ
  Departamento: Ingeniería
  Días restantes: 3
  Mensaje: Proyecto PROJ-001 vence en 3 días
```

---

## 📝 Paso 8: Agregar Proyectos Reales

Ahora que todo funciona, es hora de usar el sistema con datos reales.

### 8.1 Cómo agregar un proyecto

1. Abre el Google Sheet del departamento correspondiente (ej: `Cronograma_Ingeniería`)
2. En la primera fila vacía (debajo de los encabezados), completa cada columna:

| Columna | Qué escribir | Ejemplo | Reglas |
|---------|-------------|---------|--------|
| **A** `ID_Proyecto` | Código único | `PROJ-002` | No repetir IDs. Usar formato PROJ-XXX. |
| **B** `Cliente` | Nombre del cliente | `Edificios del Sur S.A.` | Texto libre. |
| **C** `Descripcion` | Qué se va a hacer | `Mantenimiento de ascensores torre A` | Texto libre. Sé descriptivo. |
| **D** `Fecha_Inicio` | Cuándo empieza | `18/07/2026` | **Formato obligatorio: DD/MM/YYYY** |
| **E** `Fecha_Entrega` | Cuándo debe terminar | `25/07/2026` | **Formato obligatorio: DD/MM/YYYY** |
| **F** `Estado` | En qué va el proyecto | `Pendiente` | **Valores exactos:** `Pendiente`, `En progreso`, `Completado`, `Retrasado` |
| **G** `Responsable` | Email del encargado | `maria@empresa.com` | Debe ser un email válido. |

> ⚠️ **IMPORTANTE:** El estado debe escribirse **exactamente** como aparece arriba. Si escribes "En proceso" en vez de "En progreso", el script no lo reconocerá correctamente.

### 8.2 Reglas para las fechas

- Siempre usa el formato **DD/MM/YYYY** (día/mes/año)
- ✅ Correcto: `18/07/2026`, `01/12/2026`, `25/03/2026`
- ❌ Incorrecto: `2026-07-18`, `07/18/2026`, `18-07-2026`
- La `Fecha_Entrega` debe ser **igual o posterior** a la `Fecha_Inicio`

### 8.3 Reglas para los estados

| Estado | Cuándo usarlo |
|--------|--------------|
| `Pendiente` | El proyecto está aprobado pero aún no empezó |
| `En progreso` | El proyecto está en ejecución activa |
| `Completado` | El proyecto terminó y se entregó |
| `Retrasado` | El proyecto debería estar terminado pero no lo está |

> 💡 **Tip:** Usa la validación de datos de Google Sheets (Datos → Validación de datos) para crear una lista desplegable en la columna `Estado`. Así evitas errores de tipeo.

### 8.4 Ejecutar el script para consolidar

Cada vez que agregues o modifiques proyectos, ejecuta:

```bash
python main.py
```

El script:
- Leerá los datos actualizados de los 3 departamentos
- Los consolidará en el **Cronograma Maestro**
- Evaluará si hay alertas por vencimiento
- Registrará todo en el log

> ⚠️ **ADVERTENCIA:** No edites el **Cronograma Maestro** manualmente. Se sobrescribe automáticamente cada vez que corre el script. Si editas algo a mano, se perderá en la siguiente ejecución. **Solo edita los Sheets departamentales.**

---

## 🔄 Paso 9: Ejecutar el Script Regularmente

El sistema funciona mejor si se ejecuta automáticamente cada cierto tiempo. Así los cronogramas se mantienen actualizados y las alertas llegan a tiempo.

### 9.1 Opción A: Ejecutar manualmente

Simplemente corre cuando necesites:

```bash
cd "/home/german/Escritorio/drive fer/project_scheduler"
python main.py
```

### 9.2 Opción B: Tarea programada automática (recomendado)

#### En Linux / Mac (cron job)

1. Abre el editor de cron:
```bash
crontab -e
```

2. Agrega una línea para ejecutar el script todos los días a las 8:00 AM:
```bash
0 8 * * * cd /home/german/Escritorio/drive\ fer/project_scheduler && /usr/bin/python3 main.py >> /home/german/Escritorio/drive\ fer/project_scheduler/logs/cron.log 2>&1
```

3. Guarda y cierra.

**Explicación de la línea:**
- `0 8 * * *` = minuto 0 de la hora 8, todos los días, todos los meses
- `cd ... && python3 main.py` = entra a la carpeta y ejecuta
- `>> .../cron.log 2>&1` = guarda la salida en un log de cron

**Otras frecuencias útiles:**

| Frecuencia | Línea de cron |
|------------|---------------|
| Cada hora | `0 * * * * cd ... && python3 main.py ...` |
| Cada 30 minutos | `*/30 * * * * cd ... && python3 main.py ...` |
| Lunes a viernes a las 9 AM | `0 9 * * 1-5 cd ... && python3 main.py ...` |
| Cada lunes a las 8 AM | `0 8 * * 1 cd ... && python3 main.py ...` |

#### En Windows (Task Scheduler)

1. Presiona `Win + R`, escribe `taskschd.msc` y presiona Enter
2. En el panel derecho, haz clic en **"Crear tarea básica..."**
3. Nombre: `Project Scheduler - Consolidación`
4. Descripción: `Ejecuta el script de planificación de proyectos`
5. Disparador: **"Diariamente"** → a las **08:00:00**
6. Acción: **"Iniciar un programa"**
7. Programa/script: busca la ruta de tu Python (ej: `C:\Users\german\AppData\Local\Programs\Python\Python311\python.exe`)
8. Argumentos: `main.py`
9. Iniciar en: `C:\Users\german\Escritorio\drive fer\project_scheduler`
10. Finalizar el asistente y listo.

---

## 📊 Paso 10: Entender la Consolidación

### ¿Qué es la consolidación?

La consolidación es el proceso por el cual el script:

1. **Lee** los datos de los 3 Sheets departamentales (Ingeniería, Obras, Mantenimiento)
2. **Une** todos esos datos en un solo DataFrame usando `pandas`
3. **Agrega** la columna `Departamento` para saber de dónde viene cada proyecto
4. **Escribe** el resultado en el **Cronograma Maestro**

### Diagrama del flujo

```
┌─────────────────────┐
│ Cronograma          │
│ Ingeniería          │
│ (Sheet)             │
└──────────┬──────────┘
           │
┌─────────────────────┐
│ Cronograma          │         ┌─────────────────────┐
│ Obras               │────────→│  CONSOLIDADOR       │
│ (Sheet)             │         │  (pandas.concat)    │
└──────────┬──────────┘         │                     │
           │                    │  Une + agrega       │
┌─────────────────────┐         │  columna            │
│ Cronograma          │────────→│  "Departamento"     │
│ Mantenimiento       │         └──────────┬──────────┘
│ (Sheet)             │                    │
└─────────────────────┘                    ↓
                              ┌─────────────────────┐
                              │ Cronograma Maestro  │
                              │ (Sheet)             │
                              │                     │
                              │ Todos los proyectos │
                              │ de todos los deptos │
                              └─────────────────────┘
```

### ¿Por qué es útil?

- **Gerencia** puede ver todos los proyectos de la empresa en un solo lugar
- **Filtros** permiten ver solo los de un departamento, un cliente, o un estado
- **Alertas** se evalúan sobre TODOS los proyectos, no solo de un departamento
- **Reportes** se generan a partir de un solo fuente de datos

---

## 🔔 Paso 11: Entender el Sistema de Alertas

### ¿Cómo funcionan las alertas?

El script evalúa cada proyecto en los 3 departamentos y genera alertas en estos casos:

| Tipo de alerta | Condición | Ejemplo |
|---------------|-----------|---------|
| **PROXIMO_A_VENCER** | Faltan 3 días o menos para la entrega Y el estado NO es "Completado" | Hoy es 17/07, entrega es 20/07, estado = "En progreso" → ALERTA |
| **VENCIDO** | La fecha de entrega ya pasó Y el estado NO es "Completado" | Hoy es 21/07, entrega era 20/07, estado = "Pendiente" → ALERTA |

> El umbral de 3 días se configura en `.env` con la variable `ALERT_DAYS_THRESHOLD=3`. Puedes cambiarlo a 5, 7, etc.

### ¿Dónde llegan las alertas?

1. **Archivo de log:** `alertas_cronograma.log` (siempre se genera)
2. **Email:** Si configuraste SMTP, se envía a los destinatarios de `ALERT_RECIPIENTS`

### Ejemplo de alerta en el log

```
[2026-07-17 08:00:15] WARNING: ALERTA: PROXIMO_A_VENCER
  Proyecto: PROJ-001
  Cliente: Constructora XYZ
  Departamento: Ingeniería
  Fecha de entrega: 20/07/2026
  Días restantes: 3
  Estado actual: En progreso
  Responsable: juan@empresa.com
  Mensaje: Proyecto PROJ-001 vence en 3 días
```

> 📋 **El log es tu historial operativo.** Revisarlo regularmente te dice qué proyectos necesitan atención urgente.

---

## ➕ Paso 12: Agregar un Nuevo Departamento (Escalabilidad)

El sistema está diseñado para que agregar un departamento sea fácil.

### 12.1 Pasos para agregar un departamento

**Ejemplo:** Queremos agregar el departamento de **"Calidad"**.

1. **Edita el archivo `.env`:**
```bash
# Antes:
DEPARTMENTS=Ingeniería,Obras,Mantenimiento

# Después:
DEPARTMENTS=Ingeniería,Obras,Mantenimiento,Calidad
```

2. **Ejecuta el script:**
```bash
python main.py
```

3. **El script hará automáticamente:**
   - ✅ Crea la carpeta `Calidad` dentro de `Proyectos_Empresa`
   - ✅ Crea la subcarpeta `Clientes` dentro de `Calidad`
   - ✅ Crea el Sheet `Cronograma_Calidad` con los 7 encabezados
   - ✅ Guarda el nuevo ID en `.env` como `SHEET_CALIDAD_ID`
   - ✅ El Maestro ahora incluye proyectos de los 4 departamentos

> ⚠️ **Nota:** El nombre del departamento en `.env` debe coincidir exactamente con el nombre que quieres que aparezca en Drive y en la columna `Departamento` del Maestro.

---

## 🧪 Scripts de Ejemplo y Tests

El proyecto incluye scripts de ejemplo para que aprendas a usar cada parte del sistema sin tocar `main.py`.

### Ejecutar los ejemplos

```bash
cd "/home/german/Escritorio/drive fer/project_scheduler"

# Ejemplo 1: Inicializar sistema y agregar proyectos
python examples/example_1_setup.py

# Ejemplo 2: Generar reportes consolidados
python examples/example_2_reports.py

# Ejemplo 3: Probar alertas y notificaciones
python examples/example_3_notifications.py

# Ejemplo 4: Exportar datos a CSV
python examples/example_4_export.py
```

### Ejecutar los tests unitarios

```bash
python test_suite.py
```

> Esto verifica que los módulos individuales funcionan correctamente antes de ejecutar el sistema completo.

---


## 🆘 Troubleshooting: Errores Comunes y Soluciones

Esta sección cubre los problemas más frecuentes que pueden aparecer al instalar o ejecutar el sistema, con sus causas y soluciones paso a paso.

---

### Error 1: "ModuleNotFoundError: No module named 'googleapiclient'"

**Cómo se ve:**
```
Traceback (most recent call last):
  File "main.py", line 5, in <module>
    from googleapiclient.discovery import build
ModuleNotFoundError: No module named 'googleapiclient'
```

**Causa:** Las dependencias de Python no están instaladas. El archivo `requirements.txt` no se ejecutó o falló.

**Solución:**
```bash
cd "/home/german/Escritorio/drive fer/project_scheduler"
pip install -r requirements.txt
```

> Si usas Linux/Mac y tienes problemas de permisos:
> ```bash
> pip install --user -r requirements.txt
> ```
> O con Python 3 explícitamente:
> ```bash
> pip3 install -r requirements.txt
> ```

**Verificación:**
```bash
python -c "import googleapiclient; print('✅ googleapiclient instalado')"
```

---

### Error 2: "FileNotFoundError: credentials.json"

**Cómo se ve:**
```
FileNotFoundError: [Errno 2] No such file or directory: './credentials.json'
```

**Causa:** El archivo de credenciales de Google Cloud no está en la carpeta del proyecto, o la ruta en `.env` es incorrecta.

**Solución paso a paso:**

1. **Verifica que el archivo existe:**
   ```bash
   ls -la credentials.json
   ```
   Si no aparece, aún no lo has descargado de Google Cloud Console.

2. **Descarga el archivo desde Google Cloud Console:**
   - Ve a [https://console.cloud.google.com/iam-admin/serviceaccounts](https://console.cloud.google.com/iam-admin/serviceaccounts)
   - Selecciona tu cuenta de servicio
   - Ve a la pestaña **"Claves"**
   - **"Agregar clave" → "Crear clave nueva" → JSON**
   - Guarda el archivo en la carpeta del proyecto como `credentials.json`

3. **Verifica la ruta en `.env`:**
   ```bash
   # Si el archivo está en la misma carpeta que main.py:
   GOOGLE_CREDENTIALS_PATH=./credentials.json

   # Si lo pusiste en otra carpeta, usa la ruta completa:
   # Linux/Mac:
   GOOGLE_CREDENTIALS_PATH=/home/german/Documentos/credentials.json
   # Windows:
   GOOGLE_CREDENTIALS_PATH=C:\Users\german\Documents\credentials.json
   ```

---

### Error 3: "HttpError 403: Permission denied"

**Cómo se ve:**
```
googleapiclient.errors.HttpError: <HttpError 403 when requesting ... returned "Permission denied">
```

**Causa:** La cuenta de servicio no tiene permisos para acceder a la carpeta de Google Drive o a los Sheets.

**Solución paso a paso:**

1. **Obtén el email de la cuenta de servicio:**
   - Ve a [https://console.cloud.google.com/iam-admin/serviceaccounts](https://console.cloud.google.com/iam-admin/serviceaccounts)
   - Copia el email (formato: `nombre@proyecto.iam.gserviceaccount.com`)

2. **Comparte la carpeta raíz en Google Drive:**
   - Ve a [https://drive.google.com](https://drive.google.com)
   - Encuentra la carpeta `Proyectos_Empresa`
   - Clic derecho → **"Compartir"**
   - Pega el email de la cuenta de servicio
   - Selecciona permisos: **"Editor"**
   - Haz clic en **"Enviar"**

3. **Si los Sheets ya existen**, compártelos individualmente con el mismo email y permisos de Editor.

4. **Verifica que la API de Drive esté habilitada** en Google Cloud Console.

---

### Error 4: "Las alertas no se envían por email"

**Síntomas:**
- El log muestra alertas generadas (`[WARNING] ALERTA: ...`)
- Pero no llegan emails a los destinatarios
- No hay error visible en la consola

**Causas posibles y soluciones:**

| Causa | Cómo detectarla | Solución |
|-------|----------------|----------|
| **SMTP no configurado** | Variables `SMTP_*` están vacías en `.env` | Completa todas las variables SMTP |
| **Contraseña normal en vez de App Password** | Gmail bloquea el login | Genera una App Password en [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) |
| **Puerto SMTP incorrecto** | `SMTP_PORT=587` para TLS, `SMTP_PORT=465` para SSL | Verifica con tu proveedor de email |
| **Servidor SMTP incorrecto** | `smtp.gmail.com` solo funciona con Gmail | Si usas otro proveedor, cambia el servidor |
| **Email de destinatario mal escrito** | Revisa `ALERT_RECIPIENTS` | Emails separados por coma, sin espacios extra |
| **Firewall bloqueando puerto 587** | Error de conexión timeout | Habilita el puerto o usa VPN |

**Para diagnosticar, ejecuta el ejemplo de notificaciones:**
```bash
python examples/example_3_notifications.py
```

Este script de ejemplo prueba el envío de email de forma aislada y te dará un error más específico.

---

### Error 5: "El script crea duplicados cada vez que lo ejecuto"

**Síntomas:**
- Cada vez que corres `python main.py`, aparecen nuevas carpetas `Proyectos_Empresa (1)`, `Proyectos_Empresa (2)`...
- O se crean Sheets duplicados con nombres similares

**Causa:** Los IDs de las carpetas/Sheets no se están guardando en `.env`, o el archivo `.env` no se está leyendo correctamente.

**Solución paso a paso:**

1. **Verifica que `.env` existe y tiene los IDs:**
   ```bash
   cat .env
   ```
   Deberías ver algo como:
   ```
   DRIVE_ROOT_FOLDER_ID=1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
   SHEET_INGENIERIA_ID=1qpyC0XzvTcKT6EISywvqESX3A0MwQoFDEvXq7Yd8iR8
   ```

2. **Si los IDs están vacíos**, borra las carpetas/Sheets duplicados de Drive y ejecuta de nuevo:
   ```bash
   python main.py
   ```
   Al finalizar, verifica que `.env` ahora tenga los IDs llenos.

3. **Si los IDs están llenos pero sigue creando duplicados**, verifica que `python-dotenv` esté instalado:
   ```bash
   pip install python-dotenv
   ```

4. **Como último recurso**, borra todo (ver sección "Cómo Desinstalar"), borra `.env`, y empieza desde cero.

---

### Error 6: "No se crearon las carpetas en MI Drive"

**Síntomas:**
- El script dice "Carpeta creada exitosamente"
- Pero no ves la carpeta en tu Google Drive personal

**Causa:** Las carpetas se crearon pero pertenecen a la **cuenta de servicio** (un usuario "robot"), no a tu cuenta personal de Google.

**Solución:**

1. **Crea la carpeta tú mismo** en tu Drive personal con el nombre `Proyectos_Empresa`
2. **Compártela** con el email de la cuenta de servicio (rol: Editor)
3. **Ejecuta el script de nuevo.** Ahora detectará la carpeta existente y la reutilizará.

> Alternativa: Después de que el script crea la carpeta, compártela desde la cuenta de servicio a tu email personal. Esto es más complejo porque requiere que el script comparta automáticamente.

---

### Error 7: "Las fechas se ven mal en el Sheet" o "Alertas incorrectas"

**Síntomas:**
- Fechas como `45/17/2026` o `2026-17-45`
- Alertas que deberían activarse no lo hacen, o viceversa

**Causa:** El formato de fecha en el Sheet no es `DD/MM/YYYY`.

**Solución:**

1. **En Google Sheets**, selecciona las columnas D (`Fecha_Inicio`) y E (`Fecha_Entrega`)
2. Ve a **Formato → Número → Fecha**
3. Elige el formato `DD/MM/YYYY`
4. **Reingresa las fechas** manualmente en ese formato

> ⚠️ **Importante:** Si copias y pegas desde Excel, el formato puede cambiar. Siempre verifica después de pegar.

---

## 📋 Cómo Leer e Interpretar los Logs

Los logs son tu herramienta principal para saber qué está pasando con el sistema. Aprender a leerlos te ahorra mucho tiempo de debugging.

### Ubicación de los logs

```bash
# Log principal de alertas
cat alertas_cronograma.log

# Log de ejecución general (si existe carpeta logs/)
cat logs/project_scheduler.log

# Log de tareas programadas (si usas cron)
cat logs/cron.log
```

### Niveles de log y qué significan

| Nivel | Color/Icono | Significado | Qué hacer |
|-------|------------|-------------|-----------|
| `[INFO]` | 🟢 Azul/Verde | Información normal. Todo va bien. | Nada. Es solo registro. |
| `[WARNING]` | 🟡 Amarillo | Algo requiere atención. No es un error, pero podría serlo. | Revisar. Ej: alerta de proyecto próximo a vencer. |
| `[ERROR]` | 🔴 Rojo | Algo falló. El script pudo continuar o no. | **Revisar inmediatamente.** Ej: no pudo leer un Sheet. |
| `[CRITICAL]` | 🔴🔴 Rojo intenso | Error grave. El script probablemente se detuvo. | **Revisar y corregir antes de volver a ejecutar.** |
| `[DEBUG]` | ⚪ Gris | Información detallada para desarrolladores. | Solo útil si estás modificando el código. |

### Ejemplos de mensajes y cómo interpretarlos

#### ✅ Mensajes normales (todo bien)

```
[2026-07-17 08:00:01] [INFO] Iniciando Project Scheduler v1.0
[2026-07-17 08:00:02] [INFO] Autenticación con Google exitosa
[2026-07-17 08:00:03] [INFO] Carpeta 'Proyectos_Empresa' encontrada. ID: 1xxxxx...
[2026-07-17 08:00:04] [INFO] Sheet 'Cronograma_Ingeniería' encontrado. ID: 1xxxxx...
[2026-07-17 08:00:05] [INFO] Leyendo datos de 3 departamentos...
[2026-07-17 08:00:06] [INFO] Consolidación completada: 15 proyectos totales
[2026-07-17 08:00:07] [INFO] Alertas evaluadas: 2 alertas generadas
[2026-07-17 08:00:08] [INFO] Ejecución finalizada exitosamente
```

> **Interpretación:** Todo funcionó perfecto. Hay 15 proyectos en total y 2 necesitan atención.

---

#### ⚠️ Mensajes de advertencia (revisar)

```
[2026-07-17 08:00:15] [WARNING] ALERTA: PROXIMO_A_VENCER
  Proyecto: PROJ-005
  Cliente: Edificios del Sur S.A.
  Departamento: Obras
  Fecha de entrega: 20/07/2026
  Días restantes: 3
  Estado actual: En progreso
  Responsable: maria@empresa.com
  Mensaje: Proyecto PROJ-005 vence en 3 días
```

> **Interpretación:** El proyecto PROJ-005 del departamento de Obras vence en 3 días y aún no está completado. El responsable (maria@empresa.com) debería ser notificado.

```
[2026-07-17 08:00:16] [WARNING] ALERTA: VENCIDO
  Proyecto: PROJ-003
  Cliente: Constructora XYZ
  Departamento: Ingeniería
  Fecha de entrega: 15/07/2026
  Días restantes: -2
  Estado actual: Pendiente
  Responsable: juan@empresa.com
  Mensaje: Proyecto PROJ-003 VENCIDO hace 2 días
```

> **Interpretación:** El proyecto PROJ-003 ya debería haberse entregado (venció hace 2 días) pero sigue en estado "Pendiente". Requiere acción inmediata.

---

#### ❌ Mensajes de error (corregir)

```
[2026-07-17 08:00:10] [ERROR] No se pudo leer Sheet 'Cronograma_Obras'
  ID: 1xxxxx...
  Error: HttpError 403: Permission denied
  Acción: Verificar que la cuenta de servicio tenga permisos de Editor
```

> **Interpretación:** El script no pudo leer el cronograma de Obras. Probablemente la cuenta de servicio no tiene permisos sobre ese Sheet. Ve a la sección "Error 3" de este troubleshooting.

```
[2026-07-17 08:00:11] [ERROR] Fecha mal formateada en fila 5
  Valor: '2026-07-18'
  Columna: Fecha_Entrega
  Departamento: Mantenimiento
  Acción: Corregir a formato DD/MM/YYYY (ej: 18/07/2026)
```

> **Interpretación:** Alguien escribió la fecha en formato incorrecto (ISO en vez de DD/MM/YYYY). Corrige la celda en el Sheet.

```
[2026-07-17 08:00:12] [ERROR] Estado inválido en fila 3
  Valor: 'En proceso'
  Valores válidos: Pendiente, En progreso, Completado, Retrasado
  Departamento: Ingeniería
  Acción: Corregir a 'En progreso' (con espacio)
```

> **Interpretación:** Alguien escribió "En proceso" en vez de "En progreso". El script no reconoce el estado y ignora esa fila.

---

#### 🔴 Mensajes críticos (detener y corregir)

```
[2026-07-17 08:00:01] [CRITICAL] No se encontró archivo de credenciales
  Ruta: ./credentials.json
  Acción: Descargar credentials.json desde Google Cloud Console
```

> **Interpretación:** El script no puede arrancar sin credenciales. Detenido. Descarga el archivo JSON de Google Cloud.

```
[2026-07-17 08:00:02] [CRITICAL] Fallo de autenticación con Google
  Error: invalid_grant
  Causa probable: La clave JSON fue revocada o expiró
  Acción: Generar una nueva clave en Google Cloud Console
```

> **Interpretación:** Las credenciales no son válidas. Puede que hayas borrado la clave en Google Cloud o haya expirado. Genera una nueva.

---

### Cómo diagnosticar problemas viendo los logs

**Regla general:** Lee el log de arriba hacia abajo. El primer error que aparece suele ser la causa raíz; los errores siguientes son consecuencia del primero.

**Ejemplo de diagnóstico:**

```
[08:00:01] [INFO] Iniciando...
[08:00:02] [INFO] Autenticación exitosa
[08:00:03] [ERROR] No se pudo leer Sheet 'Cronograma_Obras'  ← 🎯 CAUSA RAÍZ
[08:00:04] [ERROR] Consolidación fallida: datos incompletos   ← Consecuencia
[08:00:05] [ERROR] No se pudo escribir en Maestro             ← Consecuencia
[08:00:06] [WARNING] 0 alertas evaluadas                      ← Consecuencia
```

> **Diagnóstico:** El problema real es que no pudo leer el Sheet de Obras. Si arreglas eso, todo lo demás se arregla solo.

**Comando útil para filtrar solo errores:**

```bash
# Linux/Mac
grep "ERROR\|CRITICAL\|WARNING" alertas_cronograma.log

# Windows (PowerShell)
Select-String -Path alertas_cronograma.log -Pattern "ERROR|CRITICAL|WARNING"
```

**Comando útil para ver las últimas líneas (ejecución más reciente):**

```bash
# Linux/Mac
tail -50 alertas_cronograma.log

# Windows (PowerShell)
Get-Content alertas_cronograma.log -Tail 50
```


## 💾 Backup y Recuperación

### Backup automático (Google Sheets)

Google Sheets guarda automáticamente un historial de versiones:

1. Abre cualquier Sheet
2. Ve a **Archivo → Historial de versiones → Ver historial de versiones**
3. Puedes ver quién hizo qué cambio y cuándo
4. Puedes **restaurar** una versión anterior si alguien borró algo por error

### Backup manual (exportar a Excel)

1. Abre el Cronograma Maestro
2. Ve a **Archivo → Descargar → Microsoft Excel (.xlsx)**
3. Guarda el archivo en tu computadora como respaldo

---

## 🔒 Seguridad y Permisos

### Quién puede ver qué

| Elemento | Quién lo ve | Cómo controlarlo |
|----------|------------|------------------|
| Carpeta `Proyectos_Empresa` | Quien tenga el link o esté compartido | Compartir solo con emails específicos en Drive |
| Sheets departamentales | Mismo que arriba | Ajustar permisos en cada Sheet individualmente |
| Cronograma Maestro | Mismo que arriba | Ajustar permisos en el Sheet |
| `credentials.json` | Solo tú (en tu PC) | Nunca subirlo a GitHub ni compartirlo |
| `.env` | Solo tú (en tu PC) | Está protegido por `.gitignore` |

### Buenas prácticas de seguridad

- 🔐 **Nunca subas `credentials.json` ni `.env` a internet.** El `.gitignore` ya los protege si usas Git.
- 🔐 **Comparte los Sheets solo con quienes necesiten verlos.** No uses "Cualquiera con el link" si los datos son sensibles.
- 🔐 **Revisa quién tiene acceso** a la carpeta `Proyectos_Empresa` en Drive periódicamente.
- 🔐 **Si un empleado se va**, quítale el acceso a los Sheets y a la carpeta de Drive.

---

## 🗑️ Cómo Desinstalar / Empezar de Cero

Si necesitas borrar todo y empezar de nuevo:

### 1. Borrar en Google Drive

1. Ve a tu Google Drive
2. Busca la carpeta `Proyectos_Empresa`
3. Selecciónala y presiona `Suprimir` (o `Shift + Suprimir` para borrar permanentemente)
4. También borra los Sheets individuales si quedaron sueltos

### 2. Borrar archivos locales

```bash
cd "/home/german/Escritorio/drive fer/project_scheduler"
rm .env                    # Borra configuración con IDs
rm credentials.json        # Borra credenciales de Google
rm alertas_cronograma.log # Borra logs
rm -rf logs/               # Borra carpeta de logs
```

### 3. Volver a empezar

Sigue esta guía desde el **Paso 3** (configurar `.env`). El script creará todo de nuevo.

---

## 📖 Glosario de Términos Técnicos

| Término | Qué significa | En este proyecto |
|---------|-------------|------------------|
| **API** | Interfaz de Programación de Aplicaciones. Es cómo dos programas se comunican. | El script usa la API de Google para hablar con Drive y Sheets. |
| **Cuenta de Servicio** | Un tipo de usuario "robot" de Google que actúa sin intervención humana. | Es quien crea las carpetas y Sheets automáticamente. |
| **Consolidación** | Proceso de unir datos de varias fuentes en una sola. | Unir los 3 cronogramas departamentales en el Maestro. |
| **Cron job** | Tarea programada en Linux/Mac que se ejecuta automáticamente. | Ejecutar `main.py` todos los días a las 8 AM. |
| **DataFrame** | Estructura de datos de `pandas`, similar a una tabla de Excel. | Usado en `consolidator.py` para unir los proyectos. |
| **.env** | Archivo de variables de entorno. Guarda configuración sensible. | Contiene IDs de carpetas, emails, contraseñas SMTP. |
| **JSON** | Formato de archivo para intercambiar datos. | El `credentials.json` contiene las claves de Google. |
| **OAuth2** | Protocolo de autenticación. | La cuenta de servicio usa OAuth2 para conectarse a Google. |
| **SMTP** | Protocolo para enviar emails. | Usado en `notifier.py` para enviar alertas por correo. |
| **Service Account** | Lo mismo que "Cuenta de Servicio", en inglés. | Ver arriba. |

---

## 🆘 Solución de Problemas Comunes

Si algo no funciona, aquí están los errores más frecuentes y sus soluciones:

### "ModuleNotFoundError: No module named 'googleapiclient'"

**Causa:** Las dependencias de Google Cloud no están instaladas.

**Solución:**
```bash
pip install -r requirements.txt
```

Si sigue sin funcionar, prueba:
```bash
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

---

### "FileNotFoundError: credentials.json not found"

**Causa:** El archivo `credentials.json` no está en la carpeta del proyecto.

**Solución:**
1. Ve a [Google Cloud Console](https://console.cloud.google.com/iam-admin/serviceaccounts)
2. Descarga el archivo JSON de tu cuenta de servicio
3. Cópialo a la carpeta del proyecto: `/home/german/Escritorio/drive fer/project_scheduler/credentials.json`
4. Asegúrate de que el nombre sea exactamente `credentials.json` (minúsculas)

---

### "HttpError 403: Permission denied"

**Causa:** La cuenta de servicio no tiene permisos para acceder a Drive o Sheets.

**Solución:**

1. **Obtén el email de la cuenta de servicio:**
   - Ve a [Google Cloud Console](https://console.cloud.google.com/iam-admin/serviceaccounts)
   - Haz clic en tu cuenta de servicio
   - Copia el **"Dirección de correo electrónico"** (formato: `xxxx@xxxx.iam.gserviceaccount.com`)

2. **Comparte la carpeta raíz:**
   - Ve a [Google Drive](https://drive.google.com)
   - Haz clic derecho en `Proyectos_Empresa`
   - Selecciona **"Compartir"**
   - Pega el email de la cuenta de servicio
   - Dale permisos de **"Editor"**
   - Haz clic en **"Enviar"**

3. **Verifica que las APIs estén habilitadas:**
   - Ve a [Google Cloud Console - Biblioteca de APIs](https://console.cloud.google.com/apis/library)
   - Busca y verifica que estén habilitadas:
     - ✅ Google Drive API
     - ✅ Google Sheets API

---

### "Las alertas no se envían por email"

**Causa:** Configuración SMTP incorrecta o credenciales inválidas.

**Solución:**

1. **Verifica que SMTP_USER y SMTP_PASSWORD estén en `.env`:**
```bash
SMTP_USER=tu_email@gmail.com
SMTP_PASSWORD=tu_app_password
```

2. **Si usas Gmail, debes usar "App Password" (no tu contraseña normal):**
   - Ve a [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
   - Inicia sesión
   - En "Seleccionar app", elige **"Otra"** y escribe `Project Scheduler`
   - Haz clic en **"Generar"**
   - Copia la contraseña de 16 caracteres y pégala en `SMTP_PASSWORD`

3. **Verifica que ALERT_RECIPIENTS tenga emails válidos:**
```bash
# ✅ Correcto (separados por coma):
ALERT_RECIPIENTS=gerente@empresa.com,director@empresa.com

# ❌ Incorrecto:
ALERT_RECIPIENTS=gerente@empresa.com director@empresa.com  # Sin coma
ALERT_RECIPIENTS=gerente@empresa.com,               # Vacío al final
```

4. **Si aún no funciona, revisa el log:**
```bash
cat alertas_cronograma.log | grep -i smtp
# o
cat alertas_cronograma.log | grep -i error
```

---

### "El script crea carpetas/Sheets duplicados cada vez que se ejecuta"

**Causa:** Los IDs no se guardan en `.env` o el archivo no se está leyendo correctamente.

**Solución:**

1. **Verifica que el archivo `.env` exista:**
```bash
ls -la .env
```

Si no existe, crea uno:
```bash
cp .env.example .env
```

2. **Verifica que `.env` tenga los IDs después de la primera ejecución:**
```bash
cat .env | grep SHEET
cat .env | grep DRIVE_ROOT_FOLDER_ID
```

Deberías ver valores, no líneas vacías:
```bash
DRIVE_ROOT_FOLDER_ID=1abc123xyz...
SHEET_INGENIERIA_ID=1def456xyz...
```

Si están vacíos, el problema es que no se guardan. Revisa el log:
```bash
cat logs/project_scheduler.log | grep -i "save\|write\|update"
```

3. **Asegúrate de que `python-dotenv` esté instalado:**
```bash
pip install python-dotenv
```

---

### "Formato de fecha incorrecto: Expected DD/MM/YYYY"

**Causa:** Escribiste una fecha en formato incorrecto en los Sheets.

**Solución:**

1. **Verifica el formato:** Debe ser **DD/MM/YYYY** (día/mes/año)

| ✅ Correcto | ❌ Incorrecto |
|-----------|-------------|
| 18/07/2026 | 2026-07-18 |
| 01/12/2026 | 07/18/2026 |
| 25/03/2026 | 18-07-2026 |

2. **Si Google Sheets auto-convierte el formato:**
   - Google Sheets a veces convierte automáticamente a otro formato
   - Solución: Haz clic en la celda → **Formato → Número → Personalizado**
   - Escribe el formato: `DD/MM/YYYY`

---

### "Estado no válido: xxx no está en ['Pendiente', 'En progreso', 'Completado', 'Retrasado']"

**Causa:** Escribiste el estado con diferente ortografía o capitalización.

**Solución:**

Los estados DEBEN escribirse **exactamente** así (con mayúsculas/minúsculas exactas):
- ✅ `Pendiente`
- ✅ `En progreso`
- ✅ `Completado`
- ✅ `Retrasado`

| ❌ Incorrecto | ✅ Correcto |
|-------------|-----------|
| "PENDIENTE" | "Pendiente" |
| "En Progreso" | "En progreso" |
| "completado" | "Completado" |
| "En proceso" | "En progreso" |

**Tip:** Usa validación de datos en Google Sheets para crear una lista desplegable:
1. Selecciona la columna F (Estado)
2. Ve a **Datos → Validación de datos**
3. Tipo: **Lista de elementos**
4. Elementos: Escribe: `Pendiente,En progreso,Completado,Retrasado`
5. Haz clic en **"Guardar"**

---

### "El script se ejecuta pero no consolida los datos"

**Causa:** No hay datos en los Sheets departamentales o hay un error silencioso.

**Solución:**

1. **Verifica que hay datos en los Sheets:**
   - Abre cada uno: `Cronograma_Ingeniería`, `Cronograma_Obras`, `Cronograma_Mantenimiento`
   - Verifica que haya al menos una fila de datos (no solo encabezados)

2. **Revisa el log para ver qué sucedió:**
```bash
cat alertas_cronograma.log
# o
cat logs/project_scheduler.log
```

Busca mensajes de error o advertencias:
```bash
cat logs/project_scheduler.log | grep -i "error\|warning\|consolidat"
```

3. **Si el log no muestra nada, aumenta el nivel de logging:**
   - Edita `.env` y agrega: `LOG_LEVEL=DEBUG`
   - Ejecuta de nuevo: `python main.py`
   - Esto generará más detalles en el log

---

### "No veo la carpeta Proyectos_Empresa en MI Google Drive"

**Causa:** La carpeta fue creada pero pertenece a la cuenta de servicio, no a tu cuenta personal.

**Solución:**

**Opción A: Compartir desde la cuenta de servicio (recomendado)**
1. Crea manualmente una carpeta `Proyectos_Empresa` en TU Drive
2. Copia su ID (está en la URL: `https://drive.google.com/drive/folders/1xxxID_ACÁxxxxx`)
3. Pégalo en `.env` como: `DRIVE_ROOT_FOLDER_ID=1xxxID_ACÁxxxxx`
4. Comparte esa carpeta con el email de la cuenta de servicio (como se explica en Paso 4)
5. Ejecuta `python main.py`

**Opción B: Buscar la carpeta existente**
1. Ve a [https://drive.google.com](https://drive.google.com)
2. Busca: `Proyectos_Empresa`
3. Si aparece, haz clic en ella → copia el ID de la URL
4. Pégalo en `.env` como: `DRIVE_ROOT_FOLDER_ID=...`

---

### "Se ejecutó pero dice 'Connection timeout' o 'Network error'"

**Causa:** Problema de conexión a Internet o Google rechazó la solicitud.

**Solución:**

1. **Verifica tu conexión a Internet:**
```bash
ping google.com
```

2. **Espera un momento y reintenta:**
```bash
sleep 60  # Espera 60 segundos
python main.py
```

3. **Si es un problema de cuota:**
   - Google Cloud tiene límites de solicitudes por minuto
   - Espera 1 minuto antes de ejecutar de nuevo

4. **Revisa si tu IP fue bloqueada:**
   - A veces Google bloquea IPs que hacen muchas solicitudes
   - Intenta desde otra red o usa una VPN

---

### "¿Cómo interpretar los logs?"

**Niveles de log:**

```
[INFO]      - Información normal. Todo va bien. (verde)
[WARNING]   - Advertencia. Algo podría no ser perfecto. (amarillo)
[ERROR]     - Error. Algo falló. (rojo)
[DEBUG]     - Información detallada para debugging. (gris)
```

**Ejemplos de logs normales (no es error):**

```
[INFO] Iniciando Project Scheduler
[INFO] Carpeta 'Proyectos_Empresa' creada con ID: 1abc123...
[INFO] Sheet 'Cronograma_Ingeniería' creado con ID: 1def456...
[INFO] Consolidación completada: 5 proyectos
[INFO] Alertas evaluadas: 2 alertas generadas
[INFO] Ejecución finalizada exitosamente
```

**Ejemplos de logs con problemas:**

```
[WARNING] Algunos proyectos con fechas inválidas
[ERROR] No se pudo conectar a Google Drive API
[ERROR] El email de la cuenta de servicio no tiene permisos
```

---

## 📋 Checklist Final

Antes de considerar el proyecto operativo, verifica:

- [ ] `pip install -r requirements.txt` ejecutado sin errores
- [ ] `credentials.json` descargado de Google Cloud y en la carpeta del proyecto
- [ ] APIs de Drive y Sheets habilitadas en Google Cloud Console
- [ ] Cuenta de servicio creada con rol "Editor"
- [ ] Archivo `.env` configurado con mis datos
- [ ] Carpeta `Proyectos_Empresa` compartida con el email de la cuenta de servicio
- [ ] Primera ejecución de `python main.py` completada sin errores
- [ ] Carpetas y Sheets creados visibles en Google Drive
- [ ] IDs guardados automáticamente en `.env`
- [ ] Log de ejecución generado sin errores críticos
- [ ] Proyecto de prueba agregado y consolidado en el Maestro
- [ ] Alerta generada correctamente en el log
- [ ] Email de alerta recibido (si configuraste SMTP)
- [ ] Scripts de ejemplo ejecutados y funcionando
- [ ] Tests unitarios pasados (`python test_suite.py`)
- [ ] Entiendo que NO debo editar el Maestro manualmente
- [ ] Sé cómo agregar proyectos reales en los Sheets departamentales
- [ ] Sé cómo ejecutar el script regularmente (cron o manual)
- [ ] Sé cómo agregar un nuevo departamento si es necesario

---

*Guía generada para facilitar la puesta en marcha del sistema de planificación de proyectos. Versión 2.0 — incluye todas las mejoras solicitadas.*
