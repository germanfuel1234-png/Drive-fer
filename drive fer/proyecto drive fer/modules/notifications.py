"""
Notifications Manager Module
Handles alerts and notifications for project updates
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

logger = logging.getLogger(__name__)


class NotificationManager:
    """Manages notifications and alerts"""
    
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    def __init__(self, credentials_file: str, notification_email: str):
        """
        Initialize Notification Manager
        
        Args:
            credentials_file: Path to Google Cloud service account credentials
            notification_email: Email address to send notifications from
        """
        self.credentials_file = credentials_file
        self.notification_email = notification_email
        self.gmail_service = self._authenticate_gmail()
        logger.info("Notification Manager initialized successfully")
    
    def _authenticate_gmail(self):
        """Authenticate with Gmail API"""
        try:
            credentials = Credentials.from_service_account_file(
                self.credentials_file,
                scopes=self.SCOPES
            )
            service = build('gmail', 'v1', credentials=credentials)
            logger.info("Gmail authentication successful")
            return service
        except Exception as e:
            logger.error(f"Gmail authentication failed: {str(e)}")
            return None
    
    def check_service_requests(self) -> List[Dict]:
        """
        Check inbox for service request emails
        
        Returns:
            List of service request dictionaries
        """
        if not self.gmail_service:
            logger.warning("Gmail service not available")
            return []
        
        try:
            results = self.gmail_service.users().messages().list(
                userId='me',
                q='subject:pedido OR subject:solicitud OR subject:servicio',
                maxResults=10
            ).execute()
            
            messages = results.get('messages', [])
            service_requests = []
            
            for message in messages:
                request = self._parse_message(message['id'])
                if request:
                    service_requests.append(request)
            
            logger.info(f"Found {len(service_requests)} service requests")
            return service_requests
        except Exception as e:
            logger.error(f"Failed to check service requests: {str(e)}")
            return []
    
    def _parse_message(self, message_id: str) -> Optional[Dict]:
        """
        Parse a Gmail message to extract service request details
        
        Args:
            message_id: Gmail message ID
        
        Returns:
            Parsed message dictionary or None
        """
        try:
            message = self.gmail_service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            headers = message['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
            
            # Extract body
            body = ''
            if 'parts' in message['payload']:
                for part in message['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        body = part['body'].get('data', '')
                        break
            else:
                body = message['payload']['body'].get('data', '')
            
            return {
                'id': message_id,
                'subject': subject,
                'from': sender,
                'date': date,
                'body': body,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to parse message {message_id}: {str(e)}")
            return None
    
    def log_notification(self,
                        notification_type: str,
                        department: str,
                        client: str,
                        message: str,
                        project_id: Optional[str] = None) -> bool:
        """
        Log a notification to the logger
        
        Args:
            notification_type: Type of notification (alert, info, warning)
            department: Department name
            client: Client name
            message: Notification message
            project_id: Optional project ID
        
        Returns:
            True if successful, False otherwise
        """
        try:
            log_message = (
                f"[{notification_type.upper()}] Department: {department} | "
                f"Client: {client} | Project: {project_id or 'N/A'} | "
                f"Message: {message}"
            )
            
            if notification_type == 'alert':
                logger.warning(log_message)
            elif notification_type == 'warning':
                logger.warning(log_message)
            else:
                logger.info(log_message)
            
            return True
        except Exception as e:
            logger.error(f"Failed to log notification: {str(e)}")
            return False
    
    def check_deadlines(self,
                       schedules: Dict[str, List[Dict]],
                       days_threshold: int = 7) -> List[Dict]:
        """
        Check for approaching deadlines
        
        Args:
            schedules: Dictionary of {department: projects_list}
            days_threshold: Number of days to check ahead
        
        Returns:
            List of projects with approaching deadlines
        """
        from datetime import timedelta
        
        alerts = []
        today = datetime.now().date()
        threshold_date = today + timedelta(days=days_threshold)
        
        try:
            for dept_name, projects in schedules.items():
                for project in projects:
                    try:
                        end_date = datetime.strptime(
                            project.get('end_date', ''),
                            '%Y-%m-%d'
                        ).date()
                        
                        if today <= end_date <= threshold_date:
                            alerts.append({
                                'department': dept_name,
                                'project_id': project.get('id'),
                                'client': project.get('client'),
                                'end_date': str(end_date),
                                'days_remaining': (end_date - today).days,
                                'alert_type': 'deadline'
                            })
                    except ValueError:
                        continue
            
            logger.info(f"Found {len(alerts)} projects with approaching deadlines")
            return alerts
        except Exception as e:
            logger.error(f"Failed to check deadlines: {str(e)}")
            return []
    
    def generate_daily_summary(self,
                              schedules: Dict[str, List[Dict]]) -> str:
        """
        Generate a daily summary of all schedules
        
        Args:
            schedules: Dictionary of {department: projects_list}
        
        Returns:
            Summary string
        """
        try:
            summary = "=== RESUMEN DIARIO DE CRONOGRAMAS ===\n\n"
            summary += f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
            
            total_projects = 0
            total_in_progress = 0
            
            for dept_name, projects in schedules.items():
                in_progress = sum(
                    1 for p in projects 
                    if p.get('status') == 'En Progreso'
                )
                summary += f"{dept_name}:\n"
                summary += f"  - Total proyectos: {len(projects)}\n"
                summary += f"  - En progreso: {in_progress}\n\n"
                
                total_projects += len(projects)
                total_in_progress += in_progress
            
            summary += f"TOTAL:\n"
            summary += f"  - Proyectos totales: {total_projects}\n"
            summary += f"  - En progreso: {total_in_progress}\n"
            
            return summary
        except Exception as e:
            logger.error(f"Failed to generate summary: {str(e)}")
            return ""
