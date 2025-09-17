"""
📁 Folder Handler Package - Main orchestrator
Refactored into smaller, maintainable modules
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

from ...config.manager import config_manager
from .basic_folders import BasicFolderHandler
from .popular_folders import PopularFolderHandler
from .folder_management import FolderManagementHandler

class FolderHandler:
    """📁 Main folder handler orchestrator - delegates to specialized handlers"""
    
    # ========== MAIN MENU ==========
    @staticmethod
    async def manage_folders_menu(query):
        """📁 Show folder management menu"""
        folder_count = config_manager.get_folder_count()
        
        folders_text = f"""
📁 *BACKUP FOLDERS*

📊 *Current Status:*
• Monitored Folders: {folder_count}
• Status: {'✅ Ready' if folder_count > 0 else '⚠️ No folders'}

🎯 *Quick Add Popular Folders:*
        """
        
        keyboard = [
            [InlineKeyboardButton("📥 Downloads", callback_data="add_downloads")],
            [InlineKeyboardButton("📸 Pictures/DCIM", callback_data="add_pictures")],
            [InlineKeyboardButton("📄 Documents", callback_data="add_documents")],
            [InlineKeyboardButton("💬 WhatsApp Media", callback_data="add_whatsapp")],
            [InlineKeyboardButton("📝 Custom Path", callback_data="add_custom_path")],
            [InlineKeyboardButton("📋 View All Folders", callback_data="view_all_folders")],
            [InlineKeyboardButton("🗑️ Remove Folder", callback_data="remove_folder")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            folders_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    # ========== BASIC FOLDERS (Delegation) ==========
    @staticmethod
    async def add_downloads_folder(query):
        """📥 Add downloads folder"""
        await BasicFolderHandler.add_downloads_folder(query)
    
    @staticmethod
    async def add_pictures_folder(query):
        """📸 Add pictures folder"""
        await BasicFolderHandler.add_pictures_folder(query)
    
    @staticmethod
    async def add_documents_folder(query):
        """📄 Add documents folder"""
        await BasicFolderHandler.add_documents_folder(query)
    
    @staticmethod
    async def add_whatsapp_folder(query):
        """💬 Add WhatsApp media folder"""
        await BasicFolderHandler.add_whatsapp_folder(query)
    
    @staticmethod
    async def add_dcim_folder(query):
        """📱 Add DCIM folder"""
        await BasicFolderHandler.add_dcim_folder(query)
    
    # ========== POPULAR FOLDERS (Delegation) ==========
    @staticmethod
    async def add_folder_music(query):
        """🎵 Add Music folder"""
        await PopularFolderHandler.add_folder_music(query)
    
    @staticmethod
    async def add_folder_movies(query):
        """🎬 Add Movies folder"""
        await PopularFolderHandler.add_folder_movies(query)
    
    @staticmethod
    async def add_folder_games(query):
        """🎮 Add Games Data folder"""
        await PopularFolderHandler.add_folder_games(query)
    
    @staticmethod
    async def add_folder_camera(query):
        """📷 Add Camera folder"""
        await PopularFolderHandler.add_folder_camera(query)
    
    @staticmethod
    async def add_folder_recordings(query):
        """🎙️ Add Recordings folder"""
        await PopularFolderHandler.add_folder_recordings(query)
    
    @staticmethod
    async def add_folder_backups(query):
        """💾 Add Backups folder"""
        await PopularFolderHandler.add_folder_backups(query)
    
    @staticmethod
    async def add_folder_screenshots(query):
        """📱 Add Screenshots folder"""
        await PopularFolderHandler.add_folder_screenshots(query)
    
    # ========== FOLDER MANAGEMENT (Delegation) ==========
    @staticmethod
    async def view_all_folders(query):
        """📋 View all monitored folders"""
        await FolderManagementHandler.view_all_folders(query)
    
    @staticmethod
    async def remove_folder(query):
        """🗑️ Remove folder from monitoring"""
        await FolderManagementHandler.remove_folder(query)
    
    @staticmethod
    async def remove_specific_folder(query, folder_name: str):
        """🗑️ Remove specific folder"""
        await FolderManagementHandler.remove_specific_folder(query, folder_name)
    
    @staticmethod
    async def add_custom_path(query):
        """📝 Add custom folder path - User friendly version"""
        await FolderManagementHandler.add_custom_path(query)
    
    @staticmethod
    async def add_manual_path(query):
        """📝 Manual path entry (original method)"""
        await FolderManagementHandler.add_manual_path(query)
    
    @staticmethod
    async def create_new_folder_instruction(query):
        """🆕 Create new folder instruction"""
        await FolderManagementHandler.create_new_folder_instruction(query)
    
    @staticmethod
    async def add_existing_folder_instruction(query):
        """📁 Add existing folder instruction"""
        await FolderManagementHandler.add_existing_folder_instruction(query)
    
    @staticmethod
    async def manual_command_instruction(query):
        """📋 Manual command instruction"""
        await FolderManagementHandler.manual_command_instruction(query)

# Export main class
__all__ = ['FolderHandler']