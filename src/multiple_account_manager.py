"""
Multiple Google Accounts Manager
Untuk mengelola backup ke 2-3 akun Google Drive
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from src.google_drive_manager import GoogleDriveManager
from config.settings import GOOGLE_DRIVE_CONFIG, BACKUP_CONFIG

class MultipleAccountManager:
    """Manager untuk handle unlimited Google Drive accounts"""
    
    def __init__(self, max_accounts: int = 50):  # Support up to 50 accounts
        self.max_accounts = max_accounts
        self.accounts: List[GoogleDriveManager] = []
        self.logger = logging.getLogger(__name__)
        self.accounts_config_file = Path("config/accounts.json")
        self._load_accounts()
        
    def _load_accounts(self):
        """Load semua akun Google Drive yang tersedia"""
        credentials_dir = Path(GOOGLE_DRIVE_CONFIG["credentials_file"]).parent
        
        # Load account configuration
        accounts_config = self._load_accounts_config()
        
        for account_info in accounts_config.get('accounts', []):
            try:
                account_index = account_info['index']
                account_name = account_info.get('name', f'Account {account_index}')
                
                # Check if credentials exist for this account
                token_file = credentials_dir / f"token_account_{account_index}.json"
                
                if token_file.exists():
                    account = GoogleDriveManager(account_index=account_index)
                    account.account_name = account_name  # Add custom name
                    self.accounts.append(account)
                    self.logger.info(f"Loaded Google account {account_index}: {account_name}")
                else:
                    self.logger.warning(f"Token not found for account {account_index}: {account_name}")
                    
            except Exception as e:
                self.logger.error(f"Failed to load Google account {account_info}: {e}")
                
        if not self.accounts:
            self.logger.warning("No Google accounts could be loaded")
            
    def _load_accounts_config(self) -> dict:
        """Load accounts configuration from JSON file"""
        if self.accounts_config_file.exists():
            try:
                with open(self.accounts_config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading accounts config: {e}")
        
        # Return default config
        return {'accounts': []}
        
    def _save_accounts_config(self, config: dict):
        """Save accounts configuration to JSON file"""
        try:
            self.accounts_config_file.parent.mkdir(exist_ok=True)
            with open(self.accounts_config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving accounts config: {e}")
            
    def add_account(self, account_name: str = None) -> dict:
        """Add new Google account and return OAuth info"""
        try:
            # Get next available account index
            config = self._load_accounts_config()
            existing_indices = [acc['index'] for acc in config.get('accounts', [])]
            
            next_index = 0
            while next_index in existing_indices:
                next_index += 1
                
            if next_index >= self.max_accounts:
                raise Exception(f"Maximum accounts limit reached ({self.max_accounts})")
            
            # Generate OAuth URL
            from google_auth_oauthlib.flow import Flow
            
            flow = Flow.from_client_secrets_file(
                str(GOOGLE_DRIVE_CONFIG["credentials_file"]),
                scopes=GOOGLE_DRIVE_CONFIG["scopes"],
                redirect_uri='urn:ietf:wg:oauth:2.0:oob'
            )
            
            auth_url, state = flow.authorization_url(
                prompt='consent',
                access_type='offline'
            )
            
            # Store pending account info
            if not account_name:
                account_name = f"Account {next_index}"
                
            pending_account = {
                'index': next_index,
                'name': account_name,
                'state': state,
                'flow_info': {
                    'auth_url': auth_url,
                    'redirect_uri': flow.redirect_uri
                }
            }
            
            # Save to temp storage for OAuth completion
            temp_file = f"config/pending_account_{next_index}.json"
            with open(temp_file, 'w') as f:
                json.dump(pending_account, f, indent=2)
            
            return {
                'account_index': next_index,
                'account_name': account_name,
                'auth_url': auth_url,
                'instructions': [
                    "1. Klik link OAuth di atas",
                    "2. Login dengan akun Google yang ingin ditambahkan", 
                    "3. Berikan permission untuk aplikasi",
                    "4. Copy kode authorization yang diberikan",
                    "5. Gunakan kode tersebut untuk menyelesaikan setup"
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Error adding account: {e}")
            raise
            
    def complete_account_setup(self, account_index: int, auth_code: str) -> bool:
        """Complete account setup with authorization code"""
        try:
            # Load pending account info
            temp_file = f"config/pending_account_{account_index}.json"
            
            if not os.path.exists(temp_file):
                raise Exception("Pending account info not found")
                
            with open(temp_file, 'r') as f:
                pending_account = json.load(f)
            
            # Complete OAuth flow
            from google_auth_oauthlib.flow import Flow
            
            flow = Flow.from_client_secrets_file(
                str(GOOGLE_DRIVE_CONFIG["credentials_file"]),
                scopes=GOOGLE_DRIVE_CONFIG["scopes"],
                redirect_uri='urn:ietf:wg:oauth:2.0:oob'
            )
            
            # Exchange code for credentials
            flow.fetch_token(code=auth_code)
            
            # Save credentials
            credentials_dir = Path(GOOGLE_DRIVE_CONFIG["credentials_file"]).parent
            token_file = credentials_dir / f"token_account_{account_index}.json"
            
            with open(token_file, 'w') as f:
                f.write(flow.credentials.to_json())
            
            # Update accounts config
            config = self._load_accounts_config()
            if 'accounts' not in config:
                config['accounts'] = []
                
            config['accounts'].append({
                'index': account_index,
                'name': pending_account['name'],
                'added_date': datetime.now().isoformat(),
                'status': 'active'
            })
            
            self._save_accounts_config(config)
            
            # Remove temp file
            os.remove(temp_file)
            
            # Reload accounts
            self._load_accounts()
            
            self.logger.info(f"Successfully added account {account_index}: {pending_account['name']}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error completing account setup: {e}")
            return False
            
    def get_account_with_most_space(self) -> Optional[GoogleDriveManager]:
        """Dapatkan akun dengan storage paling banyak"""
        best_account = None
        max_available = 0
        
        for account in self.accounts:
            try:
                storage_info = account.get_storage_usage()
                if storage_info and storage_info['available_gb'] > max_available:
                    max_available = storage_info['available_gb']
                    best_account = account
            except Exception as e:
                self.logger.error(f"Error checking storage for account {account.account_index}: {e}")
                
        return best_account
        
    def get_storage_summary(self) -> List[Dict]:
        """Dapatkan ringkasan storage semua akun"""
        summary = []
        
        for account in self.accounts:
            try:
                storage_info = account.get_storage_usage()
                if storage_info:
                    summary.append({
                        'account_index': account.account_index,
                        'total_gb': storage_info['total_gb'],
                        'used_gb': storage_info['used_gb'],
                        'available_gb': storage_info['available_gb'],
                        'usage_percentage': (storage_info['used_gb'] / storage_info['total_gb']) * 100
                    })
            except Exception as e:
                self.logger.error(f"Error getting storage for account {account.account_index}: {e}")
                summary.append({
                    'account_index': account.account_index,
                    'error': str(e)
                })
                
        return summary
        
    def balance_files_across_accounts(self) -> Dict:
        """Balance file distribution across accounts"""
        # Implementasi untuk redistribute file jika ada akun yang penuh
        pass
        
    def get_total_available_storage(self) -> float:
        """Dapatkan total storage yang tersedia di semua akun"""
        total = 0
        
        for account in self.accounts:
            try:
                storage_info = account.get_storage_usage()
                if storage_info:
                    total += storage_info['available_gb']
            except Exception as e:
                self.logger.error(f"Error getting storage for account {account.account_index}: {e}")
                
        return total
