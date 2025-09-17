"""
📁 Config Manager - Handle all configuration operations
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
TERMUX_HOME = Path("/data/data/com.termux/files/home")
STORAGE_PATH = TERMUX_HOME / "storage" / "shared"

class ConfigManager:
    """⚙️ Manage all configuration files and settings"""
    
    def __init__(self):
        self.config_dir = PROJECT_ROOT / "config"
        self.credentials_dir = PROJECT_ROOT / "credentials"
        self.env_file = PROJECT_ROOT / ".env"
        
        # Load .env file
        self._load_env_file()
        
        # Ensure directories exist
        self.config_dir.mkdir(exist_ok=True)
        self.credentials_dir.mkdir(exist_ok=True)
    
    def _load_env_file(self):
        """Load .env file manually if dotenv is not available"""
        if self.env_file.exists():
            with open(self.env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
    
    def get_setting(self, key: str, default: str = '') -> str:
        """📖 Get setting value from environment"""
        return os.getenv(key, default)
    
    def set_setting(self, key: str, value: str):
        """💾 Set setting value in .env file"""
        if not self.env_file.exists():
            self.env_file.write_text("")
        
        content = self.env_file.read_text()
        
        if f"{key}=" in content:
            # Update existing
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith(f"{key}="):
                    lines[i] = f"{key}={value}"
                    break
            content = '\n'.join(lines)
        else:
            # Add new
            content += f"\n{key}={value}\n"
        
        self.env_file.write_text(content)
        os.environ[key] = value
    
    def count_credentials(self) -> int:
        """📊 Count Google Drive credentials files"""
        if not self.credentials_dir.exists():
            return 0
        return len(list(self.credentials_dir.glob("*.json")))
    
    def save_folder_config(self, name: str, path: str):
        """💾 Save folder configuration"""
        folders_file = self.config_dir / "folders.json"
        
        # Load existing
        folders = []
        if folders_file.exists():
            try:
                loaded_data = json.loads(folders_file.read_text())
                # Ensure we have a list of dictionaries
                if isinstance(loaded_data, list):
                    folders = [f for f in loaded_data if isinstance(f, dict)]
                else:
                    folders = []
            except:
                folders = []
        
        # Add new folder if not exists
        existing = [f for f in folders if isinstance(f, dict) and f.get('path') == path]
        if not existing:
            folders.append({
                'name': name,
                'path': path,
                'added': datetime.now().isoformat(),
                'active': True
            })
            
            folders_file.write_text(json.dumps(folders, indent=2))
    
    def get_folder_count(self) -> int:
        """📁 Get monitored folder count"""
        folders_file = self.config_dir / "folders.json"
        if not folders_file.exists():
            return 0
        
        try:
            loaded_data = json.loads(folders_file.read_text())
            if isinstance(loaded_data, list):
                folders = [f for f in loaded_data if isinstance(f, dict)]
                return len([f for f in folders if f.get('active', True)])
            return 0
        except:
            return 0
    
    def get_folders(self) -> List[Dict]:
        """📋 Get all monitored folders"""
        folders_file = self.config_dir / "folders.json"
        if not folders_file.exists():
            return []
        
        try:
            loaded_data = json.loads(folders_file.read_text())
            if isinstance(loaded_data, list):
                return [f for f in loaded_data if isinstance(f, dict)]
            return []
        except:
            return []
    
    def remove_folder_config(self, folder_name: str) -> bool:
        """🗑️ Remove folder configuration"""
        folders_file = self.config_dir / "folders.json"
        if not folders_file.exists():
            return False
        
        try:
            loaded_data = json.loads(folders_file.read_text())
            if isinstance(loaded_data, list):
                folders = [f for f in loaded_data if isinstance(f, dict)]
                
                # Remove folder by name
                original_count = len(folders)
                folders = [f for f in folders if f.get('name') != folder_name]
                
                if len(folders) < original_count:
                    # Save updated list
                    folders_file.write_text(json.dumps(folders, indent=2))
                    return True
            return False
        except:
            return False
    
    def save_credentials(self, credentials_data: dict, account_number: int) -> Path:
        """💾 Save Google Drive credentials"""
        filename = f"account{account_number}_credentials.json"
        file_path = self.credentials_dir / filename
        
        file_path.write_text(json.dumps(credentials_data, indent=2))
        return file_path
    
    def check_permission(self, user_id: int) -> bool:
        """✅ Check user permission"""
        allowed_ids = self.get_setting('ALLOWED_USER_IDS', '').split(',')
        return str(user_id) in allowed_ids
    
    def toggle_auto_delete(self) -> bool:
        """🗑️ Toggle auto-delete setting"""
        current = self.get_setting('AUTO_DELETE_AFTER_UPLOAD', 'false') == 'true'
        new_value = 'false' if current else 'true'
        self.set_setting('AUTO_DELETE_AFTER_UPLOAD', new_value)
        return new_value == 'true'
    
    def get_system_status(self) -> Dict:
        """📊 Get comprehensive system status"""
        return {
            'credentials_count': self.count_credentials(),
            'folder_count': self.get_folder_count(),
            'auto_delete': self.get_setting('AUTO_DELETE_AFTER_UPLOAD', 'false') == 'true',
            'notifications': self.get_setting('NOTIFICATIONS_ENABLED', 'true') == 'true',
            'debug_mode': self.get_setting('DEBUG_MODE', 'false') == 'true',
            'total_storage': self.count_credentials() * 15,
            'setup_completed': self.get_setting('SETUP_COMPLETED', 'false') == 'true',
            'platform': self.get_setting('PLATFORM', 'unknown')
        }

# Global instance
config_manager = ConfigManager()
