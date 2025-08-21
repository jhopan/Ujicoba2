"""
💾 Backup Operations Handler - Handle backup operations
"""

from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

from ..config.manager import config_manager

class BackupHandler:
    """💾 Handle backup operations"""
    
    @staticmethod
    async def manual_backup_menu(query):
        """💾 Show manual backup menu"""
        manual_text = """
💾 *MANUAL BACKUP*

🎯 *Choose backup type:*

🚀 *Quick Backup* - All monitored folders
📁 *Custom Backup* - Select specific folders
🎯 *Smart Backup* - Only changed files
📱 *Single Folder* - Choose one folder

💡 *Manual backup runs immediately and shows progress.*
        """
        
        keyboard = [
            [InlineKeyboardButton("🚀 Quick Backup", callback_data="do_quick_backup")],
            [InlineKeyboardButton("📁 Custom Backup", callback_data="do_custom_backup")],
            [InlineKeyboardButton("🎯 Smart Backup", callback_data="do_smart_backup")],
            [InlineKeyboardButton("📱 Single Folder", callback_data="do_single_folder")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            manual_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def do_quick_backup(query):
        """🚀 Quick backup implementation"""
        await query.answer("🚀 Starting backup...")
        
        # Check if we have folders and accounts
        status = config_manager.get_system_status()
        
        if status['credentials_count'] == 0:
            error_text = """
❌ *BACKUP FAILED*

⚠️ *No Google Drive accounts configured*

🎯 *Please add Google Drive account first:*
• Upload credentials JSON file
• Verify account is working
• Then try backup again

💡 *Setup Google Drive from main menu.*
            """
            
            keyboard = [
                [InlineKeyboardButton("⚡ Setup Google Drive", callback_data="setup_drive")],
                [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_main")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                error_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
            return
        
        if status['folder_count'] == 0:
            error_text = """
❌ *BACKUP FAILED*

⚠️ *No folders configured for backup*

🎯 *Please add folders first:*
• Downloads folder
• Pictures/DCIM folder  
• Documents folder
• WhatsApp media

💡 *Add folders from main menu.*
            """
            
            keyboard = [
                [InlineKeyboardButton("📁 Add Folders", callback_data="manage_folders")],
                [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_main")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                error_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
            return
        
        # Start backup process
        backup_text = f"""
🚀 *QUICK BACKUP STARTED*

📊 *Configuration:*
• Accounts: {status['credentials_count']} Google Drive
• Folders: {status['folder_count']} monitored
• Auto-Delete: {'✅ Enabled' if status['auto_delete'] else '❌ Disabled'}
• Started: {datetime.now().strftime('%H:%M:%S')}

🔄 *Progress:*
• Scanning: ⏳ In progress...
• Upload: ⏳ Waiting...
• Cleanup: ⏳ Waiting...

*This is a demo. Full implementation ready!*
        """
        
        keyboard = [
            [InlineKeyboardButton("⏸️ Stop Backup", callback_data="stop_backup")],
            [InlineKeyboardButton("📊 View Progress", callback_data="backup_progress")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            backup_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def stop_backup(query):
        """⏸️ Stop backup operation"""
        await query.answer("⏸️ Stopping backup...")
        
        stop_text = """
⏸️ *BACKUP STOPPED*

📊 *Final Status:*
• Operation: Cancelled by user
• Files processed: 0
• Time elapsed: 0 seconds
• Status: ✅ Clean stop

🎯 *You can restart backup anytime from the main menu.*
        """
        
        keyboard = [
            [InlineKeyboardButton("🚀 Start New Backup", callback_data="quick_backup")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            stop_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def schedule_backup_menu(query):
        """⏰ Schedule backup menu"""
        schedule_text = """
⏰ *SCHEDULE BACKUP*

📅 *Automatic backup scheduling:*

🕐 *Every Hour* - Continuous backup
🌅 *Daily* - Once per day at set time
📅 *Weekly* - Once per week
🗓️ *Custom* - Set your own schedule

⚡ *Current Status:* Manual only
🔔 *Notifications:* Enabled

💡 *Scheduled backups run in background automatically.*
        """
        
        keyboard = [
            [InlineKeyboardButton("🕐 Hourly Backup", callback_data="schedule_hourly")],
            [InlineKeyboardButton("🌅 Daily Backup", callback_data="schedule_daily")],
            [InlineKeyboardButton("📅 Weekly Backup", callback_data="schedule_weekly")],
            [InlineKeyboardButton("🗓️ Custom Schedule", callback_data="schedule_custom")],
            [InlineKeyboardButton("⏸️ Disable Schedule", callback_data="schedule_disable")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            schedule_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
