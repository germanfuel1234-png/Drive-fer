"""
Example 4: Data Export and Integration
Demonstrates exporting data to CSV and external integrations
"""

from main import ProjectScheduler
import os

def example_export_schedules():
    """Example: Export department schedules to CSV"""
    
    scheduler = ProjectScheduler()
    
    print("=== EXPORTANDO CRONOGRAMAS A CSV ===\n")
    
    # Create exports directory
    os.makedirs('./examples/exports', exist_ok=True)
    
    for dept_name, dept_config in scheduler.config.DEPARTMENTS.items():
        if dept_config['sheet_id']:
            output_file = f'./examples/exports/cronograma_{dept_name.lower()}.csv'
            
            if scheduler.scheduler_manager.export_to_csv(
                dept_config['sheet_id'],
                dept_name,
                output_file
            ):
                print(f"✓ {dept_name} exportado a: {output_file}")
            else:
                print(f"✗ Error al exportar {dept_name}")
    
    print("\n✓ Todos los cronogramas han sido exportados")


def example_bulk_project_add():
    """Example: Add multiple projects at once"""
    
    scheduler = ProjectScheduler()
    
    print("\n=== AGREGANDO MÚLTIPLES PROYECTOS ===\n")
    
    # Sample projects for each department
    projects_to_add = {
        'Ingeniería': [
            {
                'id': 'PRY-ENG-002',
                'client': 'Cliente D',
                'description': 'Actualización de software industrial',
                'start_date': '2026-07-20',
                'end_date': '2026-08-15',
                'status': 'Planificación',
                'responsible': 'Pedro Sánchez',
                'budget': '$30,000',
                'progress': 10,
                'notes': 'Pendiente aprobación del cliente'
            }
        ],
        'Obras': [
            {
                'id': 'PRY-OBR-002',
                'client': 'Cliente E',
                'description': 'Renovación de oficinas',
                'start_date': '2026-08-01',
                'end_date': '2026-09-30',
                'status': 'Planificación',
                'responsible': 'Laura Martínez',
                'budget': '$75,000',
                'progress': 0,
                'notes': 'Presupuesto aprobado'
            }
        ],
        'Mantenimiento': [
            {
                'id': 'PRY-MTN-002',
                'client': 'Cliente F',
                'description': 'Inspección de sistemas HVAC',
                'start_date': '2026-07-25',
                'end_date': '2026-07-28',
                'status': 'Planificación',
                'responsible': 'Alfonso Ruiz',
                'budget': '$8,000',
                'progress': 0,
                'notes': 'Servicio trimestral'
            }
        ]
    }
    
    added_count = 0
    for dept_name, projects in projects_to_add.items():
        for project in projects:
            if scheduler.add_project_to_department(dept_name, project):
                print(f"✓ {project['id']} agregado a {dept_name}")
                added_count += 1
            else:
                print(f"✗ Error al agregar {project['id']} a {dept_name}")
    
    # Consolidate after bulk add
    if scheduler.consolidate_master_schedule():
        print(f"\n✓ {added_count} proyectos agregados y cronograma maestro consolidado")
    else:
        print(f"\n✗ Error al consolidar cronograma maestro")


if __name__ == '__main__':
    print("=== Ejemplo 4: Exportar Datos e Integración ===\n")
    example_export_schedules()
    example_bulk_project_add()
