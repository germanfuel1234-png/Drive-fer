"""
Example 1: Basic Setup and Project Addition
Demonstrates how to initialize the system and add projects
"""

from main import ProjectScheduler
from datetime import datetime, timedelta

def example_setup_and_add_projects():
    """Example: Initialize scheduler and add sample projects"""
    
    # Initialize the scheduler
    scheduler = ProjectScheduler()
    
    # Example: Add a project to Ingeniería department
    engineering_project = {
        'id': 'PRY-ENG-001',
        'client': 'Cliente A',
        'description': 'Desarrollo de sistema de control automático',
        'start_date': datetime.now().strftime('%Y-%m-%d'),
        'end_date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
        'status': 'En Progreso',
        'responsible': 'Juan García',
        'budget': '$50,000',
        'progress': 45,
        'notes': 'En fase de desarrollo de firmware'
    }
    
    if scheduler.add_project_to_department('Ingeniería', engineering_project):
        print("✓ Proyecto agregado a Ingeniería")
    else:
        print("✗ Error al agregar proyecto a Ingeniería")
    
    # Example: Add a project to Obras department
    obras_project = {
        'id': 'PRY-OBR-001',
        'client': 'Cliente B',
        'description': 'Construcción de edificio comercial',
        'start_date': datetime.now().strftime('%Y-%m-%d'),
        'end_date': (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d'),
        'status': 'En Progreso',
        'responsible': 'María López',
        'budget': '$200,000',
        'progress': 30,
        'notes': 'Cimientos terminados, iniciando estructura'
    }
    
    if scheduler.add_project_to_department('Obras', obras_project):
        print("✓ Proyecto agregado a Obras")
    else:
        print("✗ Error al agregar proyecto a Obras")
    
    # Example: Add a project to Mantenimiento department
    maintenance_project = {
        'id': 'PRY-MTN-001',
        'client': 'Cliente C',
        'description': 'Mantenimiento preventivo de maquinaria',
        'start_date': datetime.now().strftime('%Y-%m-%d'),
        'end_date': (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d'),
        'status': 'En Progreso',
        'responsible': 'Carlos Rodríguez',
        'budget': '$15,000',
        'progress': 60,
        'notes': 'Reparación de bomba completada'
    }
    
    if scheduler.add_project_to_department('Mantenimiento', maintenance_project):
        print("✓ Proyecto agregado a Mantenimiento")
    else:
        print("✗ Error al agregar proyecto a Mantenimiento")
    
    # Consolidate master schedule
    if scheduler.consolidate_master_schedule():
        print("✓ Cronograma maestro consolidado")
    else:
        print("✗ Error al consolidar cronograma maestro")


if __name__ == '__main__':
    print("=== Ejemplo 1: Configuración Inicial y Agregar Proyectos ===\n")
    example_setup_and_add_projects()
