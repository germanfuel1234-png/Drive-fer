#!/usr/bin/env python3
"""
Script para crear carpetas en Google Drive
Usa la autenticación OAuth ya configurada
"""

import logging
import sys
from menu import select_gmail_account
from modules.auth import GoogleAuth
from modules.drive_manager import DriveManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def create_folder_structure():
    """Crear estructura de carpetas en Drive"""
    
    print("\n" + "="*60)
    print("📁 CREADOR DE CARPETAS EN GOOGLE DRIVE")
    print("="*60 + "\n")
    
    # Seleccionar cuenta
    account = select_gmail_account()
    token_path = account.get('token_path')
    
    print(f"\n📧 Usando cuenta: {account['email']} ({account['name']})")
    print("🔐 Autenticando...\n")
    
    # Autenticar
    auth = GoogleAuth(token_path=token_path)
    drive_mgr = DriveManager(auth)
    
    print("✅ Autenticado correctamente\n")
    
    # Crear carpeta raíz
    print("📦 Creando estructura de carpetas...\n")
    
    root_folder_name = "Proyectos_Empresa"
    root_folder_id = drive_mgr.get_or_create_folder(root_folder_name)
    print(f"✅ Carpeta raíz: {root_folder_name}")
    print(f"   ID: {root_folder_id}\n")
    
    # Departamentos
    departments = [
        "Ingeniería",
        "Obras",
        "Mantenimiento"
    ]
    
    folder_structure = {}
    
    for dept in departments:
        print(f"📂 Creando carpeta: {dept}")
        
        # Carpeta del departamento
        dept_folder_id = drive_mgr.get_or_create_folder(dept, root_folder_id)
        print(f"   ✅ {dept} (ID: {dept_folder_id})")
        
        # Subcarpeta Clientes
        clients_folder_id = drive_mgr.get_or_create_folder("Clientes", dept_folder_id)
        print(f"   ✅ Clientes (ID: {clients_folder_id})\n")
        
        folder_structure[dept] = {
            "folder_id": dept_folder_id,
            "clients_folder_id": clients_folder_id
        }
    
    # Resumen
    print("="*60)
    print("✅ ESTRUCTURA CREADA EXITOSAMENTE")
    print("="*60 + "\n")
    
    print("📋 RESUMEN DE CARPETAS:\n")
    print(f"📦 Raíz: {root_folder_name}")
    print(f"   Link: https://drive.google.com/drive/folders/{root_folder_id}\n")
    
    for dept, folders in folder_structure.items():
        print(f"📂 {dept}")
        print(f"   Folder ID: {folders['folder_id']}")
        print(f"   Link: https://drive.google.com/drive/folders/{folders['folder_id']}")
        print(f"   ├─ Clientes")
        print(f"      Folder ID: {folders['clients_folder_id']}")
        print(f"      Link: https://drive.google.com/drive/folders/{folders['clients_folder_id']}\n")
    
    print("✨ Puedes abrir los links en tu navegador para ver las carpetas\n")
    
    return folder_structure


def show_menu():
    """Mostrar menú de opciones"""
    while True:
        print("\n" + "="*60)
        print("🗂️ GESTOR DE CARPETAS EN DRIVE")
        print("="*60 + "\n")
        
        print("1. ➕ Crear estructura de carpetas")
        print("2. 📊 Ver información de la estructura")
        print("3. ❌ Salir\n")
        
        choice = input("🔹 Selecciona opción: ").strip()
        
        if choice == "1":
            create_folder_structure()
            input("\n🔹 Presiona Enter para continuar...")
        elif choice == "2":
            print_info()
            input("\n🔹 Presiona Enter para continuar...")
        elif choice == "3":
            print("\n❌ Saliendo...\n")
            sys.exit(0)
        else:
            print("\n❌ Opción no válida. Intenta de nuevo.")


def print_info():
    """Mostrar información de la estructura"""
    print("\n" + "="*60)
    print("📋 INFORMACIÓN DE ESTRUCTURA")
    print("="*60 + "\n")
    
    print("Estructura que se crea:")
    print("""
Proyectos_Empresa/
├── Ingeniería/
│   └── Clientes/
├── Obras/
│   └── Clientes/
└── Mantenimiento/
    └── Clientes/
    """)
    
    print("\n✨ Beneficios:")
    print("  • Organización clara por departamento")
    print("  • Carpeta Clientes separada por departamento")
    print("  • Fácil acceso desde Google Sheets")
    print("  • Estructura escalable para más departamentos\n")


if __name__ == "__main__":
    try:
        show_menu()
    except KeyboardInterrupt:
        print("\n\n❌ Operación cancelada por el usuario\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
