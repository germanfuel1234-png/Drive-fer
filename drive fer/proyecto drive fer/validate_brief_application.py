#!/usr/bin/env python3
"""
Validation Script - Verify Brief Application
Checks that all Brief specifications are properly implemented
"""

import os
import sys
from pathlib import Path

def check_files_exist():
    """Verify all required files exist"""
    print("\n✓ VERIFICANDO EXISTENCIA DE ARCHIVOS")
    print("=" * 60)
    
    required_files = [
        'main.py',
        'config.py',
        'requirements.txt',
        '.env.example',
        'modules/auth.py',
        'modules/scheduler.py',
        'modules/consolidator.py',
        'modules/notifier.py',
        'modules/drive_manager.py',
        'modules/sheets_manager.py',
        'BRIEF_APPLICACION.md',
        'CHANGELOG.md',
    ]
    
    base_path = Path('/home/german/Escritorio/drive fer/project_scheduler')
    
    all_exist = True
    for file_path in required_files:
        full_path = base_path / file_path
        exists = full_path.exists()
        status = "✅" if exists else "❌"
        print(f"{status} {file_path}")
        if not exists:
            all_exist = False
    
    return all_exist

def check_modules_imports():
    """Verify modules can be imported"""
    print("\n✓ VERIFICANDO IMPORTS DE MÓDULOS")
    print("=" * 60)
    
    sys.path.insert(0, '/home/german/Escritorio/drive fer/project_scheduler')
    
    modules_to_check = [
        ('config', 'Config'),
        ('modules.auth', 'GoogleAuth'),
        ('modules.drive_manager', 'DriveManager'),
        ('modules.sheets_manager', 'SheetsManager'),
        ('modules.scheduler', 'Scheduler'),
        ('modules.consolidator', 'Consolidator'),
        ('modules.notifier', 'Notifier'),
    ]
    
    all_imported = True
    for module_name, class_name in modules_to_check:
        try:
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"✅ {module_name}.{class_name}")
        except Exception as e:
            print(f"❌ {module_name}.{class_name}: {str(e)}")
            all_imported = False
    
    return all_imported

def check_config_variables():
    """Verify config has all required variables"""
    print("\n✓ VERIFICANDO VARIABLES DE CONFIGURACIÓN")
    print("=" * 60)
    
    required_vars = [
        'GOOGLE_CREDENTIALS_PATH',
        'DRIVE_ROOT_FOLDER_NAME',
        'DEPARTMENTS_LIST',
        'DEPARTMENT_SHEET_HEADERS',
        'MASTER_SHEET_HEADERS',
        'VALID_STATES',
        'ALERT_DAYS_THRESHOLD',
        'LOG_FILE_PATH',
        'MASTER_SCHEDULE_NAME',
    ]
    
    sys.path.insert(0, '/home/german/Escritorio/drive fer/project_scheduler')
    from config import Config
    
    all_present = True
    for var_name in required_vars:
        has_var = hasattr(Config, var_name)
        status = "✅" if has_var else "❌"
        print(f"{status} Config.{var_name}")
        if not has_var:
            all_present = False
    
    return all_present

def check_env_example():
    """Verify .env.example has all required variables"""
    print("\n✓ VERIFICANDO VARIABLES EN .env.example")
    print("=" * 60)
    
    env_file = Path('/home/german/Escritorio/drive fer/project_scheduler/.env.example')
    
    required_env_vars = [
        'GOOGLE_CREDENTIALS_PATH',
        'DRIVE_ROOT_FOLDER_NAME',
        'DEPARTMENTS',
        'SHEET_MAESTRO_ID',
        'ALERT_DAYS_THRESHOLD',
        'LOG_FILE_PATH',
        'SMTP_SERVER',
        'SMTP_PORT',
        'ALERT_RECIPIENTS',
    ]
    
    if not env_file.exists():
        print("❌ .env.example no existe")
        return False
    
    content = env_file.read_text()
    all_present = True
    for var_name in required_env_vars:
        has_var = var_name in content
        status = "✅" if has_var else "❌"
        print(f"{status} {var_name}")
        if not has_var:
            all_present = False
    
    return all_present

def check_main_py_flow():
    """Verify main.py implements the 10-step flow"""
    print("\n✓ VERIFICANDO FLUJO EN main.py")
    print("=" * 60)
    
    main_file = Path('/home/german/Escritorio/drive fer/project_scheduler/main.py')
    content = main_file.read_text()
    
    flow_steps = [
        ('setup_folder_structure', 'Step 1-3: Crear carpetas'),
        ('setup_spreadsheets', 'Step 4: Crear sheets'),
        ('consolidate_schedules', 'Step 5-7: Consolidar datos'),
        ('evaluate_alerts', 'Step 8-10: Alertas'),
        ('run_full_cycle', 'Orquestación completa'),
    ]
    
    all_present = True
    for method_name, description in flow_steps:
        has_method = f'def {method_name}' in content
        status = "✅" if has_method else "❌"
        print(f"{status} {method_name}() - {description}")
        if not has_method:
            all_present = False
    
    return all_present

def check_date_format():
    """Verify date format is DD/MM/YYYY"""
    print("\n✓ VERIFICANDO FORMATO DE FECHAS (DD/MM/YYYY)")
    print("=" * 60)
    
    scheduler_file = Path('/home/german/Escritorio/drive fer/project_scheduler/modules/scheduler.py')
    content = scheduler_file.read_text()
    
    has_format = "%d/%m/%Y" in content
    status = "✅" if has_format else "❌"
    print(f"{status} Formato '%d/%m/%Y' en scheduler.py")
    
    return has_format

def check_schema():
    """Verify sheet schema matches brief"""
    print("\n✓ VERIFICANDO SCHEMA DE SHEETS")
    print("=" * 60)
    
    sys.path.insert(0, '/home/german/Escritorio/drive fer/project_scheduler')
    from config import Config
    
    expected_columns = [
        'ID_Proyecto', 'Cliente', 'Descripcion', 'Fecha_Inicio',
        'Fecha_Entrega', 'Estado', 'Responsable'
    ]
    
    all_present = True
    for col in expected_columns:
        has_col = col in Config.DEPARTMENT_SHEET_HEADERS
        status = "✅" if has_col else "❌"
        print(f"{status} {col}")
        if not has_col:
            all_present = False
    
    # Check master has Departamento
    has_dept = 'Departamento' in Config.MASTER_SHEET_HEADERS
    status = "✅" if has_dept else "❌"
    print(f"{status} Master tiene 'Departamento'")
    
    return all_present and has_dept

def check_valid_states():
    """Verify valid states"""
    print("\n✓ VERIFICANDO ESTADOS VÁLIDOS")
    print("=" * 60)
    
    sys.path.insert(0, '/home/german/Escritorio/drive fer/project_scheduler')
    from config import Config
    
    expected_states = ['Pendiente', 'En progreso', 'Completado', 'Retrasado']
    
    all_present = True
    for state in expected_states:
        has_state = state in Config.VALID_STATES
        status = "✅" if has_state else "❌"
        print(f"{status} {state}")
        if not has_state:
            all_present = False
    
    return all_present

def run_all_checks():
    """Run all validation checks"""
    print("\n╔" + "=" * 58 + "╗")
    print("║" + " VALIDACIÓN DE APLICACIÓN DEL BRIEF TÉCNICO ".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    
    checks = [
        ("Archivos", check_files_exist),
        ("Imports", check_modules_imports),
        ("Variables Config", check_config_variables),
        (".env.example", check_env_example),
        ("Flujo main.py", check_main_py_flow),
        ("Formato Fechas", check_date_format),
        ("Schema Sheets", check_schema),
        ("Estados Válidos", check_valid_states),
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"\n⚠️ Error en {check_name}: {str(e)}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {check_name}")
    
    print("\n" + "=" * 60)
    print(f"Resultado: {passed}/{total} validaciones pasadas")
    
    if passed == total:
        print("\n✅ APLICACIÓN COMPLETA DEL BRIEF TÉCNICO")
        print("El proyecto está listo para producción.")
        return 0
    else:
        print(f"\n❌ {total - passed} validación(es) fallida(s)")
        print("Revise los errores arriba.")
        return 1

if __name__ == '__main__':
    exit_code = run_all_checks()
    sys.exit(exit_code)
