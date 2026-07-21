"""
Scheduler Manager Module
Consolidates and manages project schedules across departments
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import pandas as pd
from .sheets_manager import SheetsManager

logger = logging.getLogger(__name__)


class SchedulerManager:
    """Manages project scheduling and consolidation"""
    
    def __init__(self, sheets_manager: SheetsManager, credentials_file: str):
        """
        Initialize Scheduler Manager
        
        Args:
            sheets_manager: SheetsManager instance
            credentials_file: Path to credentials file
        """
        self.sheets_manager = sheets_manager
        self.credentials_file = credentials_file
        logger.info("Scheduler Manager initialized successfully")
    
    def initialize_department_schedule(self, 
                                      spreadsheet_id: str, 
                                      department_name: str) -> bool:
        """
        Initialize a department's schedule sheet
        
        Args:
            spreadsheet_id: Spreadsheet ID
            department_name: Department name
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Remove default sheet if it exists
            self._remove_default_sheet(spreadsheet_id)
            
            # Add department sheet
            sheet_props = self.sheets_manager.add_sheet(
                spreadsheet_id,
                department_name
            )
            
            # Create header row
            self.sheets_manager.create_header_row(
                spreadsheet_id,
                department_name
            )
            
            # Format header
            self.sheets_manager.format_header_row(
                spreadsheet_id,
                sheet_props['sheetId']
            )
            
            logger.info(f"Department schedule initialized: {department_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize department schedule: {str(e)}")
            return False
    
    def _remove_default_sheet(self, spreadsheet_id: str) -> bool:
        """Remove the default sheet created with spreadsheet"""
        try:
            # Get spreadsheet properties to find the default sheet
            result = self.sheets_manager.sheets_service.spreadsheets().get(
                spreadsheetId=spreadsheet_id
            ).execute()
            
            sheets = result.get('sheets', [])
            if sheets and sheets[0].get('properties', {}).get('title') == 'Sheet1':
                sheet_id = sheets[0]['properties']['sheetId']
                
                batch_update_body = {
                    'requests': [
                        {
                            'deleteSheet': {
                                'sheetId': sheet_id
                            }
                        }
                    ]
                }
                
                self.sheets_manager.sheets_service.spreadsheets().batchUpdate(
                    spreadsheetId=spreadsheet_id,
                    body=batch_update_body
                ).execute()
                
                logger.info(f"Default sheet removed from {spreadsheet_id}")
            return True
        except Exception as e:
            logger.warning(f"Could not remove default sheet: {str(e)}")
            return False
    
    def add_project(self,
                   spreadsheet_id: str,
                   sheet_name: str,
                   project_data: Dict[str, Any]) -> bool:
        """
        Add a project to a department schedule
        
        Args:
            spreadsheet_id: Spreadsheet ID
            sheet_name: Sheet name (department name)
            project_data: Project information dictionary
        
        Returns:
            True if successful, False otherwise
        """
        try:
            values = [[
                project_data.get('id', ''),
                project_data.get('client', ''),
                project_data.get('description', ''),
                project_data.get('start_date', ''),
                project_data.get('end_date', ''),
                project_data.get('status', 'En Progreso'),
                project_data.get('responsible', ''),
                project_data.get('budget', ''),
                project_data.get('progress', 0),
                project_data.get('notes', '')
            ]]
            
            return self.sheets_manager.append_data(
                spreadsheet_id,
                f'{sheet_name}!A2:J2',
                values
            )
        except Exception as e:
            logger.error(f"Failed to add project: {str(e)}")
            return False
    
    def consolidate_schedules(self,
                             master_schedule_id: str,
                             department_schedules: Dict[str, str]) -> bool:
        """
        Consolidate all department schedules into master schedule
        
        Args:
            master_schedule_id: Master schedule spreadsheet ID
            department_schedules: Dictionary of {department_name: spreadsheet_id}
        
        Returns:
            True if successful, False otherwise
        """
        try:
            all_data = []
            
            for dept_name, sheet_id in department_schedules.items():
                # Read data from department schedule
                dept_data = self.sheets_manager.read_data(
                    sheet_id,
                    f'{dept_name}!A2:J'
                )
                
                # Add department column and append
                for row in dept_data:
                    if row:  # Skip empty rows
                        row.insert(0, dept_name)  # Add department as first column
                        all_data.append(row)
            
            # Write to master schedule
            if all_data:
                master_headers = [
                    ['Departamento', 'ID Proyecto', 'Cliente', 'Descripción', 
                     'Fecha Inicio', 'Fecha Fin', 'Estado', 'Responsable', 
                     'Presupuesto', 'Progreso (%)', 'Notas']
                ]
                
                # Write headers
                self.sheets_manager.write_data(
                    master_schedule_id,
                    'Cronograma Maestro!A1:K1',
                    master_headers
                )
                
                # Write data
                self.sheets_manager.write_data(
                    master_schedule_id,
                    'Cronograma Maestro!A2:K100',
                    all_data
                )
                
                logger.info(f"Consolidated {len(all_data)} projects into master schedule")
            
            return True
        except Exception as e:
            logger.error(f"Failed to consolidate schedules: {str(e)}")
            return False
    
    def get_schedule_summary(self, spreadsheet_id: str, sheet_name: str) -> Dict[str, Any]:
        """
        Get a summary of a schedule
        
        Args:
            spreadsheet_id: Spreadsheet ID
            sheet_name: Sheet name
        
        Returns:
            Summary dictionary
        """
        try:
            data = self.sheets_manager.read_data(
                spreadsheet_id,
                f'{sheet_name}!A:J'
            )
            
            if len(data) <= 1:
                return {
                    'total_projects': 0,
                    'in_progress': 0,
                    'completed': 0,
                    'on_hold': 0
                }
            
            # Skip header row
            rows = data[1:]
            
            summary = {
                'total_projects': len(rows),
                'in_progress': sum(1 for row in rows if len(row) > 5 and row[5] == 'En Progreso'),
                'completed': sum(1 for row in rows if len(row) > 5 and row[5] == 'Completado'),
                'on_hold': sum(1 for row in rows if len(row) > 5 and row[5] == 'En Pausa'),
                'last_updated': datetime.now().isoformat()
            }
            
            logger.info(f"Schedule summary for {sheet_name}: {summary}")
            return summary
        except Exception as e:
            logger.error(f"Failed to get schedule summary: {str(e)}")
            return {}
    
    def export_to_csv(self, spreadsheet_id: str, sheet_name: str, output_file: str) -> bool:
        """
        Export a schedule to CSV
        
        Args:
            spreadsheet_id: Spreadsheet ID
            sheet_name: Sheet name
            output_file: Output file path
        
        Returns:
            True if successful, False otherwise
        """
        try:
            data = self.sheets_manager.read_data(
                spreadsheet_id,
                f'{sheet_name}!A:J'
            )
            
            if data:
                df = pd.DataFrame(data[1:], columns=data[0] if data else [])
                df.to_csv(output_file, index=False, encoding='utf-8')
                logger.info(f"Schedule exported to {output_file}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to export schedule: {str(e)}")
            return False
