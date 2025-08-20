"""
Advanced Backup System - Source Package

Sistem backup canggih untuk Android/Termux dengan kontrol Telegram Bot
"""

__version__ = "1.0.0"
__author__ = "Backup System Team" 
__description__ = "Advanced backup system with Telegram bot control for Android/Termux"

# Import main modules
from .main import BackupSystemManager
from .advanced_telegram_bot import AdvancedTelegramBot
from .enhanced_backup_manager import EnhancedBackupManager
from .enhanced_google_drive_manager import EnhancedGoogleDriveManager
from .database_manager import DatabaseManager

__all__ = [
    'BackupSystemManager',
    'AdvancedTelegramBot',
    'EnhancedBackupManager',
    'EnhancedGoogleDriveManager', 
    'DatabaseManager'
]
