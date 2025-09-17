"""
📁 Folder Management Handler - Handle folder operations
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

from ..config.manager import config_manager, STORAGE_PATH

class FolderHandler:
    """📁 Handle folder management operations"""
    
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
    
    @staticmethod
    async def add_custom_path(query):
        """📝 Add custom folder path"""
        await query.answer("📝 Custom path feature")
        
        instruction_text = """
📝 *ADD CUSTOM FOLDER PATH*

🎯 *How to add custom folder:*

1️⃣ Send me the folder path like this:
   `/add_folder /storage/emulated/0/MyFolder`

2️⃣ Or specify name and path:
   `/add_folder MyMusic /storage/emulated/0/Music`

3️⃣ Examples:
   • `/add_folder /sdcard/MyFolder`
   • `/add_folder Games /storage/emulated/0/Games`
   • `/add_folder Work /storage/emulated/0/Documents/Work`

📋 *Format:* `/add_folder [name] [path]`
💡 *Path must exist on your device*
        """
        
        keyboard = [
            [InlineKeyboardButton("📁 Back to Folders", callback_data="manage_folders")],
            [InlineKeyboardButton("🔙 Main Menu", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            instruction_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def view_all_folders(query):
        """📋 View all monitored folders"""
        folders = config_manager.get_folders()
        
        if not folders:
            folders_text = """
📋 *MONITORED FOLDERS*

⚠️ *No folders configured yet*

🎯 *To add folders:*
• Use quick add buttons
• Add custom paths
• Select popular folders

💡 *Start by adding Downloads or Pictures folder.*
            """
            
            keyboard = [
                [InlineKeyboardButton("📁 Add Folders", callback_data="manage_folders")],
                [InlineKeyboardButton("🔙 Back", callback_data="back_to_main")]
            ]
        else:
            folders_text = "📋 *MONITORED FOLDERS*\n\n"
            
            for i, folder in enumerate(folders, 1):
                status = "✅" if folder.get('active', True) else "❌"
                folders_text += f"*{i}. {folder['name']}*\n"
                folders_text += f"   📂 `{folder['path']}`\n"
                folders_text += f"   📊 Status: {status}\n\n"
            
            keyboard = [
                [InlineKeyboardButton("📁 Add More", callback_data="manage_folders")],
                [InlineKeyboardButton("🗑️ Remove Folder", callback_data="remove_folder")],
                [InlineKeyboardButton("🔙 Back", callback_data="manage_folders")]
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            folders_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def remove_folder(query):
        """🗑️ Remove folder from monitoring"""
        folders = config_manager.get_folders()
        
        if not folders:
            await query.answer("❌ No folders to remove")
            
            remove_text = """
🗑️ *REMOVE FOLDER*

⚠️ *No folders configured*

🎯 *To remove folders:*
• First add some folders
• Then use this option to remove them
• Folders will be removed from monitoring only

💡 *Files on your device won't be deleted*
            """
            
            keyboard = [
                [InlineKeyboardButton("📁 Add Folders", callback_data="manage_folders")],
                [InlineKeyboardButton("🔙 Back", callback_data="manage_folders")]
            ]
            
        else:
            await query.answer("🗑️ Select folder to remove")
            
            remove_text = """
🗑️ *REMOVE FOLDER FROM MONITORING*

⚠️ *Select folder to remove:*

📋 *Current monitored folders:*
            """
            
            keyboard = []
            for i, folder in enumerate(folders, 1):
                status = "✅" if folder.get('active', True) else "❌"
                remove_text += f"\n*{i}. {folder['name']}* {status}"
                # Add button to remove this specific folder
                keyboard.append([InlineKeyboardButton(
                    f"🗑️ Remove {folder['name']}", 
                    callback_data=f"remove_folder_{folder['name']}"
                )])
            
            remove_text += "\n\n💡 *Files on device won't be deleted, only removed from backup monitoring*"
            
            keyboard.extend([
                [InlineKeyboardButton("📁 Back to Folders", callback_data="manage_folders")],
                [InlineKeyboardButton("🔙 Main Menu", callback_data="back_to_main")]
            ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            remove_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def remove_specific_folder(query, folder_name: str):
        """🗑️ Remove specific folder"""
        success = config_manager.remove_folder_config(folder_name)
        
        if success:
            await query.answer(f"✅ {folder_name} removed from monitoring")
            
            success_text = f"""
✅ *FOLDER REMOVED*

🗑️ *Removed:* {folder_name}
📊 *Status:* No longer monitored

🎯 *What happened:*
• Folder removed from backup list
• Files on device are safe
• No longer included in backups
• Can be re-added anytime

💡 *Use "Add Folders" to monitor it again*
            """
            
            keyboard = [
                [InlineKeyboardButton("📁 Add Folders", callback_data="manage_folders")],
                [InlineKeyboardButton("🗑️ Remove More", callback_data="remove_folder")],
                [InlineKeyboardButton("🔙 Main Menu", callback_data="back_to_main")]
            ]
            
        else:
            await query.answer(f"❌ Failed to remove {folder_name}")
            
            success_text = f"""
❌ *FAILED TO REMOVE FOLDER*

🗑️ *Folder:* {folder_name}
📊 *Error:* Could not remove from configuration

🔧 *Try again or check:*
• Folder might already be removed
• Configuration file issues
• Use /menu to refresh

💡 *Contact support if problem persists*
            """
            
            keyboard = [
                [InlineKeyboardButton("🔄 Try Again", callback_data="remove_folder")],
                [InlineKeyboardButton("📁 View Folders", callback_data="view_all_folders")],
                [InlineKeyboardButton("🔙 Main Menu", callback_data="back_to_main")]
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            success_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
