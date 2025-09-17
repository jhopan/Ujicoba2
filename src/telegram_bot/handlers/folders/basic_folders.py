"""
📁 Basic Folder Handlers - Downloads, Pictures, Documents, WhatsApp, DCIM
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

from ...config.manager import config_manager, STORAGE_PATH

class BasicFolderHandler:
    """📁 Handle basic folder operations (Downloads, Pictures, Documents, etc.)"""
    
    @staticmethod
    async def add_downloads_folder(query):
        """📥 Add downloads folder"""
        downloads_path = str(STORAGE_PATH / "Download")
        config_manager.save_folder_config("Downloads", downloads_path)
        await query.answer("✅ Downloads folder added")
        
        success_text = f"""
✅ *DOWNLOADS FOLDER ADDED*

📥 *Folder:* Downloads
📂 *Path:* `{downloads_path}`
📊 *Status:* Active monitoring

🎯 *Features:*
• Automatic file detection
• All download types supported
• Date-based organization
• Incremental backup

💡 *All your downloads will be safely backed up.*
        """
        
        keyboard = [
            [InlineKeyboardButton("📁 Add More Folders", callback_data="manage_folders")],
            [InlineKeyboardButton("🚀 Start Backup Now", callback_data="quick_backup")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            success_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def add_pictures_folder(query):
        """📸 Add pictures folder"""
        pictures_path = str(STORAGE_PATH / "Pictures")
        config_manager.save_folder_config("Pictures", pictures_path)
        await query.answer("✅ Pictures folder added")
        
        success_text = f"""
✅ *PICTURES FOLDER ADDED*

📸 *Folder:* Pictures
📂 *Path:* `{pictures_path}`
📊 *File Types:* JPG, PNG, GIF, etc.

🎯 *Photo backup features:*
• Automatic DCIM detection
• Subdirectory scanning
• Date-based organization
• Duplicate detection

💡 *All your photos will be safely backed up.*
        """
        
        keyboard = [
            [InlineKeyboardButton("📱 Add DCIM Too", callback_data="add_dcim")],
            [InlineKeyboardButton("🚀 Start Backup Now", callback_data="quick_backup")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            success_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def add_documents_folder(query):
        """📄 Add documents folder"""
        documents_path = str(STORAGE_PATH / "Documents")
        config_manager.save_folder_config("Documents", documents_path)
        await query.answer("✅ Documents folder added")
        
        success_text = f"""
✅ *DOCUMENTS FOLDER ADDED*

📄 *Folder:* Documents
📂 *Path:* `{documents_path}`
📊 *File Types:* PDF, DOC, TXT, etc.

🎯 *Features:*
• Automatic file type detection
• Smart organization by type
• Duplicate file handling
• Incremental backup

💡 *All your documents will be organized in Google Drive.*
        """
        
        keyboard = [
            [InlineKeyboardButton("📁 Add More Folders", callback_data="manage_folders")],
            [InlineKeyboardButton("🚀 Start Backup", callback_data="quick_backup")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            success_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def add_whatsapp_folder(query):
        """💬 Add WhatsApp media folder"""
        whatsapp_path = str(STORAGE_PATH / "WhatsApp" / "Media")
        config_manager.save_folder_config("WhatsApp Media", whatsapp_path)
        await query.answer("✅ WhatsApp folder added")
        
        success_text = f"""
✅ *WHATSAPP MEDIA ADDED*

💬 *Folder:* WhatsApp Media
📂 *Path:* `{whatsapp_path}`
📊 *Content:* Images, Videos, Audio, Documents

🎯 *WhatsApp backup features:*
• Images from chats
• Videos and voice messages
• Documents shared in chats
• Status media (if saved)

💡 *WhatsApp media organized by type in Google Drive.*
        """
        
        keyboard = [
            [InlineKeyboardButton("📁 Add More Folders", callback_data="manage_folders")],
            [InlineKeyboardButton("🚀 Start Backup", callback_data="quick_backup")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            success_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def add_dcim_folder(query):
        """📱 Add DCIM folder"""
        dcim_path = str(STORAGE_PATH / "DCIM")
        config_manager.save_folder_config("DCIM Camera", dcim_path)
        await query.answer("✅ DCIM folder added")
        
        success_text = f"""
✅ *DCIM CAMERA FOLDER ADDED*

📱 *Folder:* DCIM (Camera)
📂 *Path:* `{dcim_path}`
📊 *Content:* Photos & Videos from camera

🎯 *Camera backup features:*
• All camera photos
• Recorded videos
• Screenshots
• Automatic date organization

💡 *Camera photos preserved with full quality.*
        """
        
        keyboard = [
            [InlineKeyboardButton("📁 Add More Folders", callback_data="manage_folders")],
            [InlineKeyboardButton("🚀 Start Backup", callback_data="quick_backup")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            success_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )