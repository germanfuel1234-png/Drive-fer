# 📊 Lógica del Sheet Maestro y Consolidación

## 🎯 Objetivo del Proyecto

**Traer un reporte semanal** con todos los proyectos de:
- Ingeniería
- Obras  
- Mantenimiento

---

## 📋 Cómo Funciona la Consolidación

```
┌─────────────────────────────────────────────────────────┐
│         SHEETS DEPARTAMENTALES (Read)                   │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Cronograma_Ingeniería     Cronograma_Obras            │
│  ┌─────────────────────┐  ┌─────────────────────┐      │
│  │ ID | Cliente | ...  │  │ ID | Cliente | ...  │      │
│  │ 001| ABC Inc | ...  │  │ 101| XYZ Corp| ...  │      │
│  │ 002| DEF Ltd | ...  │  │ 102| 123 Inc | ...  │      │
│  └─────────────────────┘  └─────────────────────┘      │
│                                                           │
│  Cronograma_Mantenimiento                               │
│  ┌─────────────────────┐                                │
│  │ ID | Cliente | ...  │                                │
│  │ 201| ABC Inc | ...  │                                │
│  │ 202| DEF Ltd | ...  │                                │
│  └─────────────────────┘                                │
│                                                           │
└─────────────────────────────────────────────────────────┘
                          ↓
           ┌──────────────────────────────┐
           │  CONSOLIDADOR (Combina)      │
           │  - Lee 3 sheets              │
           │  - Agrega columna Dept.      │
           │  - Filtra vacíos             │
           └──────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│         SHEET MAESTRO (Write)                           │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Cronograma_Maestro                                      │
│  ┌─────────────────────────────────────────────────┐   │
│  │ ID  | Cliente | ... | Departamento             │   │
│  ├─────────────────────────────────────────────────┤   │
│  │ 001 | ABC Inc | ... | Ingeniería               │   │
│  │ 002 | DEF Ltd | ... | Ingeniería               │   │
│  │ 101 | XYZ Corp| ... | Obras                    │   │
│  │ 102 | 123 Inc | ... | Obras                    │   │
│  │ 201 | ABC Inc | ... | Mantenimiento            │   │
│  │ 202 | DEF Ltd | ... | Mantenimiento            │   │
│  └─────────────────────────────────────────────────┘   │
│                                                           │
│  ✨ RESULTADO: Todos los proyectos en UNA hoja         │
│                Con referencia del departamento          │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 📅 Lógica de Fechas (IMPORTANTE)

### ❌ LO QUE NO HACE:
- **NO filtra por fecha de inicio**
- **NO trae solo "esta semana"**
- **Trae TODOS los proyectos** que no estén "Completado"

### ✅ LO QUE SÍ HACE:
Genera **ALERTAS** basadas en `Fecha_Entrega`:

```
HOY: 18/07/2026

Proyecto A → Fecha_Entrega: 16/07/2026 (VENCIDO)
Proyecto B → Fecha_Entrega: 18/07/2026 (Plazo hoy)
Proyecto C → Fecha_Entrega: 19/07/2026 (Plazo mañana)  
Proyecto D → Fecha_Entrega: 21/07/2026 (Plazo en 3 días)
Proyecto E → Fecha_Entrega: 25/07/2026 (Normal)

                       ↓

ALERTAS GENERADAS:

🔴 VENCIDOS: A (hace 2 días)
🟡 PRÓXIMOS (en ≤3 días): B, C, D
✅ NORMALES: E
```

---

## ⚙️ Configuración de Fechas

**Archivo**: `config.py`

```python
# Umbral de días para alerta "próximo"
ALERT_DAYS_THRESHOLD = 3  # Por defecto: alerta en 3 días

# Formato de fecha esperado en las hojas
DATE_FORMAT = '%d/%m/%Y'  # Ejemplo: 18/07/2026
```

---

## 📊 Columnas Esperadas en las Hojas

Cada sheet departamental debe tener estas columnas:

| Columna | Descripción | Tipo | Obligatorio |
|---------|-------------|------|-------------|
| **ID_Proyecto** | Código único | Texto | ✅ |
| **Cliente** | Nombre del cliente | Texto | ✅ |
| **Descripcion** | Descripción del proyecto | Texto | ✅ |
| **Fecha_Inicio** | Inicio del proyecto | DD/MM/YYYY | ✅ |
| **Fecha_Entrega** | Fecha de vencimiento | DD/MM/YYYY | ✅ |
| **Estado** | Pendiente/En progreso/Completado/Retrasado | Texto | ✅ |
| **Responsable** | Persona a cargo | Texto | ✅ |

### Valores válidos para "Estado":
- `Pendiente`
- `En progreso`
- `Completado` (se excluye de alertas)
- `Retrasado`

---

## 🔄 Flujo Completo de Ejecución

```
1️⃣ AUTENTICACIÓN (OAuth)
   ↓
2️⃣ CREAR/OBTENER CARPETAS
   - Proyectos_Empresa (raíz)
   - Ingeniería → Clientes
   - Obras → Clientes
   - Mantenimiento → Clientes
   ↓
3️⃣ CREAR/OBTENER HOJAS
   - Cronograma_Ingeniería
   - Cronograma_Obras
   - Cronograma_Mantenimiento
   - Cronograma_Maestro
   ↓
4️⃣ LEER DATOS de 3 departamentos
   ↓
5️⃣ CONSOLIDAR en Sheet Maestro
   (agregar columna Departamento)
   ↓
6️⃣ EVALUAR ALERTAS
   - ¿Vencidos? (Fecha_Entrega < HOY)
   - ¿Próximos? (0 ≤ días_restantes ≤ 3)
   ↓
7️⃣ REGISTRAR ALERTAS en log
   ↓
8️⃣ (Opcional) ENVIAR EMAIL
   - Si SMTP configurado
```

---

## 🎯 ¿Qué Quieres Cambiar?

Tienes varias opciones:

### Opción A: Filtrar por Semana
**Traer solo proyectos que empiezan/terminan esta semana**

```python
# Ejemplo: traer solo proyectos con entrega entre HOY y HOY+7 días
TODAY = 18/07/2026
WEEK_END = 25/07/2026
Filtro: Fecha_Entrega >= 18/07/2026 AND Fecha_Entrega <= 25/07/2026
```

### Opción B: Filtrar por Rango de Fechas
**Traer proyectos en un rango específico**

```python
# Parámetro: fecha_inicio, fecha_fin
# Filtro: Fecha_Entrega >= fecha_inicio AND Fecha_Entrega <= fecha_fin
```

### Opción C: Traer por Estado
**Solo proyectos "En progreso" (excluyendo Completado y Pendiente)**

```python
# Filtro: Estado IN ['En progreso', 'Retrasado']
```

### Opción D: Combinar Múltiples Filtros
**Ejemplo: "Este mes, En progreso, con plazo próximo"**

---

## 📋 Estructura Actual del Consolidador

```python
# config.py
DEPARTMENT_SHEET_HEADERS = [
    'ID_Proyecto',
    'Cliente',
    'Descripcion',
    'Fecha_Inicio',
    'Fecha_Entrega',
    'Estado',
    'Responsable'
]

MASTER_SHEET_HEADERS = DEPARTMENT_SHEET_HEADERS + ['Departamento']
```

---

## ❓ Preguntas Frecuentes

**P: ¿Trae datos solo de esta semana?**  
R: No, trae TODO. Pero genera alertas para vencidos y próximos.

**P: ¿Puedo cambiar el umbral de 3 días?**  
R: Sí, en `config.py`: `ALERT_DAYS_THRESHOLD = 5`

**P: ¿Qué pasa si cambio una hoja departamental?**  
R: La próxima ejecución actualiza el Sheet Maestro automáticamente.

**P: ¿Se pueden agregar más departamentos?**  
R: Sí, modificar `config.py`: `DEPARTMENTS = 'Ingeniería,Obras,Mantenimiento,Diseño'`

---

## 🔧 Próximas Acciones Sugeridas

1. **¿Quieres que implemente filtros por fecha?** (ej: solo esta semana)
2. **¿Cambiar el formato de reporte?** (ej: JSON, CSV)
3. **¿Agregar más departamentos?**
4. **¿Mejorar la lógica de alertas?** (ej: prioridades, colores)

**¿Qué necesitas específicamente?** 🎯
