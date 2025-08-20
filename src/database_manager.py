"""
Database Manager for backup system data persistence
"""

import sqlite3
import json
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path: str = "backup_system.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Backup logs table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS backup_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        file_path TEXT NOT NULL,
                        file_size INTEGER,
                        account_name TEXT,
                        drive_file_id TEXT,
                        status TEXT NOT NULL,
                        error_message TEXT,
                        retry_count INTEGER DEFAULT 0,
                        upload_duration REAL,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Backup sessions table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS backup_sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT UNIQUE NOT NULL,
                        start_time TEXT NOT NULL,
                        end_time TEXT,
                        status TEXT NOT NULL,
                        total_files INTEGER DEFAULT 0,
                        successful_files INTEGER DEFAULT 0,
                        failed_files INTEGER DEFAULT 0,
                        total_size INTEGER DEFAULT 0,
                        error_message TEXT,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # File queue table for pending uploads
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS file_queue (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        file_path TEXT NOT NULL,
                        file_size INTEGER,
                        priority INTEGER DEFAULT 0,
                        retry_count INTEGER DEFAULT 0,
                        last_attempt TEXT,
                        error_message TEXT,
                        status TEXT DEFAULT 'pending',
                        session_id TEXT,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Account statistics table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS account_stats (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        account_name TEXT NOT NULL,
                        total_files INTEGER DEFAULT 0,
                        total_size INTEGER DEFAULT 0,
                        last_upload TEXT,
                        storage_used INTEGER DEFAULT 0,
                        upload_count_today INTEGER DEFAULT 0,
                        last_updated TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # System events table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS system_events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        event_type TEXT NOT NULL,
                        event_data TEXT,
                        severity TEXT DEFAULT 'info',
                        timestamp TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def log_backup_file(self, file_path: str, file_size: int, account_name: str,
                       status: str, drive_file_id: str = None, error_message: str = None,
                       retry_count: int = 0, upload_duration: float = None) -> int:
        """
        Log a backup file operation
        
        Returns:
            int: Log entry ID
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO backup_logs 
                    (timestamp, file_path, file_size, account_name, drive_file_id, 
                     status, error_message, retry_count, upload_duration)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    datetime.now().isoformat(),
                    file_path,
                    file_size,
                    account_name,
                    drive_file_id,
                    status,
                    error_message,
                    retry_count,
                    upload_duration
                ))
                
                log_id = cursor.lastrowid
                conn.commit()
                return log_id
                
        except Exception as e:
            logger.error(f"Failed to log backup file: {e}")
            return 0
    
    def create_backup_session(self, session_id: str) -> bool:
        """Create a new backup session"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO backup_sessions (session_id, start_time, status)
                    VALUES (?, ?, ?)
                ''', (session_id, datetime.now().isoformat(), 'running'))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Failed to create backup session: {e}")
            return False
    
    def update_backup_session(self, session_id: str, **kwargs) -> bool:
        """Update backup session with new data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Build dynamic update query
                update_fields = []
                values = []
                
                for field, value in kwargs.items():
                    if field in ['end_time', 'status', 'total_files', 'successful_files',
                               'failed_files', 'total_size', 'error_message']:
                        update_fields.append(f"{field} = ?")
                        values.append(value)
                
                if update_fields:
                    values.append(session_id)
                    query = f"UPDATE backup_sessions SET {', '.join(update_fields)} WHERE session_id = ?"
                    
                    cursor.execute(query, values)
                    conn.commit()
                    return True
                
        except Exception as e:
            logger.error(f"Failed to update backup session: {e}")
            return False
    
    def add_file_to_queue(self, file_path: str, file_size: int, priority: int = 0,
                         session_id: str = None) -> bool:
        """Add file to upload queue"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO file_queue 
                    (file_path, file_size, priority, session_id)
                    VALUES (?, ?, ?, ?)
                ''', (file_path, file_size, priority, session_id))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Failed to add file to queue: {e}")
            return False
    
    def get_pending_files(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get pending files from queue"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT id, file_path, file_size, priority, retry_count, 
                           last_attempt, error_message, session_id
                    FROM file_queue 
                    WHERE status = 'pending'
                    ORDER BY priority DESC, created_at ASC
                    LIMIT ?
                ''', (limit,))
                
                columns = [description[0] for description in cursor.description]
                files = []
                
                for row in cursor.fetchall():
                    file_data = dict(zip(columns, row))
                    files.append(file_data)
                
                return files
                
        except Exception as e:
            logger.error(f"Failed to get pending files: {e}")
            return []
    
    def update_file_queue_status(self, file_id: int, status: str, 
                                error_message: str = None) -> bool:
        """Update file queue status"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    UPDATE file_queue 
                    SET status = ?, error_message = ?, last_attempt = ?
                    WHERE id = ?
                ''', (status, error_message, datetime.now().isoformat(), file_id))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Failed to update file queue status: {e}")
            return False
    
    def increment_retry_count(self, file_id: int) -> bool:
        """Increment retry count for a file"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    UPDATE file_queue 
                    SET retry_count = retry_count + 1, last_attempt = ?
                    WHERE id = ?
                ''', (datetime.now().isoformat(), file_id))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Failed to increment retry count: {e}")
            return False
    
    def get_backup_statistics(self, days: int = 30) -> Dict[str, Any]:
        """Get backup statistics for the last N days"""
        try:
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total files and success rate
                cursor.execute('''
                    SELECT 
                        COUNT(*) as total_files,
                        SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as successful_files,
                        SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed_files,
                        SUM(file_size) as total_size,
                        AVG(upload_duration) as avg_upload_time
                    FROM backup_logs 
                    WHERE timestamp >= ?
                ''', (cutoff_date,))
                
                stats = cursor.fetchone()
                
                # Daily breakdown
                cursor.execute('''
                    SELECT 
                        DATE(timestamp) as date,
                        COUNT(*) as files_count,
                        SUM(file_size) as daily_size
                    FROM backup_logs 
                    WHERE timestamp >= ?
                    GROUP BY DATE(timestamp)
                    ORDER BY date DESC
                ''', (cutoff_date,))
                
                daily_stats = cursor.fetchall()
                
                # Account breakdown
                cursor.execute('''
                    SELECT 
                        account_name,
                        COUNT(*) as files_count,
                        SUM(file_size) as total_size
                    FROM backup_logs 
                    WHERE timestamp >= ? AND status = 'success'
                    GROUP BY account_name
                ''', (cutoff_date,))
                
                account_stats = cursor.fetchall()
                
                return {
                    'period_days': days,
                    'total_files': stats[0] or 0,
                    'successful_files': stats[1] or 0,
                    'failed_files': stats[2] or 0,
                    'total_size': stats[3] or 0,
                    'success_rate': (stats[1] / stats[0] * 100) if stats[0] > 0 else 0,
                    'average_upload_time': stats[4] or 0,
                    'daily_breakdown': [
                        {'date': row[0], 'files': row[1], 'size': row[2]}
                        for row in daily_stats
                    ],
                    'account_breakdown': [
                        {'account': row[0], 'files': row[1], 'size': row[2]}
                        for row in account_stats
                    ]
                }
                
        except Exception as e:
            logger.error(f"Failed to get backup statistics: {e}")
            return {}
    
    def log_system_event(self, event_type: str, event_data: Dict[str, Any], 
                        severity: str = 'info') -> bool:
        """Log a system event"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO system_events (event_type, event_data, severity)
                    VALUES (?, ?, ?)
                ''', (event_type, json.dumps(event_data), severity))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Failed to log system event: {e}")
            return False
    
    def get_recent_events(self, limit: int = 50, 
                         event_type: str = None) -> List[Dict[str, Any]]:
        """Get recent system events"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if event_type:
                    cursor.execute('''
                        SELECT event_type, event_data, severity, timestamp
                        FROM system_events 
                        WHERE event_type = ?
                        ORDER BY timestamp DESC
                        LIMIT ?
                    ''', (event_type, limit))
                else:
                    cursor.execute('''
                        SELECT event_type, event_data, severity, timestamp
                        FROM system_events 
                        ORDER BY timestamp DESC
                        LIMIT ?
                    ''', (limit,))
                
                events = []
                for row in cursor.fetchall():
                    event_data = json.loads(row[1]) if row[1] else {}
                    events.append({
                        'type': row[0],
                        'data': event_data,
                        'severity': row[2],
                        'timestamp': row[3]
                    })
                
                return events
                
        except Exception as e:
            logger.error(f"Failed to get recent events: {e}")
            return []
    
    def cleanup_old_logs(self, days_to_keep: int = 90) -> int:
        """Clean up old log entries"""
        try:
            cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Count records to be deleted
                cursor.execute('''
                    SELECT COUNT(*) FROM backup_logs WHERE timestamp < ?
                ''', (cutoff_date,))
                count = cursor.fetchone()[0]
                
                # Delete old records
                cursor.execute('''
                    DELETE FROM backup_logs WHERE timestamp < ?
                ''', (cutoff_date,))
                
                cursor.execute('''
                    DELETE FROM system_events WHERE timestamp < ?
                ''', (cutoff_date,))
                
                conn.commit()
                logger.info(f"Cleaned up {count} old log entries")
                return count
                
        except Exception as e:
            logger.error(f"Failed to cleanup old logs: {e}")
            return 0
    
    def get_failed_files_for_retry(self, max_retries: int = 3) -> List[Dict[str, Any]]:
        """Get failed files that can be retried"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT id, file_path, file_size, retry_count, error_message
                    FROM file_queue 
                    WHERE status = 'failed' AND retry_count < ?
                    ORDER BY priority DESC, created_at ASC
                ''', (max_retries,))
                
                columns = [description[0] for description in cursor.description]
                files = []
                
                for row in cursor.fetchall():
                    file_data = dict(zip(columns, row))
                    files.append(file_data)
                
                return files
                
        except Exception as e:
            logger.error(f"Failed to get files for retry: {e}")
            return []
    
    def export_logs_to_csv(self, output_path: Path, days: int = 30) -> bool:
        """Export logs to CSV file"""
        try:
            import csv
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT timestamp, file_path, file_size, account_name, 
                           status, error_message, retry_count, upload_duration
                    FROM backup_logs 
                    WHERE timestamp >= ?
                    ORDER BY timestamp DESC
                ''', (cutoff_date,))
                
                with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Write header
                    writer.writerow(['Timestamp', 'File Path', 'File Size', 'Account', 
                                   'Status', 'Error Message', 'Retry Count', 'Upload Duration'])
                    
                    # Write data
                    writer.writerows(cursor.fetchall())
                
                logger.info(f"Logs exported to: {output_path}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to export logs: {e}")
            return False
