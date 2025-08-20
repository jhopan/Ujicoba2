"""
Scheduler untuk menjalankan backup otomatis
"""

import time
import threading
from datetime import datetime, time as dt_time
import logging
from src.backup_manager import BackupManager
from config.settings import BACKUP_CONFIG

class BackupScheduler:
    """Class untuk menjadwalkan backup otomatis"""
    
    def __init__(self, backup_manager: BackupManager):
        self.backup_manager = backup_manager
        self.logger = logging.getLogger(__name__)
        self.running = False
        self.scheduler_thread = None
        
        # Parse backup time
        backup_time_str = BACKUP_CONFIG["backup_time"]
        hour, minute = map(int, backup_time_str.split(":"))
        self.backup_time = dt_time(hour, minute)
        
    def start(self):
        """Start scheduler"""
        if self.running:
            self.logger.warning("Scheduler is already running")
            return
            
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        self.logger.info(f"Backup scheduler started. Will backup daily at {self.backup_time}")
        
    def stop(self):
        """Stop scheduler"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()
        self.logger.info("Backup scheduler stopped")
        
    def _scheduler_loop(self):
        """Main scheduler loop"""
        last_backup_date = None
        
        while self.running:
            try:
                current_time = datetime.now()
                current_date = current_time.date()
                current_time_only = current_time.time()
                
                # Check if it's time to backup and we haven't backed up today
                if (current_time_only >= self.backup_time and 
                    last_backup_date != current_date):
                    
                    self.logger.info("Starting scheduled backup...")
                    try:
                        summary = self.backup_manager.run_backup()
                        self.logger.info(f"Scheduled backup completed: {summary}")
                        last_backup_date = current_date
                    except Exception as e:
                        self.logger.error(f"Error during scheduled backup: {e}")
                        
                # Sleep for 60 seconds before next check
                time.sleep(60)
                
            except Exception as e:
                self.logger.error(f"Error in scheduler loop: {e}")
                time.sleep(60)
                
    def force_backup(self):
        """Force backup sekarang juga"""
        self.logger.info("Forcing immediate backup...")
        try:
            summary = self.backup_manager.run_backup()
            self.logger.info(f"Forced backup completed: {summary}")
            return summary
        except Exception as e:
            self.logger.error(f"Error during forced backup: {e}")
            return None
