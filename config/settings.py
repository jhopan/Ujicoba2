"""
⚙️ Settings Configuration
Configuration constants untuk Google Drive dan backup system
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
CREDENTIALS_DIR = PROJECT_ROOT / "credentials"

# Google Drive Configuration
GOOGLE_DRIVE_CONFIG = {
    "credentials_file": str(CREDENTIALS_DIR / "google_credentials.json"),
    "scopes": ['https://www.googleapis.com/auth/drive.file'],
    "upload_chunk_size": 8 * 1024 * 1024,  # 8MB chunks
    "max_retries": 3,
    "timeout": 300  # 5 minutes
}

# Backup Configuration
BACKUP_CONFIG = {
    "max_file_size": int(os.getenv("MAX_FILE_SIZE", "104857600")),  # 100MB default
    "auto_delete": os.getenv("AUTO_DELETE_AFTER_UPLOAD", "false").lower() == "true",
    "organize_by_date": os.getenv("ORGANIZE_BY_DATE", "true").lower() == "true",
    "max_concurrent_uploads": int(os.getenv("MAX_CONCURRENT_UPLOADS", "3")),
    "chunk_size_mb": int(os.getenv("CHUNK_SIZE_MB", "8")),
    "retry_attempts": int(os.getenv("RETRY_ATTEMPTS", "3")),
    "timeout_seconds": int(os.getenv("TIMEOUT_SECONDS", "300"))
}

# Telegram Configuration
TELEGRAM_CONFIG = {
    "bot_token": os.getenv("TELEGRAM_BOT_TOKEN"),
    "allowed_user_ids": [int(x.strip()) for x in os.getenv("ALLOWED_USER_IDS", "").split(",") if x.strip().isdigit()],
    "enable_notifications": os.getenv("ENABLE_NOTIFICATIONS", "true").lower() == "true",
    "enable_debug": os.getenv("ENABLE_DEBUG", "false").lower() == "true"
}

# System Configuration
SYSTEM_CONFIG = {
    "platform": os.getenv("PLATFORM", "termux"),
    "termux_home": os.getenv("TERMUX_HOME", "/data/data/com.termux/files/home"),
    "storage_path": os.getenv("STORAGE_PATH", "/data/data/com.termux/files/home/storage/shared"),
    "logs_dir": PROJECT_ROOT / "logs",
    "temp_dir": PROJECT_ROOT / "temp"
}

# Ensure directories exist
CREDENTIALS_DIR.mkdir(exist_ok=True)
SYSTEM_CONFIG["logs_dir"].mkdir(exist_ok=True)
SYSTEM_CONFIG["temp_dir"].mkdir(exist_ok=True)
