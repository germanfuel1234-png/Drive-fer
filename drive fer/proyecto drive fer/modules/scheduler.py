"""
Scheduler Module
Handles date logic, deadline calculation, and alert generation
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

logger = logging.getLogger(__name__)


class Scheduler:
    """Manages project scheduling and deadline monitoring"""
    
    DATE_FORMAT = '%d/%m/%Y'  # DD/MM/YYYY format as per spec
    
    def __init__(self, alert_days_threshold: int = 3):
        """
        Initialize Scheduler
        
        Args:
            alert_days_threshold: Number of days before deadline to trigger alert
        """
        self.alert_days_threshold = alert_days_threshold
        logger.info(f"Scheduler initialized with {alert_days_threshold} days threshold")
    
    def parse_date(self, date_string: str) -> datetime:
        """
        Parse a date string in multiple formats
        Supports: DD/MM/YYYY, d/m/YYYY, YYYY-MM-DD, YYYY-MM-DD HH:MM:SS, and ISO format
        
        Args:
            date_string: Date string in various formats
        
        Returns:
            datetime object
        """
        import re
        
        if not date_string or not isinstance(date_string, str):
            raise ValueError(f"Invalid date: {date_string}")
        
        date_string = date_string.strip()
        
        # Normalize dates with single-digit day/month (e.g., "2/7/2026" → "02/07/2026")
        # Pattern: d/m/Y or d/m/Y H:M:S
        if re.match(r'^\d{1,2}/\d{1,2}/\d{4}', date_string):
            parts = date_string.split(' ', 1)
            date_part = parts[0]
            date_components = date_part.split('/')
            # Pad day and month with leading zero if needed
            date_components[0] = date_components[0].zfill(2)
            date_components[1] = date_components[1].zfill(2)
            normalized = '/'.join(date_components)
            if len(parts) > 1:
                date_string = normalized + ' ' + parts[1]
            else:
                date_string = normalized
        
        # Try multiple date formats
        formats_to_try = [
            '%d/%m/%Y',              # DD/MM/YYYY (now normalized)
            '%Y-%m-%d',              # YYYY-MM-DD
            '%Y-%m-%d %H:%M:%S',     # YYYY-MM-DD HH:MM:SS
            '%Y-%m-%dT%H:%M:%S',     # ISO format
            '%d-%m-%Y',              # DD-MM-YYYY
            '%m/%d/%Y',              # MM/DD/YYYY (US format)
            '%d/%m/%Y %H:%M:%S',     # DD/MM/YYYY HH:MM:SS (now normalized)
        ]
        
        for fmt in formats_to_try:
            try:
                return datetime.strptime(date_string, fmt)
            except ValueError:
                continue
        
        # If none of the formats worked, raise an error
        logger.error(f"Invalid date format: {date_string}. Tried formats: {formats_to_try}")
        raise ValueError(f"Invalid date format: {date_string}. Expected one of: DD/MM/YYYY, YYYY-MM-DD, or YYYY-MM-DD HH:MM:SS")
    
    def format_date(self, dt: datetime) -> str:
        """
        Format a datetime object to DD/MM/YYYY string
        
        Args:
            dt: datetime object
        
        Returns:
            Formatted date string
        """
        return dt.strftime(self.DATE_FORMAT)
    
    def calculate_days_remaining(self, deadline_str: str) -> int:
        """
        Calculate days remaining until deadline
        
        Args:
            deadline_str: Deadline date in DD/MM/YYYY format
        
        Returns:
            Number of days remaining (negative if overdue)
        """
        try:
            deadline = self.parse_date(deadline_str)
            today = datetime.now()
            days_remaining = (deadline - today).days
            return days_remaining
        except Exception as e:
            logger.error(f"Error calculating days remaining: {str(e)}")
            return None
    
    def detect_overdue_projects(self, projects: List[Dict]) -> List[Dict]:
        """
        Identify projects that are overdue
        
        Args:
            projects: List of project dictionaries from sheet
        
        Returns:
            List of overdue projects with alert details
        """
        overdue_projects = []
        
        for project in projects:
            try:
                # Skip if already completed
                if project.get('Estado') == 'Completado':
                    continue
                
                # Calculate days remaining
                deadline_str = project.get('Fecha_Entrega', '')
                if not deadline_str:
                    continue
                
                days_remaining = self.calculate_days_remaining(deadline_str)
                
                # If negative, it's overdue
                if days_remaining is not None and days_remaining < 0:
                    overdue_projects.append({
                        'proyecto': project.get('ID_Proyecto'),
                        'cliente': project.get('Cliente'),
                        'departamento': project.get('Departamento', 'N/A'),
                        'fecha_entrega': deadline_str,
                        'dias_vencimiento': abs(days_remaining),
                        'estado': project.get('Estado'),
                        'responsable': project.get('Responsable'),
                        'tipo_alerta': 'VENCIDO',
                        'descripcion': f"Proyecto vencido hace {abs(days_remaining)} días"
                    })
            except Exception as e:
                logger.warning(f"Error processing project: {str(e)}")
                continue
        
        return overdue_projects
    
    def detect_approaching_deadlines(self, projects: List[Dict]) -> List[Dict]:
        """
        Identify projects with approaching deadlines
        
        Args:
            projects: List of project dictionaries from sheet
        
        Returns:
            List of projects with approaching deadlines
        """
        approaching_projects = []
        
        for project in projects:
            try:
                # Skip if already completed
                if project.get('Estado') == 'Completado':
                    continue
                
                # Calculate days remaining
                deadline_str = project.get('Fecha_Entrega', '')
                if not deadline_str:
                    continue
                
                days_remaining = self.calculate_days_remaining(deadline_str)
                
                # If positive and within threshold, it's approaching
                if days_remaining is not None and 0 <= days_remaining <= self.alert_days_threshold:
                    approaching_projects.append({
                        'proyecto': project.get('ID_Proyecto'),
                        'cliente': project.get('Cliente'),
                        'departamento': project.get('Departamento', 'N/A'),
                        'fecha_entrega': deadline_str,
                        'dias_restantes': days_remaining,
                        'estado': project.get('Estado'),
                        'responsable': project.get('Responsable'),
                        'tipo_alerta': 'PROXIMO',
                        'descripcion': f"Plazo en {days_remaining} días"
                    })
            except Exception as e:
                logger.warning(f"Error processing project: {str(e)}")
                continue
        
        return approaching_projects
    
    def evaluate_all_alerts(self, projects: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """
        Evaluate all projects for alerts (both overdue and approaching)
        
        Args:
            projects: List of project dictionaries
        
        Returns:
            Tuple of (overdue_alerts, approaching_alerts)
        """
        overdue = self.detect_overdue_projects(projects)
        approaching = self.detect_approaching_deadlines(projects)
        
        total_alerts = len(overdue) + len(approaching)
        logger.info(f"Alert evaluation complete: {len(overdue)} overdue, {len(approaching)} approaching")
        
        return overdue, approaching
    
    def generate_alert_summary(self, overdue: List[Dict], approaching: List[Dict]) -> str:
        """
        Generate a human-readable summary of alerts
        
        Args:
            overdue: List of overdue projects
            approaching: List of approaching deadline projects
        
        Returns:
            Summary string
        """
        summary = []
        summary.append(f"{'='*60}")
        summary.append(f"RESUMEN DE ALERTAS - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        summary.append(f"{'='*60}")
        summary.append("")
        
        # Overdue section
        summary.append(f"PROYECTOS VENCIDOS: {len(overdue)}")
        for project in overdue:
            summary.append(f"  • {project['proyecto']} - {project['cliente']}")
            summary.append(f"    Departamento: {project['departamento']}")
            summary.append(f"    Vencido hace: {project['dias_vencimiento']} días")
            summary.append(f"    Responsable: {project['responsable']}")
            summary.append("")
        
        # Approaching section
        summary.append(f"PLAZOS PRÓXIMOS (próximos {self.alert_days_threshold} días): {len(approaching)}")
        for project in approaching:
            summary.append(f"  • {project['proyecto']} - {project['cliente']}")
            summary.append(f"    Departamento: {project['departamento']}")
            summary.append(f"    Días restantes: {project['dias_restantes']}")
            summary.append(f"    Responsable: {project['responsable']}")
            summary.append("")
        
        summary.append(f"{'='*60}")
        
        return "\n".join(summary)
