"""
Notifier Module
Handles alert notifications via logging and optional email
"""

import logging
import smtplib
from datetime import datetime
from typing import List, Dict
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)


class Notifier:
    """Handles notification delivery via logging and email"""
    
    def __init__(self,
                 log_file_path: str,
                 smtp_server: str = None,
                 smtp_port: int = 587,
                 smtp_user: str = None,
                 smtp_password: str = None,
                 alert_recipients: List[str] = None):
        """
        Initialize Notifier
        
        Args:
            log_file_path: Path to alert log file
            smtp_server: SMTP server address (optional)
            smtp_port: SMTP port (default 587)
            smtp_user: SMTP username (optional)
            smtp_password: SMTP password (optional)
            alert_recipients: List of email addresses for alerts (optional)
        """
        self.log_file_path = log_file_path
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.alert_recipients = alert_recipients or []
        
        # Setup alert logger
        self.alert_logger = self._setup_alert_logger()
        logger.info("Notifier initialized")
    
    def _setup_alert_logger(self):
        """Setup a separate logger for alerts"""
        alert_logger = logging.getLogger('alerts')
        alert_logger.setLevel(logging.INFO)
        
        # Create file handler
        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%d/%m/%Y %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        # Add handler to logger
        alert_logger.addHandler(file_handler)
        
        return alert_logger
    
    def log_alert(self, alert: Dict) -> bool:
        """
        Log an alert to the alert log file
        
        Args:
            alert: Dictionary with alert information
        
        Returns:
            True if successful, False otherwise
        """
        try:
            alert_message = (
                f"[{alert.get('tipo_alerta')}] "
                f"{alert.get('proyecto')} - {alert.get('cliente')} - "
                f"Depto: {alert.get('departamento')} - "
                f"{alert.get('descripcion')}"
            )
            
            self.alert_logger.warning(alert_message)
            return True
        except Exception as e:
            logger.error(f"Error logging alert: {str(e)}")
            return False
    
    def log_alerts_batch(self, alerts: List[Dict]) -> int:
        """
        Log multiple alerts
        
        Args:
            alerts: List of alert dictionaries
        
        Returns:
            Number of alerts logged successfully
        """
        success_count = 0
        
        for alert in alerts:
            if self.log_alert(alert):
                success_count += 1
        
        logger.info(f"Logged {success_count}/{len(alerts)} alerts")
        return success_count
    
    def send_email_alert(self, subject: str, body: str) -> bool:
        """
        Send alert via email using SMTP
        
        Args:
            subject: Email subject
            body: Email body (text)
        
        Returns:
            True if successful, False otherwise
        """
        if not self.smtp_server or not self.smtp_user or not self.alert_recipients:
            logger.warning("Email not configured. Skipping email notification.")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.smtp_user
            msg['To'] = ', '.join(self.alert_recipients)
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Alert email sent to {len(self.alert_recipients)} recipients")
            return True
        except Exception as e:
            logger.error(f"Failed to send email alert: {str(e)}")
            return False
    
    def send_alerts_summary(self, overdue_alerts: List[Dict], approaching_alerts: List[Dict]) -> bool:
        """
        Send a consolidated alert summary via email
        
        Args:
            overdue_alerts: List of overdue project alerts
            approaching_alerts: List of approaching deadline alerts
        
        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.alert_recipients:
            logger.warning("No alert recipients configured. Skipping email.")
            return False
        
        try:
            # Build email subject
            subject = (
                f"ALERTAS DE PROYECTOS - {datetime.now().strftime('%d/%m/%Y')} "
                f"({len(overdue_alerts)} vencidos, {len(approaching_alerts)} próximos)"
            )
            
            # Build email body
            body_lines = []
            body_lines.append("=" * 70)
            body_lines.append(f"RESUMEN DE ALERTAS DE PROYECTOS")
            body_lines.append(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            body_lines.append("=" * 70)
            body_lines.append("")
            
            # Overdue section
            body_lines.append(f"PROYECTOS VENCIDOS ({len(overdue_alerts)})")
            body_lines.append("-" * 70)
            if overdue_alerts:
                for alert in overdue_alerts:
                    body_lines.append(f"  • {alert['proyecto']} - {alert['cliente']}")
                    body_lines.append(f"    Departamento: {alert['departamento']}")
                    body_lines.append(f"    Vencido desde: {alert['fecha_entrega']} ({alert['dias_vencimiento']} días)")
                    body_lines.append(f"    Responsable: {alert['responsable']}")
                    body_lines.append("")
            else:
                body_lines.append("  No hay proyectos vencidos.\n")
            
            # Approaching section
            body_lines.append(f"PLAZOS PRÓXIMOS ({len(approaching_alerts)})")
            body_lines.append("-" * 70)
            if approaching_alerts:
                for alert in approaching_alerts:
                    body_lines.append(f"  • {alert['proyecto']} - {alert['cliente']}")
                    body_lines.append(f"    Departamento: {alert['departamento']}")
                    body_lines.append(f"    Plazo: {alert['fecha_entrega']} ({alert['dias_restantes']} días restantes)")
                    body_lines.append(f"    Responsable: {alert['responsable']}")
                    body_lines.append("")
            else:
                body_lines.append("  No hay plazos próximos.\n")
            
            body_lines.append("=" * 70)
            body = "\n".join(body_lines)
            
            # Send email
            return self.send_email_alert(subject, body)
        except Exception as e:
            logger.error(f"Error building alert summary: {str(e)}")
            return False
    
    def log_consolidation(self, summary: Dict) -> bool:
        """
        Log consolidation summary
        
        Args:
            summary: Consolidation summary dictionary
        
        Returns:
            True if successful, False otherwise
        """
        try:
            log_message = f"[CONSOLIDATION] Consolidated data: {summary}"
            self.alert_logger.info(log_message)
            return True
        except Exception as e:
            logger.error(f"Error logging consolidation: {str(e)}")
            return False
    
    def log_execution_summary(self, execution_details: Dict) -> bool:
        """
        Log a summary of script execution
        
        Args:
            execution_details: Dictionary with execution information
        
        Returns:
            True if successful, False otherwise
        """
        try:
            lines = []
            lines.append("")
            lines.append("=" * 70)
            lines.append(f"RESUMEN DE EJECUCIÓN - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            lines.append("=" * 70)
            
            for key, value in execution_details.items():
                lines.append(f"{key}: {value}")
            
            lines.append("=" * 70)
            lines.append("")
            
            message = "\n".join(lines)
            self.alert_logger.info(message)
            return True
        except Exception as e:
            logger.error(f"Error logging execution summary: {str(e)}")
            return False
