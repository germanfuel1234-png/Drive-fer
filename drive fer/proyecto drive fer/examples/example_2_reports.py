"""
Example 2: Generate Reports and Monitor Schedules
Demonstrates reporting and monitoring functionality
"""

from main import ProjectScheduler
import json

def example_generate_reports():
    """Example: Generate schedule reports"""
    
    scheduler = ProjectScheduler()
    
    # Generate schedules report
    print("Generando reportes de cronogramas...\n")
    report = scheduler.generate_schedules_report()
    
    print("=== REPORTE DE CRONOGRAMAS ===\n")
    print(f"Generado en: {report['generated_at']}\n")
    
    total_projects = 0
    total_in_progress = 0
    total_completed = 0
    
    for dept_name, summary in report['departments'].items():
        print(f"{dept_name}:")
        print(f"  - Total de proyectos: {summary.get('total_projects', 0)}")
        print(f"  - En progreso: {summary.get('in_progress', 0)}")
        print(f"  - Completados: {summary.get('completed', 0)}")
        print(f"  - En pausa: {summary.get('on_hold', 0)}")
        print()
        
        total_projects += summary.get('total_projects', 0)
        total_in_progress += summary.get('in_progress', 0)
        total_completed += summary.get('completed', 0)
    
    print("=== RESUMEN TOTAL ===")
    print(f"Total de proyectos: {total_projects}")
    print(f"En progreso: {total_in_progress}")
    print(f"Completados: {total_completed}")
    
    # Save report to file
    with open('./examples/schedule_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print("\n✓ Reporte guardado en ./examples/schedule_report.json")


def example_check_deadlines():
    """Example: Check for approaching deadlines"""
    
    scheduler = ProjectScheduler()
    
    print("\n=== VERIFICANDO PLAZOS PRÓXIMOS ===\n")
    
    # Check for deadlines in the next 7 days
    alerts = scheduler.check_approaching_deadlines(days_threshold=7)
    
    if alerts:
        print(f"Se encontraron {len(alerts)} proyectos con plazos próximos:\n")
        for alert in alerts:
            print(f"  Departamento: {alert['department']}")
            print(f"  Proyecto: {alert['project_id']}")
            print(f"  Cliente: {alert['client']}")
            print(f"  Plazo: {alert['end_date']}")
            print(f"  Días restantes: {alert['days_remaining']}")
            print()
    else:
        print("No hay proyectos con plazos próximos en los próximos 7 días")


if __name__ == '__main__':
    print("=== Ejemplo 2: Generar Reportes y Monitorear Cronogramas ===\n")
    example_generate_reports()
    example_check_deadlines()
