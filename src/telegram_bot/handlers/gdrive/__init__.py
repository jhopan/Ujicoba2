"""
☁️ Google Drive Handler Module - Modular Google Drive Operations
"""

from .account_manager import GoogleDriveAccountHandler
from .file_operations import GoogleDriveFileHandler
from .setup_guide import GoogleDriveSetupHandler


class GoogleDriveHandler:
    """☁️ Main Google Drive handler with delegation to specialized modules"""
    
    # ========== SETUP & GUIDE (Delegation) ==========
    @staticmethod
    async def setup_drive_menu(query):
        """☁️ Show Google Drive setup menu"""
        await GoogleDriveSetupHandler.setup_drive_menu(query)
    
    @staticmethod
    async def show_setup_guide(query):
        """📖 Show detailed setup guide"""
        await GoogleDriveSetupHandler.show_setup_guide(query)
    
    @staticmethod
    async def show_quick_setup(query):
        """⚡ Show quick setup instructions"""
        await GoogleDriveSetupHandler.show_quick_setup(query)
    
    @staticmethod
    async def setup_help(query):
        """❓ Show setup help and FAQ"""
        await GoogleDriveSetupHandler.setup_help(query)
    
    @staticmethod
    async def setup_troubleshooting(query):
        """🛠️ Setup troubleshooting guide"""
        await GoogleDriveSetupHandler.setup_troubleshooting(query)
    
    @staticmethod
    async def mobile_setup_guide(query):
        """📱 Mobile setup guide"""
        await GoogleDriveSetupHandler.mobile_setup_guide(query)
    
    # ========== ACCOUNT MANAGEMENT (Delegation) ==========
    @staticmethod
    async def manage_accounts(query):
        """👥 Manage Google Drive accounts"""
        await GoogleDriveAccountHandler.manage_accounts(query)
    
    @staticmethod
    async def add_new_account(query):
        """➕ Add new Google Drive account"""
        await GoogleDriveAccountHandler.add_new_account(query)
    
    @staticmethod
    async def view_account_usage(query):
        """📊 View account usage and storage"""
        await GoogleDriveAccountHandler.view_account_usage(query)
    
    @staticmethod
    async def manage_account_list(query):
        """🔧 Manage account list"""
        await GoogleDriveAccountHandler.manage_account_list(query)
    
    @staticmethod
    async def remove_account_menu(query):
        """🗑️ Remove account menu"""
        await GoogleDriveAccountHandler.remove_account_menu(query)
    
    @staticmethod
    async def remove_specific_account(query, account_id: str):
        """🗑️ Remove specific account"""
        await GoogleDriveAccountHandler.remove_specific_account(query, account_id)
    
    @staticmethod
    async def switch_account(query, account_id: str):
        """🔄 Switch active account"""
        await GoogleDriveAccountHandler.switch_account(query, account_id)
    
    # ========== FILE OPERATIONS (Delegation) ==========
    @staticmethod
    async def show_drive_operations(query):
        """📁 Show Google Drive file operations"""
        await GoogleDriveFileHandler.show_drive_operations(query)
    
    @staticmethod
    async def upload_files(query):
        """☁️ Upload files to Google Drive"""
        await GoogleDriveFileHandler.upload_files(query)
    
    @staticmethod
    async def download_files(query):
        """📥 Download files from Google Drive"""
        await GoogleDriveFileHandler.download_files(query)
    
    @staticmethod
    async def list_drive_files(query):
        """📋 List Google Drive files"""
        await GoogleDriveFileHandler.list_drive_files(query)
    
    @staticmethod
    async def backup_folders(query):
        """💾 Backup folders to Google Drive"""
        await GoogleDriveFileHandler.backup_folders(query)
    
    @staticmethod
    async def quick_backup(query):
        """🚀 Quick backup to Google Drive"""
        await GoogleDriveFileHandler.quick_backup(query)
    
    @staticmethod
    async def manage_drive_storage(query):
        """🗑️ Manage Google Drive storage"""
        await GoogleDriveFileHandler.manage_drive_storage(query)
    
    @staticmethod
    async def search_drive_files(query):
        """🔍 Search files in Google Drive"""
        await GoogleDriveFileHandler.search_drive_files(query)
    
    @staticmethod
    async def backup_progress(query):
        """📊 Show backup progress"""
        await GoogleDriveFileHandler.backup_progress(query)
    
    # ========== CREDENTIAL PROCESSING ==========
    @staticmethod
    async def process_credentials(update, context):
        """📎 Process uploaded Google Drive credentials"""
        await GoogleDriveAccountHandler.process_credentials(update, context)


# Export main class
__all__ = ['GoogleDriveHandler']