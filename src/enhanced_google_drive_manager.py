"""
Enhanced Google Drive Manager dengan fitur:
- Folder organization berdasarkan tanggal dan tipe file
- Upload progress tracking
- Better error handling
"""

import os
import io
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError
import logging

class EnhancedGoogleDriveManager:
    """Enhanced Google Drive Manager"""
    
    def __init__(self, account_index: int = 0, account_name: str = None):
        self.account_index = account_index
        self.account_name = account_name or f"Account {account_index}"
        self.service = None
        self.backup_root_folder_id = None
        self.folder_cache = {}  # Cache untuk folder IDs
        self.logger = logging.getLogger(__name__)
        self._authenticate()
        
    def _authenticate(self):
        """Authenticate dengan Google Drive API"""
        creds = None
        token_file = f"credentials/token_account_{self.account_index}.json"
        credentials_file = "credentials/google_credentials.json"
        
        # Load existing token
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, 
                ['https://www.googleapis.com/auth/drive.file'])
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                raise Exception(f"No valid credentials for account {self.account_index}")
            
            # Save the credentials for the next run
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('drive', 'v3', credentials=creds)
        self._ensure_backup_root_folder()
        
    def _ensure_backup_root_folder(self):
        """Pastikan root folder backup ada"""
        try:
            folder_name = "AutoBackup"
            
            # Cari folder yang sudah ada
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = self.service.files().list(q=query, fields='files(id, name)').execute()
            items = results.get('files', [])
            
            if items:
                self.backup_root_folder_id = items[0]['id']
                self.logger.info(f"Found existing backup root folder: {items[0]['name']}")
            else:
                # Buat folder baru
                folder_metadata = {
                    'name': folder_name,
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                folder = self.service.files().create(body=folder_metadata, fields='id').execute()
                self.backup_root_folder_id = folder.get('id')
                self.logger.info(f"Created new backup root folder with ID: {self.backup_root_folder_id}")
                
            # Cache root folder
            self.folder_cache[folder_name] = self.backup_root_folder_id
                
        except HttpError as error:
            self.logger.error(f"Error ensuring backup root folder: {error}")
            raise
            
    async def ensure_folder_structure(self, folder_path: str) -> str:
        """
        Pastikan struktur folder ada dan return folder ID
        folder_path format: "2024-08-20/Images" atau "2024-08-20/Documents"
        """
        try:
            # Split path menjadi components
            path_parts = folder_path.split('/')
            current_parent_id = self.backup_root_folder_id
            current_path = ""
            
            for part in path_parts:
                current_path = f"{current_path}/{part}" if current_path else part
                
                # Check cache first
                if current_path in self.folder_cache:
                    current_parent_id = self.folder_cache[current_path]
                    continue
                
                # Search for folder
                query = (f"name='{part}' and "
                        f"parents in '{current_parent_id}' and "
                        f"mimeType='application/vnd.google-apps.folder' and "
                        f"trashed=false")
                
                results = self.service.files().list(q=query, fields='files(id, name)').execute()
                items = results.get('files', [])
                
                if items:
                    # Folder exists
                    current_parent_id = items[0]['id']
                    self.logger.debug(f"Found existing folder: {part}")
                else:
                    # Create folder
                    folder_metadata = {
                        'name': part,
                        'mimeType': 'application/vnd.google-apps.folder',
                        'parents': [current_parent_id]
                    }
                    
                    folder = self.service.files().create(body=folder_metadata, fields='id').execute()
                    current_parent_id = folder.get('id')
                    self.logger.info(f"Created folder: {part}")
                
                # Cache folder ID
                self.folder_cache[current_path] = current_parent_id
            
            return current_parent_id
            
        except HttpError as error:
            self.logger.error(f"Error ensuring folder structure {folder_path}: {error}")
            return None
            
    async def upload_file_to_folder(self, file_path: str, folder_id: str, 
                                   remote_name: str = None) -> str:
        """Upload file ke folder tertentu"""
        try:
            if not remote_name:
                remote_name = Path(file_path).name
            
            # Check if file already exists in folder
            existing_file = await self._find_file_in_folder(remote_name, folder_id)
            
            file_metadata = {
                'name': remote_name,
                'parents': [folder_id]
            }
            
            # Determine media type
            file_size = os.path.getsize(file_path)
            resumable = file_size > 5 * 1024 * 1024  # Use resumable upload for files > 5MB
            
            media = MediaFileUpload(file_path, resumable=resumable)
            
            if existing_file:
                # Update existing file
                file = self.service.files().update(
                    fileId=existing_file['id'],
                    body=file_metadata,
                    media_body=media,
                    fields='id'
                ).execute()
                self.logger.info(f"Updated existing file: {remote_name}")
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
            return None
        except Exception as error:
            self.logger.error(f"Unexpected error uploading file {file_path}: {error}")
            return None
            
    async def _find_file_in_folder(self, filename: str, folder_id: str) -> dict:
        """Cari file berdasarkan nama dalam folder tertentu"""
        try:
            query = f"name='{filename}' and parents in '{folder_id}' and trashed=false"
            results = self.service.files().list(q=query, fields='files(id, name)').execute()
            items = results.get('files', [])
            return items[0] if items else None
            
        except HttpError as error:
            self.logger.error(f"Error finding file {filename}: {error}")
            return None
            
    def get_storage_usage(self) -> dict:
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
                'available_gb': available / (1024**3),
                'usage_percentage': (used / total * 100) if total > 0 else 0
            }
            
        except HttpError as error:
            self.logger.error(f"Error getting storage usage: {error}")
            return None
            
    def list_backup_folders(self) -> List[dict]:
        """List semua folder backup"""
        try:
            if not self.backup_root_folder_id:
                return []
                
            query = f"parents in '{self.backup_root_folder_id}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = self.service.files().list(
                q=query, 
                fields='files(id, name, createdTime, modifiedTime)',
                orderBy='createdTime desc'
            ).execute()
            
            return results.get('files', [])
            
        except HttpError as error:
            self.logger.error(f"Error listing backup folders: {error}")
            return []
            
    def download_file(self, file_id: str, local_path: str) -> bool:
        """Download file dari Google Drive"""
        try:
            request = self.service.files().get_media(fileId=file_id)
            file_io = io.BytesIO()
            downloader = MediaIoBaseDownload(file_io, request)
            
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                
            # Write to local file
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, 'wb') as f:
                f.write(file_io.getvalue())
                
            self.logger.info(f"Downloaded file to: {local_path}")
            return True
            
        except HttpError as error:
            self.logger.error(f"Error downloading file: {error}")
            return False
            
    def search_files(self, query: str, limit: int = 50) -> List[dict]:
        """Search files dalam backup folder"""
        try:
            if not self.backup_root_folder_id:
                return []
                
            # Search in backup folder and subfolders
            search_query = (f"parents in '{self.backup_root_folder_id}' and "
                          f"name contains '{query}' and "
                          f"trashed=false")
            
            results = self.service.files().list(
                q=search_query,
                fields='files(id, name, size, createdTime, parents)',
                pageSize=limit
            ).execute()
            
            return results.get('files', [])
            
        except HttpError as error:
            self.logger.error(f"Error searching files: {error}")
            return []
            
    def get_folder_contents(self, folder_id: str) -> List[dict]:
        """Get contents of a folder"""
        try:
            query = f"parents in '{folder_id}' and trashed=false"
            results = self.service.files().list(
                q=query,
                fields='files(id, name, size, mimeType, createdTime, modifiedTime)',
                orderBy='name'
            ).execute()
            
            return results.get('files', [])
            
        except HttpError as error:
            self.logger.error(f"Error getting folder contents: {error}")
            return []
