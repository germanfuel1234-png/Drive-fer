"""
Quick Start Script - Inicio Rápido
Ejecuta esto después de configurar las credenciales para verificar que todo funciona
"""

import sys
import os
from pathlib import Path

def check_files():
    """Verifica que todos los archivos necesarios existen"""
    print("=" * 60)
    print("VERIFICANDO ARCHIVOS DEL PROYECTO")
    print("=" * 60)
    
    required_files = [
        'main.py',
        'config.py',
        'requirements.txt',
        '.env.example',
        'modules/__init__.py',
        'modules/drive_manager.py',
        'modules/sheets_manager.py',
        'modules/scheduler_manager.py',
        'modules/notifications.py',
        'README.md',
        'SETUP.md'
    ]
    
    all_exist = True
    for file in required_files:
        path = Path(file)
        if path.exists():
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - NO ENCONTRADO")
            all_exist = False
    
    print()
    return all_exist


def check_dependencies():
    """Verifica que las dependencias están instaladas"""
    print("=" * 60)
    print("VERIFICANDO DEPENDENCIAS")
    print("=" * 60)
    
    dependencies = [
        'google.api_core',
        'google.auth',
        'googleapiclient',
        'dotenv',
        'pandas'
    ]
    
    all_installed = True
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✓ {dep}")
        except ImportError:
            print(f"✗ {dep} - NO INSTALADO")
            all_installed = False
    
    print()
    return all_installed


def check_credentials():
    """Verifica que el archivo de credenciales existe"""
    print("=" * 60)
    print("VERIFICANDO CREDENCIALES")
    print("=" * 60)
    
    creds_file = Path('credentials.json')
    if creds_file.exists():
        print("✓ credentials.json encontrado")
        # Verificar que es un JSON válido
        try:
            import json
            with open(creds_file) as f:
                data = json.load(f)
                if 'client_email' in data:
                    print(f"✓ Cuenta de servicio: {data['client_email']}")
                    print()
                    return True
        except json.JSONDecodeError:
            print("✗ credentials.json inválido")
            return False
    else:
        print("✗ credentials.json NO ENCONTRADO")
        print("\nPor favor:")
        print("1. Ve a https://console.cloud.google.com/")
        print("2. Crea una clave de servicio")
        print("3. Descarga el JSON y guárdalo como 'credentials.json'")
        print()
        return False


def check_env():
    """Verifica la configuración de variables de entorno"""
    print("=" * 60)
    print("VERIFICANDO CONFIGURACIÓN (.env)")
    print("=" * 60)
    
    env_file = Path('.env')
    if env_file.exists():
        print("✓ .env encontrado")
        with open(env_file) as f:
            lines = f.readlines()
            for line in lines[:5]:  # Mostrar primeras 5 líneas
                if not line.startswith('#') and '=' in line:
                    key = line.split('=')[0]
                    print(f"  ✓ {key}")
        print()
        return True
    else:
        print("⚠ .env NO ENCONTRADO")
        print("  → Creando .env desde .env.example...")
        if Path('.env.example').exists():
            with open('.env.example') as src, open('.env', 'w') as dst:
                dst.write(src.read())
            print("  ✓ .env creado")
            print()
            return True
        else:
            print("  ✗ .env.example no encontrado")
            print()
            return False


def test_import():
    """Prueba que los módulos se pueden importar"""
    print("=" * 60)
    print("VERIFICANDO MÓDULOS PYTHON")
    print("=" * 60)
    
    try:
        from config import Config
        print("✓ config.py importado correctamente")
        
        from modules import DriveManager, SheetsManager, SchedulerManager, NotificationManager
        print("✓ modules importados correctamente")
        
        from main import ProjectScheduler
        print("✓ main.py importado correctamente")
        
        print()
        return True
    except ImportError as e:
        print(f"✗ Error al importar módulos: {str(e)}")
        print()
        return False


def test_google_auth():
    """Prueba la autenticación con Google"""
    print("=" * 60)
    print("PROBANDO AUTENTICACIÓN CON GOOGLE")
    print("=" * 60)
    
    try:
        from google.oauth2.service_account import Credentials
        from pathlib import Path
        
        creds_file = Path('credentials.json')
        if not creds_file.exists():
            print("✗ credentials.json no encontrado")
            return False
        
        scopes = ['https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_file(
            str(creds_file),
            scopes=scopes
        )
        
        print("✓ Autenticación exitosa")
        print(f"✓ Cuenta: {credentials.service_account_email}")
        print()
        return True
    except Exception as e:
        print(f"✗ Error de autenticación: {str(e)}")
        print()
        return False


def show_next_steps():
    """Muestra los próximos pasos"""
    print("=" * 60)
    print("PRÓXIMOS PASOS")
    print("=" * 60)
    print("""
1. CONFIGURAR CREDENCIALES (si no lo has hecho):
   - Ve a https://console.cloud.google.com/
   - Crea un proyecto llamado "Project Scheduler"
   - Habilita Google Drive API y Google Sheets API
   - Crea una cuenta de servicio y descarga la clave JSON
   - Guarda el JSON como 'credentials.json'

2. EJECUTAR LA APLICACIÓN:
   python main.py
   
   Esto creará:
   - Carpetas en Google Drive (Ingeniería, Obras, Mantenimiento)
   - Cronogramas para cada departamento
   - Cronograma maestro consolidado

3. ACTUALIZAR .env:
   - Copia los IDs mostrados por la aplicación
   - Pega los valores en el archivo .env

4. EJECUTAR EJEMPLOS:
   python examples/example_1_setup.py      # Agregar proyectos
   python examples/example_2_reports.py    # Generar reportes
   python examples/example_3_notifications.py  # Alertas
   python examples/example_4_export.py     # Exportar datos

5. DOCUMENTACIÓN:
   - Lee README.md para descripción completa
   - Lee SETUP.md para configuración detallada

¿PROBLEMAS?
   - Revisa logs/project_scheduler.log
   - Verifica que credentials.json está en la carpeta raíz
   - Asegúrate de que las APIs están habilitadas en Google Cloud
""")


def main():
    """Ejecuta todas las verificaciones"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " PROJECT SCHEDULER - VERIFICACIÓN DE CONFIGURACIÓN ".center(58) + "║")
    print("╚" + "=" * 58 + "╝\n")
    
    checks = {
        'Archivos del proyecto': check_files,
        'Dependencias Python': check_dependencies,
        'Credenciales de Google': check_credentials,
        'Configuración (.env)': check_env,
        'Módulos Python': test_import,
        'Autenticación con Google': test_google_auth
    }
    
    results = {}
    for check_name, check_func in checks.items():
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"✗ Error durante {check_name}: {str(e)}\n")
            results[check_name] = False
    
    # Resumen
    print("=" * 60)
    print("RESUMEN")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check_name, result in results.items():
        status = "✓ OK" if result else "✗ FALLO"
        print(f"{check_name}: {status}")
    
    print(f"\nPruebas pasadas: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 ¡TODA LA CONFIGURACIÓN ES CORRECTA! ¡Puedes empezar!\n")
        show_next_steps()
        return 0
    else:
        print("\n⚠️  Hay algunos problemas que necesitan ser resueltos.\n")
        if not results['Credenciales de Google']:
            print("ACCIÓN REQUERIDA: Debes configurar las credenciales de Google Cloud")
        if not results['Dependencias Python']:
            print("ACCIÓN REQUERIDA: Instala las dependencias con: pip install -r requirements.txt")
        return 1


if __name__ == '__main__':
    sys.exit(main())
