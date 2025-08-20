"""
File Recovery Manager untuk restore file dari Google Drive
"""

import os
import sqlite3
from pathlib import Path
from datetime import datetime
import logging
from typing import List, Dict, Optional
from src.google_drive_manager import GoogleDriveManager
from config.settings import DATABASE_CONFIG

class FileRecoveryManager:
    """Class untuk mengelola recovery/restore file dari backup"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db_path = DATABASE_CONFIG["db_file"]
        self.google_accounts: List[GoogleDriveManager] = []
        self._load_google_accounts()
        
    def _load_google_accounts(self):
        """Load semua akun Google yang tersedia"""
        try:
            account = GoogleDriveManager(account_index=0)
            self.google_accounts.append(account)
            self.logger.info(f"Loaded Google account 0 for recovery")
        except Exception as e:
            self.logger.error(f"Failed to load Google account 0: {e}")
            
    def search_backed_files(self, filename_pattern: str = None, 
                           date_from: datetime = None, 
                           date_to: datetime = None) -> List[Dict]:
        """Search file yang sudah di-backup"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM backed_files WHERE 1=1"
        params = []
        
        if filename_pattern:
            query += " AND file_path LIKE ?"
            params.append(f"%{filename_pattern}%")
            
        if date_from:
            query += " AND backup_date >= ?"
            params.append(date_from)
            
        if date_to:
            query += " AND backup_date <= ?"
            params.append(date_to)
            
        query += " ORDER BY backup_date DESC"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        
        files = []
        for result in results:
            files.append({
                'id': result[0],
                'file_path': result[1],
                'file_hash': result[2],
                'file_size': result[3],
                'backup_date': result[4],
                'google_account_index': result[5],
                'google_file_id': result[6]
            })
            
        return files
        
    def restore_file(self, backup_record: Dict, restore_path: str = None) -> bool:
        """Restore file dari Google Drive"""
        try:
            account_index = backup_record['google_account_index']
            google_file_id = backup_record['google_file_id']
            original_path = backup_record['file_path']
            
            if account_index >= len(self.google_accounts):
                self.logger.error(f"Google account {account_index} not available")
                return False
                
            account = self.google_accounts[account_index]
            
            # Tentukan path restore
            if restore_path is None:
                restore_path = original_path
                
            # Buat direktori jika belum ada
            os.makedirs(os.path.dirname(restore_path), exist_ok=True)
            
            # Download file
            success = account.download_file(google_file_id, restore_path)
            
            if success:
                self.logger.info(f"File restored to: {restore_path}")
                return True
            else:
                self.logger.error(f"Failed to restore file: {original_path}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error restoring file: {e}")
            return False
            
    def restore_multiple_files(self, backup_records: List[Dict], 
                              restore_base_path: str = None) -> Dict:
        """Restore multiple files"""
        successful = 0
        failed = 0
        
        for record in backup_records:
            try:
                if restore_base_path:
                    # Restore ke directory baru
                    original_path = Path(record['file_path'])
                    restore_path = Path(restore_base_path) / original_path.name
                else:
                    restore_path = record['file_path']
                    
                if self.restore_file(record, str(restore_path)):
                    successful += 1
                else:
                    failed += 1
                    
            except Exception as e:
                self.logger.error(f"Error restoring file {record['file_path']}: {e}")
                failed += 1
                
        summary = {
            'total_files': len(backup_records),
            'successful': successful,
            'failed': failed
        }
        
        self.logger.info(f"Restore completed: {summary}")
        return summary
        
    def list_available_files(self) -> List[Dict]:
        """List semua file yang tersedia untuk restore"""
        return self.search_backed_files()
        
    def get_file_versions(self, original_path: str) -> List[Dict]:
        """Dapatkan semua versi backup dari file tertentu"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM backed_files 
            WHERE file_path = ? 
            ORDER BY backup_date DESC
        ''', (original_path,))
        
        results = cursor.fetchall()
        conn.close()
        
        versions = []
        for result in results:
            versions.append({
                'id': result[0],
                'file_path': result[1],
                'file_hash': result[2],
                'file_size': result[3],
                'backup_date': result[4],
                'google_account_index': result[5],
                'google_file_id': result[6]
            })
            
        return versions
