"""
Enhanced Backup Manager dengan fitur lengkap:
- Auto-retry saat gagal
- Organisasi folder berdasarkan tanggal dan jenis file
- Auto-delete setelah upload berhasil
- Progress reporting
"""

import os
import shutil
import sqlite3
import hashlib
import time
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

from src.enhanced_google_drive_manager import EnhancedGoogleDriveManager
from src.utils.network_manager import NetworkManager
from src.utils.folder_manager import FolderManager  
from src.utils.enhanced_settings import EnhancedSettings
from src.utils.file_organizer import FileOrganizer

class EnhancedBackupManager:
    """Enhanced Backup Manager dengan fitur lengkap"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.settings = EnhancedSettings()
        self.network_manager = NetworkManager()
        self.folder_manager = FolderManager()
        self.file_organizer = FileOrganizer()
        
        self.google_accounts: List[EnhancedGoogleDriveManager] = []
        self.db_path = self.settings.get('database_path', 'config/backup_tracking.db')
        
        self._init_database()
        self._load_google_accounts()
        
    def _init_database(self):
        """Initialize database dengan schema enhanced"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Enhanced backup files table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS backed_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT UNIQUE,
                original_path TEXT,
                file_hash TEXT,
                file_size INTEGER,
                file_type TEXT,
                backup_date TIMESTAMP,
                google_account_index INTEGER,
                google_file_id TEXT,
                google_folder_id TEXT,
                upload_status TEXT DEFAULT 'completed',
                deleted_from_local BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Enhanced backup logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS backup_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                backup_date TIMESTAMP,
                total_files INTEGER,
                successful_files INTEGER,
                failed_files INTEGER,
                uploaded_files INTEGER,
                deleted_files INTEGER,
                folders_created INTEGER,
                total_size_mb REAL,
                duration_seconds INTEGER,
                retry_attempts INTEGER DEFAULT 0,
                network_issues INTEGER DEFAULT 0,
                status TEXT DEFAULT 'completed'
            )
        ''')
        
        # Backup queue for retry mechanism
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS backup_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT,
                retry_count INTEGER DEFAULT 0,
                last_attempt TIMESTAMP,
                error_message TEXT,
                priority INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Daily backup status
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_status (
                date DATE PRIMARY KEY,
                backup_completed BOOLEAN DEFAULT 0,
                files_backed INTEGER DEFAULT 0,
                size_backed_mb REAL DEFAULT 0,
                issues_encountered TEXT,
                next_retry_time TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def _load_google_accounts(self):
        """Load semua akun Google Drive"""
        accounts_config = self.settings.get('google_accounts', [])
        
        for account_info in accounts_config:
            try:
                account = EnhancedGoogleDriveManager(
                    account_index=account_info['index'],
                    account_name=account_info.get('name', f"Account {account_info['index']}")
                )
                self.google_accounts.append(account)
                self.logger.info(f"Loaded Google account: {account.account_name}")
            except Exception as e:
                self.logger.error(f"Failed to load account {account_info}: {e}")
                
    async def run_backup_with_progress(self, progress_callback=None) -> Dict:
        """Jalankan backup dengan progress reporting"""
        start_time = datetime.now()
        today = start_time.date()
        
        # Check if backup already completed today
        if self._is_backup_completed_today():
            return {
                'status': 'already_completed',
                'message': 'Backup already completed today',
                'total_files': 0,
                'successful_files': 0,
                'failed_files': 0,
                'uploaded_files': 0,
                'deleted_files': 0,
                'folders_created': 0,
                'total_size_mb': 0,
                'duration_seconds': 0
            }
        
        self.logger.info("Starting enhanced backup process...")
        
        # Check network connectivity
        if not self.network_manager.check_network()['connected']:
            self._schedule_retry()
            return {
                'status': 'network_error',
                'message': 'No network connection. Backup scheduled for retry.',
                'total_files': 0,
                'successful_files': 0,
                'failed_files': 0,
                'uploaded_files': 0,
                'deleted_files': 0,
                'folders_created': 0,
                'total_size_mb': 0,
                'duration_seconds': 0
            }
        
        # Get files to backup
        files_to_backup = self._get_files_to_backup()
        total_files = len(files_to_backup)
        
        if progress_callback:
            await progress_callback(f"Found {total_files} files to backup")
        
        if total_files == 0:
            self._mark_backup_completed(today, 0, 0)
            return {
                'status': 'no_files',
                'message': 'No files to backup',
                'total_files': 0,
                'successful_files': 0,
                'failed_files': 0,
                'uploaded_files': 0,
                'deleted_files': 0,
                'folders_created': 0,
                'total_size_mb': 0,
                'duration_seconds': 0
            }
        
        # Initialize counters
        successful_files = 0
        failed_files = 0
        uploaded_files = 0
        deleted_files = 0
        folders_created = 0
        total_size = 0
        retry_attempts = 0
        network_issues = 0
        
        # Create date-based folder for today
        date_folder_name = start_time.strftime("%Y-%m-%d")
        
        if progress_callback:
            await progress_callback(f"Creating folder: {date_folder_name}")
        
        # Process files
        for i, file_path in enumerate(files_to_backup):
            try:
                if progress_callback:
                    progress = (i + 1) / total_files * 100
                    await progress_callback(f"Processing file {i+1}/{total_files} ({progress:.1f}%)")
                
                file_size = file_path.stat().st_size
                total_size += file_size
                
                # Attempt to backup file with retry
                backup_result = await self._backup_file_with_retry(
                    file_path, date_folder_name, progress_callback
                )
                
                if backup_result['success']:
                    successful_files += 1
                    if backup_result['uploaded']:
                        uploaded_files += 1
                    if backup_result['deleted']:
                        deleted_files += 1
                    if backup_result['folder_created']:
                        folders_created += 1
                else:
                    failed_files += 1
                    if 'network' in backup_result.get('error', '').lower():
                        network_issues += 1
                    
                    # Add to retry queue
                    self._add_to_retry_queue(str(file_path), backup_result.get('error', 'Unknown error'))
                    
            except Exception as e:
                self.logger.error(f"Error processing {file_path}: {e}")
                failed_files += 1
                self._add_to_retry_queue(str(file_path), str(e))
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        total_size_mb = total_size / (1024 * 1024)
        
        # Log backup summary
        self._log_backup_summary(
            total_files, successful_files, failed_files, uploaded_files,
            deleted_files, folders_created, total_size_mb, duration,
            retry_attempts, network_issues
        )
        
        # Mark daily backup status
        self._mark_backup_completed(today, successful_files, total_size_mb)
        
        summary = {
            'status': 'completed',
            'total_files': total_files,
            'successful_files': successful_files,
            'failed_files': failed_files,
            'uploaded_files': uploaded_files,
            'deleted_files': deleted_files,
            'folders_created': folders_created,
            'total_size_mb': total_size_mb,
            'duration_seconds': duration,
            'retry_attempts': retry_attempts,
            'network_issues': network_issues
        }
        
        self.logger.info(f"Backup completed: {summary}")
        return summary
        
    async def _backup_file_with_retry(self, file_path: Path, date_folder: str, 
                                    progress_callback=None) -> Dict:
        """Backup file dengan retry mechanism"""
        max_retries = self.settings.get('max_retry_attempts', 3)
        retry_delay = self.settings.get('retry_delay_minutes', 5) * 60
        
        for attempt in range(max_retries + 1):
            try:
                if attempt > 0:
                    if progress_callback:
                        await progress_callback(f"Retry attempt {attempt} for {file_path.name}")
                    
                    # Wait before retry
                    await asyncio.sleep(retry_delay)
                    
                    # Check network again
                    if not self.network_manager.check_network()['connected']:
                        return {
                            'success': False,
                            'error': 'Network connection lost',
                            'uploaded': False,
                            'deleted': False,
                            'folder_created': False
                        }
                
                # Get best available account
                account = self._get_best_account()
                if not account:
                    return {
                        'success': False,
                        'error': 'No available Google accounts',
                        'uploaded': False,
                        'deleted': False,
                        'folder_created': False
                    }
                
                # Organize file by type
                file_type = self.file_organizer.get_file_type(file_path)
                
                # Create folder structure: Date/FileType/
                folder_path = f"{date_folder}/{file_type}"
                folder_id = await account.ensure_folder_structure(folder_path)
                
                if not folder_id:
                    return {
                        'success': False,
                        'error': 'Failed to create folder structure',
                        'uploaded': False,
                        'deleted': False,
                        'folder_created': False
                    }
                
                # Upload file
                google_file_id = await account.upload_file_to_folder(
                    str(file_path), folder_id, file_path.name
                )
                
                if google_file_id:
                    # Record successful backup
                    self._record_backup(
                        str(file_path), file_path, account.account_index,
                        google_file_id, folder_id, file_type
                    )
                    
                    # Delete original file if setting enabled
                    deleted = False
                    if self.settings.get('auto_delete_after_upload', True):
                        try:
                            file_path.unlink()
                            deleted = True
                            self.logger.info(f"Deleted original file: {file_path}")
                        except Exception as e:
                            self.logger.warning(f"Failed to delete {file_path}: {e}")
                    
                    return {
                        'success': True,
                        'uploaded': True,
                        'deleted': deleted,
                        'folder_created': True,
                        'account': account.account_name,
                        'folder': folder_path
                    }
                else:
                    if attempt == max_retries:
                        return {
                            'success': False,
                            'error': f'Upload failed after {max_retries + 1} attempts',
                            'uploaded': False,
                            'deleted': False,
                            'folder_created': False
                        }
                        
            except Exception as e:
                self.logger.error(f"Backup attempt {attempt + 1} failed for {file_path}: {e}")
                if attempt == max_retries:
                    return {
                        'success': False,
                        'error': str(e),
                        'uploaded': False,
                        'deleted': False,
                        'folder_created': False
                    }
        
        return {
            'success': False,
            'error': 'Max retries exceeded',
            'uploaded': False,
            'deleted': False,
            'folder_created': False
        }
        
    def _get_files_to_backup(self) -> List[Path]:
        """Get files yang perlu di-backup"""
        files_to_backup = []
        source_folders = self.settings.get('source_folders', [])
        allowed_extensions = self.settings.get('allowed_extensions', [])
        max_file_size = self.settings.get('max_file_size_mb', 100) * 1024 * 1024
        
        for folder_path in source_folders:
            folder = Path(folder_path)
            if not folder.exists():
                continue
                
            for file_path in folder.rglob("*"):
                if file_path.is_file():
                    # Check extension
                    if file_path.suffix.lower() not in allowed_extensions:
                        continue
                    
                    # Check size
                    if file_path.stat().st_size > max_file_size:
                        continue
                    
                    # Check if already backed up
                    if not self._should_backup_file(file_path):
                        continue
                    
                    files_to_backup.append(file_path)
        
        return files_to_backup
        
    def _should_backup_file(self, file_path: Path) -> bool:
        """Check apakah file perlu di-backup"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if file already backed up
        cursor.execute(
            "SELECT file_hash, upload_status FROM backed_files WHERE file_path = ?",
            (str(file_path),)
        )
        result = cursor.fetchone()
        
        if result:
            # File exists in DB, check if hash changed
            old_hash, status = result
            current_hash = self._calculate_file_hash(file_path)
            
            if old_hash == current_hash and status == 'completed':
                conn.close()
                return False  # File unchanged and already backed up
        
        conn.close()
        return True
        
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return ""
            
    def _get_best_account(self) -> Optional[EnhancedGoogleDriveManager]:
        """Get akun dengan storage terbanyak"""
        best_account = None
        max_available = 0
        
        for account in self.google_accounts:
            try:
                storage_info = account.get_storage_usage()
                if storage_info and storage_info['available_gb'] > max_available:
                    max_available = storage_info['available_gb']
                    best_account = account
            except Exception as e:
                self.logger.error(f"Error checking storage for {account.account_name}: {e}")
        
        return best_account
        
    def _record_backup(self, file_path: str, original_path: Path, account_index: int,
                      google_file_id: str, folder_id: str, file_type: str):
        """Record backup success to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        file_hash = self._calculate_file_hash(original_path)
        file_size = original_path.stat().st_size
        
        cursor.execute('''
            INSERT OR REPLACE INTO backed_files 
            (file_path, original_path, file_hash, file_size, file_type, backup_date, 
             google_account_index, google_file_id, google_folder_id, upload_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            file_path, str(original_path), file_hash, file_size, file_type,
            datetime.now(), account_index, google_file_id, folder_id, 'completed'
        ))
        
        conn.commit()
        conn.close()
        
    def _is_backup_completed_today(self) -> bool:
        """Check apakah backup hari ini sudah selesai"""
        today = datetime.now().date()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT backup_completed FROM daily_status WHERE date = ?",
            (today,)
        )
        result = cursor.fetchone()
        conn.close()
        
        return result and result[0]
        
    def _mark_backup_completed(self, date, files_count: int, size_mb: float):
        """Mark backup as completed for the day"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO daily_status 
            (date, backup_completed, files_backed, size_backed_mb)
            VALUES (?, ?, ?, ?)
        ''', (date, True, files_count, size_mb))
        
        conn.commit()
        conn.close()
        
    def _schedule_retry(self):
        """Schedule backup retry untuk besok"""
        tomorrow = datetime.now() + timedelta(days=1)
        retry_time = tomorrow.replace(
            hour=int(self.settings.get('backup_time', '00:00').split(':')[0]),
            minute=int(self.settings.get('backup_time', '00:00').split(':')[1]),
            second=0,
            microsecond=0
        )
        
        today = datetime.now().date()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO daily_status 
            (date, backup_completed, issues_encountered, next_retry_time)
            VALUES (?, ?, ?, ?)
        ''', (today, False, "Network connection failed", retry_time))
        
        conn.commit()
        conn.close()
        
        self.logger.info(f"Backup rescheduled for {retry_time}")
        
    def _add_to_retry_queue(self, file_path: str, error_message: str):
        """Add file to retry queue"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO backup_queue 
            (file_path, retry_count, last_attempt, error_message)
            VALUES (?, 0, ?, ?)
        ''', (file_path, datetime.now(), error_message))
        
        conn.commit()
        conn.close()
        
    def _log_backup_summary(self, total_files: int, successful_files: int, 
                           failed_files: int, uploaded_files: int, deleted_files: int,
                           folders_created: int, total_size_mb: float, duration: float,
                           retry_attempts: int, network_issues: int):
        """Log backup summary to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO backup_logs 
            (backup_date, total_files, successful_files, failed_files, uploaded_files,
             deleted_files, folders_created, total_size_mb, duration_seconds, 
             retry_attempts, network_issues)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now(), total_files, successful_files, failed_files,
            uploaded_files, deleted_files, folders_created, total_size_mb,
            duration, retry_attempts, network_issues
        ))
        
        conn.commit()
        conn.close()
        
    def get_backup_history(self, limit: int = 20) -> List[Dict]:
        """Get backup history"""
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
                'uploaded_files': result[5],
                'deleted_files': result[6],
                'folders_created': result[7],
                'total_size_mb': result[8],
                'duration_seconds': result[9],
                'retry_attempts': result[10],
                'network_issues': result[11]
            })
        
        return history
        
    def get_today_status(self) -> Dict:
        """Get status backup hari ini"""
        today = datetime.now().date()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM daily_status WHERE date = ?",
            (today,)
        )
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'date': result[0],
                'backup_completed': bool(result[1]),
                'files_backed': result[2],
                'size_backed_mb': result[3],
                'issues_encountered': result[4],
                'next_retry_time': result[5]
            }
        else:
            return {
                'date': str(today),
                'backup_completed': False,
                'files_backed': 0,
                'size_backed_mb': 0,
                'issues_encountered': None,
                'next_retry_time': None
            }
