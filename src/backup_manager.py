"""
Backup Manager untuk mengkoordinasi proses backup
"""

import os
import shutil
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime
import logging
from typing import List, Dict, Optional
from src.google_drive_manager import GoogleDriveManager
from config.settings import BACKUP_CONFIG, DATABASE_CONFIG

class BackupManager:
    """Class utama untuk mengelola proses backup"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.google_accounts: List[GoogleDriveManager] = []
        self.current_account_index = 0
        self.db_path = DATABASE_CONFIG["db_file"]
        self._init_database()
        self._load_google_accounts()
        
    def _init_database(self):
        """Initialize database untuk tracking backup"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS backed_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT UNIQUE,
                file_hash TEXT,
                file_size INTEGER,
                backup_date TIMESTAMP,
                google_account_index INTEGER,
                google_file_id TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS backup_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                backup_date TIMESTAMP,
                total_files INTEGER,
                successful_files INTEGER,
                failed_files INTEGER,
                total_size_mb REAL,
                duration_seconds INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def _load_google_accounts(self):
        """Load semua akun Google yang tersedia"""
        # Dalam implementasi sebenarnya, Anda bisa menambahkan multiple accounts
        # Untuk contoh ini, kita mulai dengan 1 account
        try:
            account = GoogleDriveManager(account_index=0)
            self.google_accounts.append(account)
            self.logger.info(f"Loaded Google account 0")
        except Exception as e:
            self.logger.error(f"Failed to load Google account 0: {e}")
            
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate MD5 hash dari file"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            self.logger.error(f"Error calculating hash for {file_path}: {e}")
            return ""
            
    def _is_file_backed_up(self, file_path: str) -> Optional[Dict]:
        """Check apakah file sudah di-backup"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM backed_files WHERE file_path = ?",
            (file_path,)
        )
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'file_path': result[1],
                'file_hash': result[2],
                'file_size': result[3],
                'backup_date': result[4],
                'google_account_index': result[5],
                'google_file_id': result[6]
            }
        return None
        
    def _record_backup(self, file_path: str, file_hash: str, file_size: int, 
                      account_index: int, google_file_id: str):
        """Record backup ke database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO backed_files 
            (file_path, file_hash, file_size, backup_date, google_account_index, google_file_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (file_path, file_hash, file_size, datetime.now(), account_index, google_file_id))
        
        conn.commit()
        conn.close()
        
    def _should_backup_file(self, file_path: Path) -> bool:
        """Check apakah file harus di-backup"""
        # Check extension
        if file_path.suffix.lower() not in BACKUP_CONFIG["allowed_extensions"]:
            return False
            
        # Check file size
        try:
            file_size_mb = file_path.stat().st_size / (1024 * 1024)
            if file_size_mb > BACKUP_CONFIG["max_file_size_mb"]:
                return False
        except OSError:
            return False
            
        # Check if file already backed up and hasn't changed
        backup_record = self._is_file_backed_up(str(file_path))
        if backup_record:
            current_hash = self._calculate_file_hash(str(file_path))
            if current_hash == backup_record['file_hash']:
                return False  # File hasn't changed
                
        return True
        
    def _get_files_to_backup(self) -> List[Path]:
        """Dapatkan list file yang perlu di-backup"""
        files_to_backup = []
        
        for source_folder in BACKUP_CONFIG["source_folders"]:
            source_path = Path(source_folder)
            
            if not source_path.exists():
                self.logger.warning(f"Source folder does not exist: {source_folder}")
                continue
                
            for file_path in source_path.rglob("*"):
                if file_path.is_file():
                    # Skip ignored folders
                    if any(ignore in str(file_path) for ignore in BACKUP_CONFIG["ignore_folders"]):
                        continue
                        
                    if self._should_backup_file(file_path):
                        files_to_backup.append(file_path)
                        
        return files_to_backup
        
    def _get_best_account(self) -> Optional[GoogleDriveManager]:
        """Dapatkan akun Google dengan storage paling banyak"""
        best_account = None
        max_available = 0
        
        for account in self.google_accounts:
            try:
                storage_info = account.get_storage_usage()
                if storage_info and storage_info['available_gb'] > max_available:
                    max_available = storage_info['available_gb']
                    best_account = account
            except Exception as e:
                self.logger.error(f"Error checking storage for account {account.account_index}: {e}")
                
        return best_account
        
    def backup_file(self, file_path: Path) -> bool:
        """Backup single file"""
        try:
            account = self._get_best_account()
            if not account:
                self.logger.error("No available Google account for backup")
                return False
                
            # Generate remote filename dengan timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            remote_name = f"{timestamp}_{file_path.name}"
            
            # Upload file
            google_file_id = account.upload_file(str(file_path), remote_name)
            
            if google_file_id:
                # Record backup
                file_hash = self._calculate_file_hash(str(file_path))
                file_size = file_path.stat().st_size
                self._record_backup(
                    str(file_path), file_hash, file_size, 
                    account.account_index, google_file_id
                )
                self.logger.info(f"Successfully backed up: {file_path}")
                return True
            else:
                self.logger.error(f"Failed to backup: {file_path}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error backing up {file_path}: {e}")
            return False
            
    def run_backup(self) -> Dict:
        """Jalankan proses backup lengkap"""
        start_time = datetime.now()
        self.logger.info("Starting backup process...")
        
        files_to_backup = self._get_files_to_backup()
        total_files = len(files_to_backup)
        successful_files = 0
        failed_files = 0
        total_size = 0
        
        self.logger.info(f"Found {total_files} files to backup")
        
        for file_path in files_to_backup:
            try:
                file_size = file_path.stat().st_size
                total_size += file_size
                
                if self.backup_file(file_path):
                    successful_files += 1
                else:
                    failed_files += 1
                    
            except Exception as e:
                self.logger.error(f"Error processing {file_path}: {e}")
                failed_files += 1
                
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        total_size_mb = total_size / (1024 * 1024)
        
        # Log backup summary
        self._log_backup_summary(
            total_files, successful_files, failed_files, 
            total_size_mb, duration
        )
        
        summary = {
            'total_files': total_files,
            'successful_files': successful_files,
            'failed_files': failed_files,
            'total_size_mb': total_size_mb,
            'duration_seconds': duration
        }
        
        self.logger.info(f"Backup completed: {summary}")
        return summary
        
    def _log_backup_summary(self, total_files: int, successful_files: int, 
                           failed_files: int, total_size_mb: float, duration: float):
        """Log backup summary ke database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO backup_logs 
            (backup_date, total_files, successful_files, failed_files, total_size_mb, duration_seconds)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (datetime.now(), total_files, successful_files, failed_files, total_size_mb, duration))
        
        conn.commit()
        conn.close()
        
    def get_backup_history(self, limit: int = 10) -> List[Dict]:
        """Dapatkan history backup"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM backup_logs 
            ORDER BY backup_date DESC 
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        history = []
        for result in results:
            history.append({
                'id': result[0],
                'backup_date': result[1],
                'total_files': result[2],
                'successful_files': result[3],
                'failed_files': result[4],
                'total_size_mb': result[5],
                'duration_seconds': result[6]
            })
            
        return history
