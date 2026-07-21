"""
Authentication Module
Handles Google Cloud authentication using OAuth2 or Service Account credentials
"""

import logging
import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)


class GoogleAuth:
    """Handles authentication with Google APIs using OAuth2 or Service Account"""
    
    DRIVE_SCOPE = 'https://www.googleapis.com/auth/drive'
    SHEETS_SCOPE = 'https://www.googleapis.com/auth/spreadsheets'
    GMAIL_SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'
    SCOPES = [DRIVE_SCOPE, SHEETS_SCOPE, GMAIL_SCOPE]
    
    def __init__(self, token_path: str = None, credentials_file: str = None):
        """
        Initialize Google Authentication
        
        Args:
            token_path: Path to OAuth2 token JSON file (preferred)
            credentials_file: Path to service account JSON credentials file (fallback)
        """
        self.token_path = token_path
        self.credentials_file = credentials_file
        self.credentials = None
        self.drive_service = None
        self.sheets_service = None
        self.gmail_service = None
        self.auth_method = None
        
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Cloud using available credentials"""
        try:
            # Try OAuth token first
            if self.token_path and os.path.exists(self.token_path):
                self._authenticate_oauth()
            # Fallback to service account
            elif self.credentials_file and os.path.exists(self.credentials_file):
                self._authenticate_service_account()
            else:
                raise FileNotFoundError("No valid credentials found")
            
            # Build services
            self.drive_service = build('drive', 'v3', credentials=self.credentials)
            self.sheets_service = build('sheets', 'v4', credentials=self.credentials)
            self.gmail_service = build('gmail', 'v1', credentials=self.credentials)
            
            logger.info(f"Successfully authenticated with Google Cloud")
            logger.info(f"Authentication method: {self.auth_method}")
            
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            raise
    
    def _authenticate_oauth(self):
        """Authenticate using OAuth2 token"""
        try:
            logger.info(f"Loading OAuth2 token from: {self.token_path}")
            self.credentials = Credentials.from_authorized_user_file(
                self.token_path,
                scopes=self.SCOPES
            )
            
            # Refresh token if needed
            if self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
                logger.info("Token refreshed successfully")
            
            self.auth_method = "OAuth2"
            logger.info("OAuth2 authentication successful")
            
        except Exception as e:
            logger.error(f"OAuth2 authentication failed: {str(e)}")
            raise
    
    def _authenticate_service_account(self):
        """Authenticate using Service Account credentials"""
        try:
            logger.info(f"Loading Service Account credentials from: {self.credentials_file}")
            self.credentials = ServiceAccountCredentials.from_service_account_file(
                self.credentials_file,
                scopes=self.SCOPES
            )
            
            self.auth_method = "Service Account"
            logger.info(f"Service Account: {self.credentials.service_account_email}")
            logger.info("Service Account authentication successful")
            
        except Exception as e:
            logger.error(f"Service Account authentication failed: {str(e)}")
            raise
    
    def get_drive_service(self):
        """Get the authenticated Google Drive service"""
        return self.drive_service
    
    def get_sheets_service(self):
        """Get the authenticated Google Sheets service"""
        return self.sheets_service
    
    def get_gmail_service(self):
        """Get the authenticated Gmail service"""
        return self.gmail_service
    
    def get_credentials(self):
        """Get the credentials object"""
        return self.credentials
    
    def get_auth_method(self):
        """Get the authentication method used"""
        return self.auth_method
