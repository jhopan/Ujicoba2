"""
Google Drive Manager untuk handle upload dan download
"""

import os
import io
import json
import pickle
from pathlib import Path
import os
import sys
import logging
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError

# Add project root to path untuk import config
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import GOOGLE_DRIVE_CONFIG

class GoogleDriveManager:
    """Class untuk mengelola operasi Google Drive"""
    
    def __init__(self, account_index=0):
        self.account_index = account_index
        self.service = None
        self.backup_folder_id = None
        self.logger = logging.getLogger(__name__)
        self._authenticate()
        
    def _authenticate(self):
        """Authenticate dengan Google Drive API"""
        creds = None
        token_file = f"token_account_{self.account_index}.json"
        token_path = Path(GOOGLE_DRIVE_CONFIG["credentials_file"]).parent / token_file
        
        # Load existing token
        if token_path.exists():
            creds = Credentials.from_authorized_user_file(str(token_path), 
                                                        GOOGLE_DRIVE_CONFIG["scopes"])
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    GOOGLE_DRIVE_CONFIG["credentials_file"], 
                    GOOGLE_DRIVE_CONFIG["scopes"])
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('drive', 'v3', credentials=creds)
        self._create_backup_folder()
        
    def _create_backup_folder(self):
        """Buat folder backup di Google Drive jika belum ada"""
        try:
            # Cari folder backup yang sudah ada
            query = f"name='{GOOGLE_DRIVE_CONFIG['folder_name']}' and mimeType='application/vnd.google-apps.folder'"
            results = self.service.files().list(q=query).execute()
            items = results.get('files', [])
            
            if items:
                self.backup_folder_id = items[0]['id']
                self.logger.info(f"Found existing backup folder: {items[0]['name']}")
            else:
                # Buat folder baru
                folder_metadata = {
                    'name': GOOGLE_DRIVE_CONFIG['folder_name'],
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                folder = self.service.files().create(body=folder_metadata, fields='id').execute()
                self.backup_folder_id = folder.get('id')
                self.logger.info(f"Created new backup folder with ID: {self.backup_folder_id}")
                
        except HttpError as error:
            self.logger.error(f"Error creating backup folder: {error}")
            raise
            
    def upload_file(self, file_path, remote_name=None):
        """Upload file ke Google Drive"""
        try:
            if not remote_name:
                remote_name = Path(file_path).name
                
            # Check if file already exists
            existing_file = self.find_file(remote_name)
            
            file_metadata = {
                'name': remote_name,
                'parents': [self.backup_folder_id]
            }
            
            media = MediaFileUpload(file_path, resumable=True)
            
            if existing_file:
                # Update existing file
                file = self.service.files().update(
                    fileId=existing_file['id'],
                    body=file_metadata,
                    media_body=media
                ).execute()
                self.logger.info(f"Updated file: {remote_name}")
            else:
                # Create new file
                file = self.service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id'
                ).execute()
                self.logger.info(f"Uploaded new file: {remote_name}")
                
            return file.get('id')
            
        except HttpError as error:
            self.logger.error(f"Error uploading file {file_path}: {error}")
            raise
            
    def download_file(self, file_id, local_path):
        """Download file dari Google Drive"""
        try:
            request = self.service.files().get_media(fileId=file_id)
            file_io = io.BytesIO()
            downloader = MediaIoBaseDownload(file_io, request)
            
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                
            # Write to local file
            with open(local_path, 'wb') as f:
                f.write(file_io.getvalue())
                
            self.logger.info(f"Downloaded file to: {local_path}")
            return True
            
        except HttpError as error:
            self.logger.error(f"Error downloading file: {error}")
            return False
            
    def find_file(self, filename):
        """Cari file berdasarkan nama"""
        try:
            query = f"name='{filename}' and parents in '{self.backup_folder_id}'"
            results = self.service.files().list(q=query).execute()
            items = results.get('files', [])
            return items[0] if items else None
            
        except HttpError as error:
            self.logger.error(f"Error finding file {filename}: {error}")
            return None
            
    def get_storage_usage(self):
        """Dapatkan informasi penggunaan storage"""
        try:
            about = self.service.about().get(fields='storageQuota').execute()
            quota = about.get('storageQuota', {})
            
            total = int(quota.get('limit', 0))
            used = int(quota.get('usage', 0))
            available = total - used
            
            return {
                'total_gb': total / (1024**3),
                'used_gb': used / (1024**3),
                'available_gb': available / (1024**3)
            }
            
        except HttpError as error:
            self.logger.error(f"Error getting storage usage: {error}")
            return None
            
    def list_files(self):
        """List semua file dalam folder backup"""
        try:
            query = f"parents in '{self.backup_folder_id}'"
            results = self.service.files().list(q=query, fields='files(id, name, size, modifiedTime)').execute()
            return results.get('files', [])
            
        except HttpError as error:
            self.logger.error(f"Error listing files: {error}")
            return []
