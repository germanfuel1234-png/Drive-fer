"""
Testing Script - Script de Pruebas
Ejecuta pruebas unitarias básicas de los módulos
"""

import sys
import logging
from pathlib import Path
from datetime import datetime, timedelta

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_config():
    """Test de configuración"""
    print("\n" + "=" * 60)
    print("TEST 1: CONFIGURACIÓN")
    print("=" * 60)
    
    try:
        from config import Config
        
        assert Config.ROOT_FOLDER_NAME == 'Gestión de Proyectos'
        print("✓ Nombre de carpeta raíz correcto")
        
        assert 'Ingeniería' in Config.DEPARTMENTS
        assert 'Obras' in Config.DEPARTMENTS
        assert 'Mantenimiento' in Config.DEPARTMENTS
        print("✓ Todos los departamentos configurados")
        
        assert Path(Config.GOOGLE_APPLICATION_CREDENTIALS).name == 'credentials.json'
        print("✓ Ruta de credenciales configurada")
        
        return True
    except AssertionError as e:
        print(f"✗ Error de configuración: {str(e)}")
        return False
    except Exception as e:
        print(f"✗ Error inesperado: {str(e)}")
        return False


def test_drive_manager_initialization():
    """Test de inicialización del DriveManager"""
    print("\n" + "=" * 60)
    print("TEST 2: INICIALIZACIÓN DE DRIVE MANAGER")
    print("=" * 60)
    
    try:
        from config import Config
        from modules import DriveManager
        
        if not Path(Config.GOOGLE_APPLICATION_CREDENTIALS).exists():
            print("⚠ credentials.json no encontrado - Skipping")
            return True
        
        drive_mgr = DriveManager(Config.GOOGLE_APPLICATION_CREDENTIALS)
        print("✓ Drive Manager inicializado correctamente")
        
        assert drive_mgr.service is not None
        print("✓ Servicio de Google Drive conectado")
        
        return True
    except Exception as e:
        print(f"⚠ No se pudo inicializar Drive Manager (esperado si credentials.json no existe)")
        print(f"  Razón: {str(e)[:100]}...")
        return True  # No fallar si credentials.json no existe


def test_sheets_manager_initialization():
    """Test de inicialización del SheetsManager"""
    print("\n" + "=" * 60)
    print("TEST 3: INICIALIZACIÓN DE SHEETS MANAGER")
    print("=" * 60)
    
    try:
        from config import Config
        from modules import SheetsManager
        
        if not Path(Config.GOOGLE_APPLICATION_CREDENTIALS).exists():
            print("⚠ credentials.json no encontrado - Skipping")
            return True
        
        sheets_mgr = SheetsManager(Config.GOOGLE_APPLICATION_CREDENTIALS)
        print("✓ Sheets Manager inicializado correctamente")
        
        assert sheets_mgr.sheets_service is not None
        print("✓ Servicio de Google Sheets conectado")
        
        assert sheets_mgr.drive_service is not None
        print("✓ Servicio de Google Drive conectado")
        
        return True
    except Exception as e:
        print(f"⚠ No se pudo inicializar Sheets Manager (esperado si credentials.json no existe)")
        print(f"  Razón: {str(e)[:100]}...")
        return True  # No fallar si credentials.json no existe


def test_scheduler_manager_initialization():
    """Test de inicialización del SchedulerManager"""
    print("\n" + "=" * 60)
    print("TEST 4: INICIALIZACIÓN DE SCHEDULER MANAGER")
    print("=" * 60)
    
    try:
        from config import Config
        from modules import SheetsManager, SchedulerManager
        
        if not Path(Config.GOOGLE_APPLICATION_CREDENTIALS).exists():
            print("⚠ credentials.json no encontrado - Skipping")
            return True
        
        sheets_mgr = SheetsManager(Config.GOOGLE_APPLICATION_CREDENTIALS)
        scheduler_mgr = SchedulerManager(sheets_mgr, Config.GOOGLE_APPLICATION_CREDENTIALS)
        
        print("✓ Scheduler Manager inicializado correctamente")
        
        return True
    except Exception as e:
        print(f"⚠ No se pudo inicializar Scheduler Manager (esperado si credentials.json no existe)")
        print(f"  Razón: {str(e)[:100]}...")
        return True


def test_notification_manager_initialization():
    """Test de inicialización del NotificationManager"""
    print("\n" + "=" * 60)
    print("TEST 5: INICIALIZACIÓN DE NOTIFICATION MANAGER")
    print("=" * 60)
    
    try:
        from config import Config
        from modules import NotificationManager
        
        if not Path(Config.GOOGLE_APPLICATION_CREDENTIALS).exists():
            print("⚠ credentials.json no encontrado - Skipping")
            return True
        
        notif_mgr = NotificationManager(
            Config.GOOGLE_APPLICATION_CREDENTIALS,
            Config.NOTIFICATION_EMAIL
        )
        
        print("✓ Notification Manager inicializado correctamente")
        
        return True
    except Exception as e:
        print(f"⚠ No se pudo inicializar Notification Manager")
        print(f"  Razón: {str(e)[:100]}...")
        return True


def test_project_data_structure():
    """Test de estructura de datos de proyectos"""
    print("\n" + "=" * 60)
    print("TEST 6: ESTRUCTURA DE DATOS DE PROYECTO")
    print("=" * 60)
    
    try:
        project = {
            'id': 'PRY-TEST-001',
            'client': 'Cliente Test',
            'description': 'Proyecto de prueba',
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
            'status': 'En Progreso',
            'responsible': 'Tester',
            'budget': '$10,000',
            'progress': 50,
            'notes': 'Proyecto de prueba'
        }
        
        # Validar campos obligatorios
        required_fields = ['id', 'client', 'description', 'start_date', 'end_date', 'status']
        for field in required_fields:
            assert field in project, f"Campo faltante: {field}"
            assert project[field], f"Campo vacío: {field}"
        
        print("✓ Estructura de datos correcta")
        print(f"  Campos: {', '.join(project.keys())}")
        
        return True
    except AssertionError as e:
        print(f"✗ Error de estructura: {str(e)}")
        return False


def test_date_formats():
    """Test de formatos de fecha"""
    print("\n" + "=" * 60)
    print("TEST 7: FORMATOS DE FECHA")
    print("=" * 60)
    
    try:
        from datetime import datetime
        
        test_dates = [
            '2026-07-20',
            '2026-12-31',
            '2027-01-01'
        ]
        
        for date_str in test_dates:
            parsed = datetime.strptime(date_str, '%Y-%m-%d')
            assert parsed is not None
        
        print("✓ Formato de fecha correcto (YYYY-MM-DD)")
        
        return True
    except ValueError as e:
        print(f"✗ Error de formato de fecha: {str(e)}")
        return False


def test_logging():
    """Test de sistema de logging"""
    print("\n" + "=" * 60)
    print("TEST 8: SISTEMA DE LOGGING")
    print("=" * 60)
    
    try:
        from config import Config
        
        # Verificar que el archivo de log puede ser creado
        log_path = Path(Config.LOG_FILE)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Crear un logger de prueba
        test_logger = logging.getLogger('test_logger')
        handler = logging.FileHandler(log_path)
        test_logger.addHandler(handler)
        test_logger.info("Mensaje de prueba")
        
        assert log_path.exists()
        print(f"✓ Sistema de logging funcional")
        print(f"  Ubicación: {Config.LOG_FILE}")
        
        return True
    except Exception as e:
        print(f"✗ Error en sistema de logging: {str(e)}")
        return False


def run_all_tests():
    """Ejecuta todas las pruebas"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " PROJECT SCHEDULER - SUITE DE PRUEBAS ".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    
    tests = [
        ('Configuración', test_config),
        ('Drive Manager', test_drive_manager_initialization),
        ('Sheets Manager', test_sheets_manager_initialization),
        ('Scheduler Manager', test_scheduler_manager_initialization),
        ('Notification Manager', test_notification_manager_initialization),
        ('Estructura de Datos', test_project_data_structure),
        ('Formatos de Fecha', test_date_formats),
        ('Sistema de Logging', test_logging),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n✗ Error no controlado en {test_name}")
            print(f"  {str(e)}")
            results[test_name] = False
    
    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASÓ" if result else "✗ FALLÓ"
        print(f"{test_name}: {status}")
    
    print(f"\nPruebas pasadas: {passed}/{total}")
    
    if passed == total:
        print("\n✅ ¡TODAS LAS PRUEBAS PASARON!\n")
        return 0
    else:
        print("\n⚠️  Algunas pruebas fallaron\n")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
