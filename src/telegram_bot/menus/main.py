"""
🏠 Main Menu Handler - Handle main menu operations
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from ..config.manager import config_manager

class MainMenuHandler:
    """🏠 Handle main menu operations"""
    
    @staticmethod
    async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """🏠 Display main menu with status"""
        user_id = update.effective_user.id
        
        if not config_manager.check_permission(user_id):
            await update.message.reply_text("❌ Access denied")
            return
        
        # Get system status
        status = config_manager.get_system_status()
        
        welcome_text = f"""
🤖 *TERMUX BACKUP SYSTEM*
📱 *Android Backup dengan Unlimited Storage*

👤 *User:* {update.effective_user.first_name}
📊 *Status:* {'✅ Ready' if status['credentials_count'] > 0 else '⚠️ Setup Needed'}
🗃️ *Accounts:* {status['credentials_count']} Google Drive
📁 *Folders:* {status['folder_count']} monitored

🎯 *Pilih menu:*
        """
        
        # Create keyboard based on status
        keyboard = []
        
        # Quick actions
        if status['credentials_count'] > 0:
            keyboard.append([
                InlineKeyboardButton("🚀 Quick Backup", callback_data="quick_backup"),
                InlineKeyboardButton("⏸️ Stop", callback_data="stop_backup")
            ])
        else:
            keyboard.append([
                InlineKeyboardButton("⚡ Setup Google Drive", callback_data="setup_drive")
            ])
        
        # Main functions
        keyboard.extend([
            [
                InlineKeyboardButton("👥 Google Drive", callback_data="manage_accounts"),
                InlineKeyboardButton("📁 Folders", callback_data="manage_folders")
            ],
            [
                InlineKeyboardButton("⚙️ Auto-Delete Settings", callback_data="auto_delete_settings"),
                InlineKeyboardButton("📊 Status", callback_data="system_status")
            ],
            [
                InlineKeyboardButton("💾 Manual Backup", callback_data="manual_backup"),
                InlineKeyboardButton("⏰ Schedule", callback_data="schedule_backup")
            ],
            [
                InlineKeyboardButton("📋 Logs", callback_data="view_logs"),
                InlineKeyboardButton("❓ Help", callback_data="help_menu")
            ]
        ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.message:
            await update.message.reply_text(
                welcome_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
        else:
            await update.callback_query.edit_message_text(
                welcome_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
    
    @staticmethod
    async def refresh_main_menu(query):
        """🔄 Refresh main menu"""
        # Create a fake update object for the main menu
        class FakeUpdate:
            def __init__(self, query):
                self.callback_query = query
                self.effective_user = query.from_user
                self.message = None
        
        fake_update = FakeUpdate(query)
        await MainMenuHandler.show_main_menu(fake_update, None)
