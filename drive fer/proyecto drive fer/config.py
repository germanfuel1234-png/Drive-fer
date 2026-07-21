"""
Configuration module for Project Scheduler
Manages environment variables and system settings
"""

import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class"""
    
    # === AUTENTICACIÓN GOOGLE ===
    GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH', './credentials.json')
    
    # === DRIVE CONFIGURATION ===
    DRIVE_ROOT_FOLDER_NAME = os.getenv('DRIVE_ROOT_FOLDER_NAME', 'Proyectos_Empresa')
    DRIVE_ROOT_FOLDER_ID = os.getenv('DRIVE_ROOT_FOLDER_ID', '')
    
    # === DEPARTMENTS CONFIGURATION ===
    DEPARTMENTS_LIST = os.getenv('DEPARTMENTS', 'Ingenieria,Obras,Mantenimiento').split(',')
    DEPARTMENTS = {dept.strip(): {} for dept in DEPARTMENTS_LIST}
    
    # Sheet IDs por departamento (cargar desde env)
    for i, dept in enumerate(DEPARTMENTS_LIST):
        dept_clean = dept.strip()
        sheet_var = f'SHEET_{dept_clean.upper()}_ID'
        DEPARTMENTS[dept_clean]['sheet_id'] = os.getenv(sheet_var, '')
    
    # === MASTER SCHEDULE CONFIGURATION ===
    SHEET_MAESTRO_ID = os.getenv('SHEET_MAESTRO_ID', '')
    MASTER_SCHEDULE_NAME = 'Cronograma_Maestro'
    
    # === SHEET SCHEMA (Columnas obligatorias) ===
    DEPARTMENT_SHEET_HEADERS = [
        'ID_Proyecto',
        'Cliente',
        'Descripcion',
        'Fecha_Inicio',
        'Fecha_Entrega',
        'Estado',
        'Responsable'
    ]
    
    MASTER_SHEET_HEADERS = DEPARTMENT_SHEET_HEADERS + ['Departamento']
    
    # === ESTADO VALUES ===
    VALID_STATES = ['Pendiente', 'En progreso', 'Completado', 'Retrasado']
    
    # === ALERTAS CONFIGURATION ===
    ALERT_DAYS_THRESHOLD = int(os.getenv('ALERT_DAYS_THRESHOLD', 3))
    LOG_FILE_PATH = os.getenv('LOG_FILE_PATH', './alertas_cronograma.log')
    
    # === EMAIL CONFIGURATION (SMTP) ===
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_USER = os.getenv('SMTP_USER', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    ALERT_RECIPIENTS = os.getenv('ALERT_RECIPIENTS', '').split(',') if os.getenv('ALERT_RECIPIENTS') else []
    
    # === LOGGING CONFIGURATION ===
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', './logs/project_scheduler.log')
    
    # Create logs directories if they don't exist
    Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    Path(LOG_FILE_PATH).parent.mkdir(parents=True, exist_ok=True)
    
    # === CACHE FILE FOR IDs ===
    CACHE_IDS_FILE = '.cache_sheet_ids.json'
    
    @classmethod
    def load_cached_ids(cls):
        """Load sheet IDs from cache file"""
        if not os.path.exists(cls.CACHE_IDS_FILE):
            return False
        
        try:
            with open(cls.CACHE_IDS_FILE, 'r') as f:
                cached = json.load(f)
            
            # Load root folder ID
            if 'root_folder_id' in cached:
                cls.DRIVE_ROOT_FOLDER_ID = cached['root_folder_id']
            
            # Load master sheet ID
            if 'master_sheet_id' in cached:
                cls.SHEET_MAESTRO_ID = cached['master_sheet_id']
            
            # Load department sheet IDs
            if 'departments' in cached:
                for dept, data in cached['departments'].items():
                    if dept in cls.DEPARTMENTS:
                        cls.DEPARTMENTS[dept].update(data)
            
            return True
        except Exception as e:
            logging.warning(f"Error loading cached IDs: {e}")
            return False
    
    @classmethod
    def save_cached_ids(cls):
        """Save sheet IDs to cache file"""
        try:
            cache_data = {
                'root_folder_id': cls.DRIVE_ROOT_FOLDER_ID,
                'master_sheet_id': cls.SHEET_MAESTRO_ID,
                'departments': cls.DEPARTMENTS
            }
            
            with open(cls.CACHE_IDS_FILE, 'w') as f:
                json.dump(cache_data, f, indent=2)
            
            return True
        except Exception as e:
            logging.warning(f"Error saving cached IDs: {e}")
            return False
    
    @staticmethod
    def setup_logging():
        """Setup logging configuration"""
        logging.basicConfig(
            level=getattr(logging, Config.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(Config.LOG_FILE),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

# Initialize logger
logger = Config.setup_logging()
