"""
Google Drive Manager Module
Handles folder creation and management in Google Drive
"""

import logging
from typing import Dict, List, Optional
from modules.auth import GoogleAuth

logger = logging.getLogger(__name__)


class DriveManager:
    """Manages Google Drive operations"""
    
    def __init__(self, auth: GoogleAuth):
        """
        Initialize Drive Manager
        
        Args:
            auth: GoogleAuth instance with authenticated service
        """
        self.service = auth.get_drive_service()
        logger.info("Drive Manager initialized successfully")
    
    def create_folder(self, folder_name: str, parent_id: Optional[str] = None) -> str:
        """
        Create a folder in Google Drive
        
        Args:
            folder_name: Name of the folder to create
            parent_id: Parent folder ID (if None, creates in root)
        
        Returns:
            Folder ID
        """
        try:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            if parent_id:
                file_metadata['parents'] = [parent_id]
            
            result = self.service.files().create(body=file_metadata, fields='id').execute()
            folder_id = result.get('id')
            logger.info(f"Folder created: {folder_name} (ID: {folder_id})")
            return folder_id
        except Exception as e:
            logger.error(f"Failed to create folder {folder_name}: {str(e)}")
            raise
    
    def get_folder_id(self, folder_name: str, parent_id: Optional[str] = None) -> Optional[str]:
        """
        Get folder ID by name
        
        Args:
            folder_name: Name of the folder to find
            parent_id: Parent folder ID to search in
        
        Returns:
            Folder ID or None if not found
        """
        try:
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            if parent_id:
                query += f" and '{parent_id}' in parents"
            
            results = self.service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
            files = results.get('files', [])
            
            if files:
                logger.info(f"Folder found: {folder_name} (ID: {files[0]['id']})")
                return files[0]['id']
            else:
                logger.debug(f"Folder not found: {folder_name}")
                return None
        except Exception as e:
            logger.error(f"Failed to get folder {folder_name}: {str(e)}")
            return None
    
    def get_or_create_folder(self, folder_name: str, parent_id: Optional[str] = None) -> str:
        """
        Get folder ID if exists, otherwise create it
        
        Args:
            folder_name: Name of the folder
            parent_id: Parent folder ID
        
        Returns:
            Folder ID
        """
        existing_id = self.get_folder_id(folder_name, parent_id)
        if existing_id:
            return existing_id
        else:
            return self.create_folder(folder_name, parent_id)
    
    def list_folders(self, parent_id: Optional[str] = None) -> List[Dict]:
        """
        List all folders in a directory
        
        Args:
            parent_id: Parent folder ID
        
        Returns:
            List of folder dictionaries
        """
        try:
            query = "mimeType='application/vnd.google-apps.folder' and trashed=false"
            if parent_id:
                query += f" and '{parent_id}' in parents"
            
            results = self.service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
            folders = results.get('files', [])
            logger.info(f"Found {len(folders)} folders")
            return folders
        except Exception as e:
            logger.error(f"Failed to list folders: {str(e)}")
            return []
    
    def share_folder(self, folder_id: str, email: str, role: str = 'editor') -> bool:
        """
        Share a folder with a user
        
        Args:
            folder_id: Folder ID to share
            email: Email address to share with
            role: Role (viewer, commenter, editor, owner)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            permission = {
                'type': 'user',
                'role': role,
                'emailAddress': email
            }
            self.service.permissions().create(fileId=folder_id, body=permission).execute()
            logger.info(f"Folder {folder_id} shared with {email} as {role}")
            return True
        except Exception as e:
            logger.error(f"Failed to share folder: {str(e)}")
            return False

