# 🚀 INICIO RÁPIDO - Menú Interactivo Gmail

## 5 Pasos para Comenzar

### Paso 1️⃣: Navega a la carpeta del proyecto
```bash
cd "proyecto drive fer"
```

### Paso 2️⃣: Instala dependencias (si aún no las has instalado)
```bash
pip install -r requirements.txt
```

### Paso 3️⃣: Verifica que todo funciona
```bash
python test_menu.py
```
Deberías ver: `✅ ALL TESTS PASSED`

### Paso 4️⃣: Ejecuta el menú interactivo
```bash
python main.py
```

### Paso 5️⃣: Agrega tu cuenta Gmail
En el menú, selecciona:
- **"Agregar Nueva Cuenta"**
- Ingresa tu email: `tu_email@gmail.com`
- Ingresa nombre (ej: "Personal" o "Trabajo")
- Ingresa ruta de credenciales JSON: `/ruta/a/tu/credenciales.json`
- El menú guarda automáticamente ✅

---

## 📝 Usando Credenciales Guardadas

Una vez que hayas agregado una cuenta, la próxima vez solo necesitas:

```bash
python main.py
```

Y selecciona tu cuenta del listado. ¡Eso es todo!

---

## 🔐 ¿Cómo obtener archivo de credenciales?

1. Ve a [Google Cloud Console](https://console.cloud.google.com)
2. Crea un proyecto o usa uno existente
3. Habilita APIs: Drive, Sheets, Gmail
4. Crea una "Service Account"
5. Descarga el JSON de credenciales
6. Guarda el archivo en una ubicación conocida

Ejemplo:
```
~/credenciales/drive-project.json
```

---

## ⚡ Modo Avanzado (Sin menú)

Si quieres saltarte el menú y especificar credenciales directamente:

```bash
python main.py ~/credenciales/drive-project.json
```

---

## ❓ ¿Algo no funciona?

### Error: "File not found"
→ Verifica que la ruta al archivo de credenciales sea correcta

### Error: "Invalid email format"
→ Usa un email válido (ejemplo: usuario@gmail.com)

### Error: "Module not found"
→ Ejecuta: `pip install -r requirements.txt`

---

## 📚 Más Información

- [MENU_INTERACTIVO.md](MENU_INTERACTIVO.md) - Guía completa
- [CAMBIOS_MENU_INTERACTIVO.md](CAMBIOS_MENU_INTERACTIVO.md) - Cambios realizados
- [README.md](README.md) - Documentación general

---

## ✨ ¡Listo!

Tu proyecto ahora tiene un menú interactivo amigable para seleccionar cuentas Gmail. 

Ejecuta:
```bash
python main.py
```

¡Y comienza! 🎉
