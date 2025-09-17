"""
Enhanced Settings Manager for configuration and preferences
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
import logging

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

logger = logging.getLogger(__name__)

class EnhancedSettings:
    def __init__(self, config_dir: str = "~/.backup_system"):
        self.config_dir = Path(config_dir).expanduser()
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.settings_file = self.config_dir / "settings.json"
        self.accounts_file = self.config_dir / "accounts.json"
        self.backup_rules_file = self.config_dir / "backup_rules.yaml"
        
        # Default settings
        self.default_settings = {
            'backup': {
                'auto_schedule': True,
                'schedule_time': '00:00',  # Midnight
                'max_file_size': 100 * 1024 * 1024,  # 100MB
                'retry_attempts': 3,
                'retry_delay': 60,  # seconds
                'delete_after_upload': False,
                'compress_files': False,
                'verify_uploads': True
            },
            'telegram': {
                'send_progress_updates': True,
                'progress_update_interval': 10,  # seconds
                'send_completion_notifications': True,
                'send_error_notifications': True,
                'allowed_users': []  # Telegram user IDs
            },
            'storage': {
                'max_storage_per_account': 15 * 1024 * 1024 * 1024,  # 15GB
                'storage_warning_threshold': 0.9,  # 90%
                'auto_rotate_accounts': True,
                'preferred_account_order': []
            },
            'file_organization': {
                'organize_by_date': True,
                'organize_by_type': True,
                'date_format': '%Y-%m-%d',
                'create_manifest': True,
                'duplicate_handling': 'skip'  # skip, overwrite, rename
            },
            'network': {
                'connection_timeout': 30,
                'upload_timeout': 300,
                'max_concurrent_uploads': 3,
                'bandwidth_limit': None,  # bytes per second, None = unlimited
                'use_resumable_uploads': True
            },
            'logging': {
                'level': 'INFO',
                'max_log_size': 10 * 1024 * 1024,  # 10MB
                'backup_count': 5,
                'log_to_file': True,
                'log_to_telegram': True
            }
        }
        
        self.settings = self.load_settings()
        self.accounts = self.load_accounts()
        self.backup_rules = self.load_backup_rules()
    
    def load_settings(self) -> Dict[str, Any]:
        """Load settings from file or create with defaults"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                
                # Merge with defaults to ensure all keys exist
                settings = self._merge_dict(self.default_settings, loaded_settings)
                logger.info("Settings loaded successfully")
                return settings
            else:
                logger.info("No settings file found, using defaults")
                self.save_settings(self.default_settings)
                return self.default_settings.copy()
        
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
            return self.default_settings.copy()
    
    def save_settings(self, settings: Dict[str, Any] = None) -> bool:
        """Save settings to file"""
        try:
            if settings is None:
                settings = self.settings
            
            # Update timestamp
            settings['last_updated'] = datetime.now().isoformat()
            
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            
            self.settings = settings
            logger.info("Settings saved successfully")
            return True
        
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
            return False
    
    def load_accounts(self) -> List[Dict[str, Any]]:
        """Load Google Drive accounts configuration"""
        try:
            if self.accounts_file.exists():
                with open(self.accounts_file, 'r') as f:
                    accounts = json.load(f)
                logger.info(f"Loaded {len(accounts)} accounts")
                return accounts
            else:
                logger.info("No accounts file found")
                return []
        
        except Exception as e:
            logger.error(f"Failed to load accounts: {e}")
            return []
    
    def save_accounts(self, accounts: List[Dict[str, Any]] = None) -> bool:
        """Save accounts configuration"""
        try:
            if accounts is None:
                accounts = self.accounts
            
            with open(self.accounts_file, 'w') as f:
                json.dump(accounts, f, indent=2)
            
            self.accounts = accounts
            logger.info("Accounts saved successfully")
            return True
        
        except Exception as e:
            logger.error(f"Failed to save accounts: {e}")
            return False
    
    def load_backup_rules(self) -> Dict[str, Any]:
        """Load backup rules from YAML file"""
        try:
            if self.backup_rules_file.exists():
                with open(self.backup_rules_file, 'r') as f:
                    if YAML_AVAILABLE:
                        rules = yaml.safe_load(f) or {}
                    else:
                        # Fallback to JSON format if yaml not available
                        rules = json.load(f) or {}
                logger.info("Backup rules loaded successfully")
                return rules
            else:
                default_rules = {
                    'include_paths': ['~/Downloads', '~/Documents', '~/Pictures'],
                    'exclude_paths': ['~/Downloads/temp', '*/node_modules'],
                    'file_types': {
                        'include': [],  # Empty = all types
                        'exclude': ['.tmp', '.log', '.cache']
                    },
                    'size_limits': {
                        'min_size': 0,
                        'max_size': None
                    },
                    'date_filters': {
                        'newer_than_days': None,
                        'older_than_days': None
                    }
                }
                self.save_backup_rules(default_rules)
                return default_rules
        
        except Exception as e:
            logger.error(f"Failed to load backup rules: {e}")
            return {}
    
    def save_backup_rules(self, rules: Dict[str, Any] = None) -> bool:
        """Save backup rules to YAML file"""
        try:
            if rules is None:
                rules = self.backup_rules
            
            with open(self.backup_rules_file, 'w') as f:
                if YAML_AVAILABLE:
                    yaml.dump(rules, f, default_flow_style=False, indent=2)
                else:
                    # Fallback to JSON format if yaml not available
                    json.dump(rules, f, indent=2)
            
            self.backup_rules = rules
            logger.info("Backup rules saved successfully")
            return True
        
        except Exception as e:
            logger.error(f"Failed to save backup rules: {e}")
            return False
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get a setting value using dot notation
        
        Args:
            key_path: Dot-separated path (e.g., 'backup.retry_attempts')
            default: Default value if not found
            
        Returns:
            Setting value or default
        """
        try:
            keys = key_path.split('.')
            value = self.settings
            
            for key in keys:
                value = value[key]
            
            return value
        
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any) -> bool:
        """
        Set a setting value using dot notation
        
        Args:
            key_path: Dot-separated path
            value: Value to set
            
        Returns:
            bool: Success status
        """
        try:
            keys = key_path.split('.')
            current = self.settings
            
            # Navigate to parent
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            
            # Set value
            current[keys[-1]] = value
            logger.info(f"Setting updated: {key_path} = {value}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to set setting {key_path}: {e}")
            return False
    
    def add_account(self, account_name: str, credentials_path: str, 
                   max_storage: int = None) -> bool:
        """
        Add a new Google Drive account
        
        Args:
            account_name: Name for the account
            credentials_path: Path to credentials file
            max_storage: Maximum storage for this account
            
        Returns:
            bool: Success status
        """
        try:
            new_account = {
                'name': account_name,
                'credentials_path': credentials_path,
                'max_storage': max_storage or self.get('storage.max_storage_per_account'),
                'current_usage': 0,
                'enabled': True,
                'added_date': datetime.now().isoformat()
            }
            
            # Check if account already exists
            for account in self.accounts:
                if account['name'] == account_name:
                    logger.warning(f"Account {account_name} already exists")
                    return False
            
            self.accounts.append(new_account)
            self.save_accounts()
            logger.info(f"Added new account: {account_name}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to add account {account_name}: {e}")
            return False
    
    def remove_account(self, account_name: str) -> bool:
        """Remove a Google Drive account"""
        try:
            original_count = len(self.accounts)
            self.accounts = [acc for acc in self.accounts if acc['name'] != account_name]
            
            if len(self.accounts) < original_count:
                self.save_accounts()
                logger.info(f"Removed account: {account_name}")
                return True
            else:
                logger.warning(f"Account {account_name} not found")
                return False
        
        except Exception as e:
            logger.error(f"Failed to remove account {account_name}: {e}")
            return False
    
    def get_enabled_accounts(self) -> List[Dict[str, Any]]:
        """Get list of enabled accounts"""
        return [acc for acc in self.accounts if acc.get('enabled', True)]
    
    def update_account_usage(self, account_name: str, usage_bytes: int) -> bool:
        """Update storage usage for an account"""
        try:
            for account in self.accounts:
                if account['name'] == account_name:
                    account['current_usage'] = usage_bytes
                    account['last_updated'] = datetime.now().isoformat()
                    self.save_accounts()
                    return True
            
            logger.warning(f"Account {account_name} not found for usage update")
            return False
        
        except Exception as e:
            logger.error(f"Failed to update account usage: {e}")
            return False
    
    def get_account_with_space(self, required_space: int) -> Optional[Dict[str, Any]]:
        """
        Find an account with sufficient free space
        
        Args:
            required_space: Required space in bytes
            
        Returns:
            Account dict or None if no space available
        """
        enabled_accounts = self.get_enabled_accounts()
        
        for account in enabled_accounts:
            max_storage = account.get('max_storage', self.get('storage.max_storage_per_account'))
            current_usage = account.get('current_usage', 0)
            available_space = max_storage - current_usage
            
            if available_space >= required_space:
                return account
        
        return None
    
    def export_settings(self, export_path: Path) -> bool:
        """Export all settings to a backup file"""
        try:
            export_data = {
                'settings': self.settings,
                'accounts': self.accounts,
                'backup_rules': self.backup_rules,
                'export_date': datetime.now().isoformat(),
                'version': '1.0'
            }
            
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            logger.info(f"Settings exported to: {export_path}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to export settings: {e}")
            return False
    
    def import_settings(self, import_path: Path) -> bool:
        """Import settings from a backup file"""
        try:
            with open(import_path, 'r') as f:
                import_data = json.load(f)
            
            if 'settings' in import_data:
                self.settings = import_data['settings']
                self.save_settings()
            
            if 'accounts' in import_data:
                self.accounts = import_data['accounts']
                self.save_accounts()
            
            if 'backup_rules' in import_data:
                self.backup_rules = import_data['backup_rules']
                self.save_backup_rules()
            
            logger.info(f"Settings imported from: {import_path}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to import settings: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """Reset all settings to defaults"""
        try:
            self.settings = self.default_settings.copy()
            self.save_settings()
            logger.info("Settings reset to defaults")
            return True
        
        except Exception as e:
            logger.error(f"Failed to reset settings: {e}")
            return False
    
    def get_settings_summary(self) -> str:
        """Get a formatted summary of current settings"""
        summary = "=== Backup System Settings ===\n\n"
        
        # Backup settings
        summary += "📱 Backup Configuration:\n"
        summary += f"  • Auto Schedule: {self.get('backup.auto_schedule')}\n"
        summary += f"  • Schedule Time: {self.get('backup.schedule_time')}\n"
        summary += f"  • Max File Size: {self._format_size(self.get('backup.max_file_size'))}\n"
        summary += f"  • Retry Attempts: {self.get('backup.retry_attempts')}\n"
        summary += f"  • Delete After Upload: {self.get('backup.delete_after_upload')}\n\n"
        
        # Account summary
        enabled_accounts = self.get_enabled_accounts()
        summary += f"💾 Storage Accounts: {len(enabled_accounts)} enabled\n"
        for acc in enabled_accounts:
            usage = acc.get('current_usage', 0)
            max_storage = acc.get('max_storage', 0)
            usage_pct = (usage / max_storage * 100) if max_storage > 0 else 0
            summary += f"  • {acc['name']}: {usage_pct:.1f}% used\n"
        
        summary += f"\n📁 File Organization:\n"
        summary += f"  • Organize by Date: {self.get('file_organization.organize_by_date')}\n"
        summary += f"  • Organize by Type: {self.get('file_organization.organize_by_type')}\n"
        summary += f"  • Duplicate Handling: {self.get('file_organization.duplicate_handling')}\n"
        
        return summary
    
    def _merge_dict(self, default: Dict, override: Dict) -> Dict:
        """Recursively merge dictionaries"""
        result = default.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_dict(result[key], value)
            else:
                result[key] = value
        return result
    
    def _format_size(self, size_bytes: int) -> str:
        """Format size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
