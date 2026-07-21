"""
Example 3: Notifications and Alerts
Demonstrates how to handle notifications and service requests
"""

from main import ProjectScheduler
from datetime import datetime

def example_check_service_requests():
    """Example: Check for incoming service requests"""
    
    scheduler = ProjectScheduler()
    
    print("=== VERIFICANDO SOLICITUDES DE SERVICIO ===\n")
    
    # Check inbox for service requests
    requests = scheduler.check_service_requests()
    
    if requests:
        print(f"Se encontraron {len(requests)} solicitudes de servicio:\n")
        for req in requests:
            print(f"De: {req['from']}")
            print(f"Asunto: {req['subject']}")
            print(f"Fecha: {req['date']}")
            print(f"Mensaje: {req['body'][:100]}...")
            print("-" * 50)
            print()
    else:
        print("No hay nuevas solicitudes de servicio")


def example_log_notifications():
    """Example: Log notifications for various events"""
    
    scheduler = ProjectScheduler()
    
    print("\n=== REGISTRANDO NOTIFICACIONES ===\n")
    
    # Log a service request received
    if scheduler.log_notification(
        notification_type='alert',
        department='Ingeniería',
        client='Cliente A',
        message='Se recibió solicitud de servicio para reparación de equipo',
        project_id='PRY-ENG-001'
    ):
        print("✓ Notificación de alerta registrada")
    
    # Log a deadline approaching
    if scheduler.log_notification(
        notification_type='warning',
        department='Obras',
        client='Cliente B',
        message='Plazo de entrega se aproxima (5 días)',
        project_id='PRY-OBR-001'
    ):
        print("✓ Notificación de advertencia registrada")
    
    # Log a project completion
    if scheduler.log_notification(
        notification_type='info',
        department='Mantenimiento',
        client='Cliente C',
        message='Mantenimiento preventivo completado satisfactoriamente',
        project_id='PRY-MTN-001'
    ):
        print("✓ Notificación de información registrada")
    
    print("\n✓ Todas las notificaciones han sido registradas en el log")


def example_generate_daily_summary():
    """Example: Generate a daily summary of all schedules"""
    
    scheduler = ProjectScheduler()
    
    print("\n=== RESUMEN DIARIO ===\n")
    
    # This is a placeholder - in production, fetch actual schedule data
    schedules = {
        'Ingeniería': [
            {'status': 'En Progreso', 'id': 'PRY-ENG-001'},
            {'status': 'Completado', 'id': 'PRY-ENG-002'},
        ],
        'Obras': [
            {'status': 'En Progreso', 'id': 'PRY-OBR-001'},
            {'status': 'En Pausa', 'id': 'PRY-OBR-002'},
        ],
        'Mantenimiento': [
            {'status': 'En Progreso', 'id': 'PRY-MTN-001'},
        ]
    }
    
    summary = scheduler.notification_manager.generate_daily_summary(schedules)
    print(summary)
    
    # Save summary to file
    with open('./examples/daily_summary.txt', 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print("✓ Resumen guardado en ./examples/daily_summary.txt")


if __name__ == '__main__':
    print("=== Ejemplo 3: Notificaciones y Alertas ===\n")
    example_check_service_requests()
    example_log_notifications()
    example_generate_daily_summary()
