# 🔐 OAuth Setup - Configuración de Google Cloud

Para usar la autenticación OAuth interactivo (que se abre en tu navegador), necesitas un archivo `credentials.json` de Google Cloud Console.

## 📋 Pasos para Obtener credentials.json

### Paso 1: Ir a Google Cloud Console

1. Abre https://console.cloud.google.com/
2. Inicia sesión con tu cuenta de Google
3. **Crea un nuevo proyecto** o selecciona uno existente

### Paso 2: Habilitar APIs

1. Abre el menú "APIs & Services" → "Library"
2. Busca y habilita las siguientes APIs:
   - ✅ **Google Drive API**
   - ✅ **Google Sheets API**
   - ✅ **Gmail API**

### Paso 3: Crear Credenciales OAuth

1. Ve a "APIs & Services" → "Credentials"
2. Haz clic en **"+ Create Credentials"** → **"OAuth 2.0 Client ID"**
3. Si te pide una pantalla de consentimiento, configúrala:
   - **User type**: External
   - **App name**: "Proyecto Scheduler" (o el que prefieras)
   - **Email**: Tu email de Google
   - **Permisos**: Deja los defaults
4. En "Credenciales", selecciona **"Desktop application"** (o "Other")
5. Haz clic en crear

### Paso 4: Descargar credentials.json

1. En la tabla de "OAuth 2.0 Client IDs", encontrarás un cliente recién creado
2. Haz clic en el icono de descarga (↓) a la derecha
3. Se descargará un archivo llamado `credentials.json`

### Paso 5: Colocar el Archivo

Coloca el archivo `credentials.json` en:
```
/home/german/Escritorio/drive fer/proyecto drive fer/credentials.json
```

**Exactamente en la misma carpeta que `main.py`**

---

## 🚀 Usar el Menú OAuth

Una vez que tengas `credentials.json` en la carpeta correcta:

```bash
cd "proyecto drive fer"
python main.py
```

El menú mostrará:
```
📧 GMAIL ACCOUNT SELECTOR
============================================================

📌 NO SAVED ACCOUNTS FOUND
  1. ➕ Add New Account
  2. ❌ Exit

🔹 Enter your choice: 1
```

Elige **"Add New Account"** y sigue los pasos:

1. **Ingresa tu email de Gmail** (ejemplo: `germanty123@gmail.com`)
2. **Ingresa nombre/descripción** (ejemplo: "Personal")
3. **Se abrirá tu navegador** para autenticación
4. **Inicia sesión** con tu cuenta de Gmail
5. **Autoriza** el acceso a Drive, Sheets y Gmail
6. **Vuelve a la terminal** (se cerrará automáticamente)
7. ✅ **¡Cuenta guardada y lista para usar!**

---

## 🔒 Seguridad

- ✅ El archivo `credentials.json` se mantiene **local**
- ✅ Los tokens de OAuth se guardan en `.gmail_tokens/`
- ✅ No se envían credenciales a servidores externos
- ✅ Los tokens se actualizan automáticamente

---

## 📁 Estructura de Archivos

```
proyecto drive fer/
├── credentials.json          ← Descarga de Google Cloud (MANTENER PRIVADO)
├── .gmail_accounts.json      ← Cuentas guardadas (autogenerado)
├── .gmail_tokens/
│   ├── germanty123_gmail_com_token.json
│   └── ...
├── main.py
└── menu.py
```

---

## ❓ Troubleshooting

### Problema: "No se encontró 'credentials.json'"
**Solución**: Descarga el archivo desde Google Cloud Console (Paso 4) y colócalo en la carpeta del proyecto.

### Problema: "El navegador no se abrió"
**Solución**: Abre manualmente http://localhost:8080/ en tu navegador mientras el menú espera.

### Problema: "Error de autenticación"
**Solución**: 
1. Verifica que las APIs estén habilitadas (Drive, Sheets, Gmail)
2. Revisa que `credentials.json` sea válido
3. Intenta eliminar tokens antiguos en `.gmail_tokens/`

### Problema: "This app isn't verified"
**Solución**: Haz clic en "Advanced" → "Go to Proyecto Scheduler (unsafe)" (es seguro, es tu propia app)

---

## ✅ Listo

Una vez completado este setup, tu cuenta estará guardada y podrás:

```bash
python main.py
```

Y simplemente seleccionar tu cuenta del menú. 🎉

---

**Más info**: https://developers.google.com/identity/protocols/oauth2
