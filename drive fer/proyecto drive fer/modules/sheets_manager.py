"""
Google Sheets Manager Module
Handles spreadsheet creation and management
"""

import logging
from typing import Dict, List, Optional, Any
from modules.auth import GoogleAuth

logger = logging.getLogger(__name__)


class SheetsManager:
    """Manages Google Sheets operations"""
    
    def __init__(self, auth: GoogleAuth):
        """
        Initialize Sheets Manager
        
        Args:
            auth: GoogleAuth instance with authenticated service
        """
        self.sheets_service = auth.get_sheets_service()
        self.drive_service = auth.get_drive_service()
        logger.info("Sheets Manager initialized successfully")
    
    def _escape_sheet_name(self, sheet_name: str) -> str:
        """
        Escape sheet name for use in range notation
        Adds single quotes around names containing special characters
        
        Args:
            sheet_name: Original sheet name
            
        Returns:
            Escaped sheet name suitable for A1 notation
        """
        # Check if name needs escaping (contains special chars, spaces, etc.)
        needs_escaping = any(c in sheet_name for c in "áéíóúÁÉÍÓÚ ñÑ'\"!@#$%^&*()")
        
        if needs_escaping:
            # Escape single quotes by doubling them
            escaped = sheet_name.replace("'", "''")
            return f"'{escaped}'"
        return sheet_name
    
    def _build_range(self, sheet_name: str, cell_range: str = "A1") -> str:
        """
        Build a proper A1 notation range with escaped sheet name
        
        Args:
            sheet_name: Sheet name
            cell_range: Cell range (e.g., "A1", "A:G", "A1:C10")
            
        Returns:
            Properly formatted range for Google Sheets API
        """
        escaped_name = self._escape_sheet_name(sheet_name)
        return f"{escaped_name}!{cell_range}"
    
    def create_spreadsheet(self, title: str, folder_id: Optional[str] = None) -> str:
        """
        Create a new Google Sheet
        
        Args:
            title: Spreadsheet title
            folder_id: Folder to place the spreadsheet in
        
        Returns:
            Spreadsheet ID
        """
        try:
            spreadsheet = {
                'properties': {
                    'title': title,
                    'locale': 'es_ES',
                    'autoRecalc': 'ON_CHANGE'
                }
            }
            
            result = self.sheets_service.spreadsheets().create(body=spreadsheet).execute()
            sheet_id = result.get('spreadsheetId')
            
            # Move to folder if specified
            if folder_id:
                self.drive_service.files().update(
                    fileId=sheet_id,
                    addParents=folder_id,
                    removeParents='root',
                    fields='id, parents'
                ).execute()
            
            logger.info(f"Spreadsheet created: {title} (ID: {sheet_id})")
            return sheet_id
        except Exception as e:
            logger.error(f"Failed to create spreadsheet: {str(e)}")
            raise
    
    def get_spreadsheet_id(self, title: str) -> Optional[str]:
        """
        Find spreadsheet ID by title
        
        Args:
            title: Spreadsheet title
        
        Returns:
            Spreadsheet ID or None if not found
        """
        try:
            query = f"name='{title}' and mimeType='application/vnd.google-apps.spreadsheet' and trashed=false"
            results = self.drive_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
            files = results.get('files', [])
            
            if files:
                logger.info(f"Spreadsheet found: {title} (ID: {files[0]['id']})")
                return files[0]['id']
            else:
                logger.debug(f"Spreadsheet not found: {title}")
                return None
        except Exception as e:
            logger.error(f"Failed to get spreadsheet {title}: {str(e)}")
            return None
    
    def get_or_create_spreadsheet(self, title: str, folder_id: Optional[str] = None) -> str:
        """
        Get spreadsheet ID if exists, otherwise create it
        
        Args:
            title: Spreadsheet title
            folder_id: Folder ID for new spreadsheet
        
        Returns:
            Spreadsheet ID
        """
        existing_id = self.get_spreadsheet_id(title)
        if existing_id:
            return existing_id
        else:
            return self.create_spreadsheet(title, folder_id)
    
    def get_sheet_names(self, spreadsheet_id: str) -> List[str]:
        """
        Get all sheet names in a spreadsheet
        
        Args:
            spreadsheet_id: Spreadsheet ID
            
        Returns:
            List of sheet names
        """
        try:
            metadata = self.sheets_service.spreadsheets().get(
                spreadsheetId=spreadsheet_id,
                fields='sheets.properties.title'
            ).execute()
            
            sheets = metadata.get('sheets', [])
            names = [sheet['properties']['title'] for sheet in sheets]
            
            logger.info(f"Sheet names for {spreadsheet_id}: {names}")
            return names
            
        except Exception as e:
            logger.error(f"Failed to get sheet names: {str(e)}")
            return []
    
    def rename_sheet(self, spreadsheet_id: str, old_name: str, new_name: str) -> bool:
        """
        Rename a sheet in a spreadsheet
        
        Args:
            spreadsheet_id: Spreadsheet ID
            old_name: Current sheet name
            new_name: New sheet name
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get sheet ID from name
            metadata = self.sheets_service.spreadsheets().get(
                spreadsheetId=spreadsheet_id,
                fields='sheets.properties'
            ).execute()
            
            sheet_id = None
            for sheet in metadata.get('sheets', []):
                if sheet['properties']['title'] == old_name:
                    sheet_id = sheet['properties']['sheetId']
                    break
            
            if sheet_id is None:
                logger.warning(f"Sheet '{old_name}' not found")
                return False
            
            # Rename the sheet
            requests = [
                {
                    'updateSheetProperties': {
                        'properties': {
                            'sheetId': sheet_id,
                            'title': new_name
                        },
                        'fields': 'title'
                    }
                }
            ]
            
            self.sheets_service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={'requests': requests}
            ).execute()
            
            logger.info(f"Sheet renamed: '{old_name}' → '{new_name}'")
            return True
            
        except Exception as e:
            logger.error(f"Failed to rename sheet: {str(e)}")
            return False
    
    def ensure_sheet_name(self, spreadsheet_id: str, desired_name: str) -> str:
        """
        Ensure a sheet with the desired name exists
        If it doesn't, rename the first sheet to this name
        
        Args:
            spreadsheet_id: Spreadsheet ID
            desired_name: Desired sheet name
            
        Returns:
            Actual sheet name to use
        """
        try:
            sheets = self.get_sheet_names(spreadsheet_id)
            
            # If desired name already exists, use it
            if desired_name in sheets:
                logger.info(f"Sheet '{desired_name}' already exists")
                return desired_name
            
            # Otherwise rename the first sheet
            if sheets:
                first_sheet = sheets[0]
                self.rename_sheet(spreadsheet_id, first_sheet, desired_name)
                logger.info(f"First sheet renamed to '{desired_name}'")
                return desired_name
            
            logger.warning("No sheets found in spreadsheet")
            return desired_name
            
        except Exception as e:
            logger.error(f"Failed to ensure sheet name: {str(e)}")
            return desired_name
    
    def add_sheet(self, spreadsheet_id: str, sheet_title: str) -> Dict[str, Any]:
        """
        Add a new sheet to a spreadsheet
        
        Args:
            spreadsheet_id: Spreadsheet ID
            sheet_title: Title for the new sheet
        
        Returns:
            Sheet properties dictionary
        """
        try:
            batch_update_body = {
                'requests': [
                    {
                        'addSheet': {
                            'properties': {
                                'title': sheet_title
                            }
                        }
                    }
                ]
            }
            
            result = self.sheets_service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=batch_update_body
            ).execute()
            
            logger.info(f"Sheet added to {spreadsheet_id}: {sheet_title}")
            return result['replies'][0]['addSheet']['properties']
        except Exception as e:
            logger.error(f"Failed to add sheet: {str(e)}")
            raise
    
    def write_data(self, spreadsheet_id: str, range_: str, values: List[List[Any]]) -> bool:
        """
        Write data to a spreadsheet
        
        Args:
            spreadsheet_id: Spreadsheet ID
            range_: Range in A1 notation (e.g., 'Sheet1!A1:C10')
            values: Data to write (list of lists)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            body = {
                'values': values
            }
            
            result = self.sheets_service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            logger.info(f"Data written to {spreadsheet_id}: {range_} ({len(values)} rows)")
            return True
        except Exception as e:
            logger.error(f"Failed to write data: {str(e)}")
            return False
    
    def read_data(self, spreadsheet_id: str, range_: str) -> List[List[Any]]:
        """
        Read data from a spreadsheet
        
        Args:
            spreadsheet_id: Spreadsheet ID
            range_: Range in A1 notation
        
        Returns:
            Data from the range
        """
        try:
            result = self.sheets_service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_
            ).execute()
            
            values = result.get('values', [])
            logger.info(f"Data read from {spreadsheet_id}: {range_} ({len(values)} rows)")
            return values
        except Exception as e:
            logger.error(f"Failed to read data: {str(e)}")
            return []
    
    def append_data(self, spreadsheet_id: str, range_: str, values: List[List[Any]]) -> bool:
        """
        Append data to a spreadsheet
        
        Args:
            spreadsheet_id: Spreadsheet ID
            range_: Range in A1 notation
            values: Data to append
        
        Returns:
            True if successful, False otherwise
        """
        try:
            body = {
                'values': values
            }
            
            result = self.sheets_service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=range_,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            logger.info(f"Data appended to {spreadsheet_id}: {range_} ({len(values)} rows)")
            return True
        except Exception as e:
            logger.error(f"Failed to append data: {str(e)}")
            return False
    
    def clear_sheet(self, spreadsheet_id: str, range_: str) -> bool:
        """
        Clear data from a spreadsheet range
        
        Args:
            spreadsheet_id: Spreadsheet ID
            range_: Range in A1 notation
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.sheets_service.spreadsheets().values().clear(
                spreadsheetId=spreadsheet_id,
                range=range_,
                body={}
            ).execute()
            
            logger.info(f"Data cleared from {spreadsheet_id}: {range_}")
            return True
        except Exception as e:
            logger.error(f"Failed to clear data: {str(e)}")
            return False
    
    def create_headers(self, spreadsheet_id: str, sheet_name: str, headers: List[str]) -> bool:
        """
        Create header row in a sheet
        
        Args:
            spreadsheet_id: Spreadsheet ID
            sheet_name: Sheet name
            headers: List of header names
        
        Returns:
            True if successful, False otherwise
        """
        # First ensure the sheet has the correct name
        actual_sheet_name = self.ensure_sheet_name(spreadsheet_id, sheet_name)
        
        headers_data = [headers]
        range_ = self._build_range(actual_sheet_name, "A1")
        return self.write_data(
            spreadsheet_id,
            range_,
            headers_data
        )

