"""
🗂️ Folder Management Operations - View, Remove, Custom paths
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

from ...config.manager import config_manager

class FolderManagementHandler:
    """🗂️ Handle folder management operations (view, remove, custom paths)"""
    
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
                [InlineKeyboardButton("🔙 Back", callback_data="manage_folders")]
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
    
    @staticmethod
    async def add_custom_path(query):
        """📝 Add custom folder path - User friendly version"""
        await query.answer("📂 Choose popular folders")
        
        instruction_text = """
📂 *ADD POPULAR FOLDERS*

🎯 *Quick Add Popular Folders:*

Choose from common Android folders below, or use manual path if needed.

💡 *Popular folders are pre-configured with correct paths*
        """
        
        keyboard = [
            [InlineKeyboardButton("🎵 Music", callback_data="add_folder_music")],
            [InlineKeyboardButton("🎬 Movies", callback_data="add_folder_movies")],
            [InlineKeyboardButton("🎮 Games Data", callback_data="add_folder_games")],
            [InlineKeyboardButton("📷 Camera", callback_data="add_folder_camera")],
            [InlineKeyboardButton("🎙️ Recordings", callback_data="add_folder_recordings")],
            [InlineKeyboardButton("💾 Backups", callback_data="add_folder_backups")],
            [InlineKeyboardButton("📱 Screenshots", callback_data="add_folder_screenshots")],
            [InlineKeyboardButton("📝 Manual Path", callback_data="add_manual_path")],
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
    async def add_manual_path(query):
        """📝 Manual path entry (original method)"""
        await query.answer("📝 Manual path instructions")
        
        instruction_text = """
📝 *MANUAL FOLDER PATH*

🎯 *For advanced users only:*

💡 *Use command format:*
   `/add_folder FolderName /path/to/folder`

📋 *Examples:*
   • `/add_folder MyMusic /storage/emulated/0/Music`
   • `/add_folder Work /storage/emulated/0/Documents/Work`
   • `/add_folder MyApps /storage/emulated/0/Android/data`

⚠️ *Note:* Path must exist on your device

🔄 *Tip:* Use file manager to find exact path
        """
        
        keyboard = [
            [InlineKeyboardButton("📂 Popular Folders", callback_data="add_custom_path")],
            [InlineKeyboardButton("📁 Back to Folders", callback_data="manage_folders")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            instruction_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )