"""
⚙️ Settings Handler - Manage bot settings and configuration
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

from ..config.manager import config_manager

class SettingsHandler:
    """⚙️ Handle settings and configuration"""
    
    @staticmethod
    async def settings_menu(query):
        """⚙️ Show settings menu"""
        status = config_manager.get_system_status()
        
        settings_text = f"""
⚙️ *SETTINGS & CONFIGURATION*

🎯 *Current Configuration:*
• Google Drive: {status['credentials_count']} accounts
• Folders: {status['folder_count']} monitored
• Auto-Delete: {'✅ Enabled' if status['auto_delete'] else '❌ Disabled'}
• Notifications: {'✅ Enabled' if status['notifications'] else '❌ Disabled'}
• Debug Mode: {'✅ Enabled' if status['debug_mode'] else '❌ Disabled'}

🔧 *Available Settings:*
📂 Folder Configuration
🔔 Notification Settings  
🧹 Cleanup Settings
🔐 Security Settings
⚡ Performance Settings
        """
        
        keyboard = [
            [InlineKeyboardButton("📂 Folder Settings", callback_data="settings_folders")],
            [InlineKeyboardButton("🔔 Notifications", callback_data="settings_notifications")],
            [InlineKeyboardButton("🧹 Cleanup Settings", callback_data="settings_cleanup")],
            [InlineKeyboardButton("🔐 Security", callback_data="settings_security")],
            [InlineKeyboardButton("⚡ Performance", callback_data="settings_performance")],
            [InlineKeyboardButton("🔄 Reset All", callback_data="settings_reset")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            settings_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def folder_settings(query):
        """📂 Folder configuration settings"""
        settings_text = """
📂 *FOLDER SETTINGS*

🎯 *Monitoring Configuration:*

📱 *Downloads Folder*
• Path: /storage/emulated/0/Download
• Status: ✅ Active
• Auto-backup: ✅ Enabled

📸 *Pictures/DCIM*
• Path: /storage/emulated/0/DCIM
• Status: ✅ Active  
• Auto-backup: ✅ Enabled

📄 *Documents*
• Path: /storage/emulated/0/Documents
• Status: ❌ Not configured
• Auto-backup: ❌ Disabled

💬 *WhatsApp Media*
• Path: /storage/emulated/0/WhatsApp/Media
• Status: ❌ Not configured
• Auto-backup: ❌ Disabled
        """
        
        keyboard = [
            [InlineKeyboardButton("📱 Configure Downloads", callback_data="config_downloads")],
            [InlineKeyboardButton("📸 Configure Pictures", callback_data="config_pictures")],
            [InlineKeyboardButton("📄 Configure Documents", callback_data="config_documents")],
            [InlineKeyboardButton("💬 Configure WhatsApp", callback_data="config_whatsapp")],
            [InlineKeyboardButton("🔄 Scan All Folders", callback_data="scan_all_folders")],
            [InlineKeyboardButton("🔙 Back", callback_data="show_settings")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            settings_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def notification_settings(query):
        """🔔 Notification settings"""
        settings_text = """
🔔 *NOTIFICATION SETTINGS*

📢 *Current Configuration:*

✅ *Backup Complete* - When backup finishes
✅ *Backup Failed* - When errors occur
✅ *Storage Full* - When Drive storage is low
✅ *New Files* - When new files detected
❌ *Debug Messages* - Development info
❌ *Hourly Status* - Regular status updates

🎯 *Notification Types:*
• Success messages: Important completions
• Error alerts: Problems that need attention
• Status updates: Regular progress info
• Debug info: Technical details
        """
        
        keyboard = [
            [InlineKeyboardButton("✅ Toggle Backup Alerts", callback_data="toggle_backup_alerts")],
            [InlineKeyboardButton("✅ Toggle Error Alerts", callback_data="toggle_error_alerts")],
            [InlineKeyboardButton("❌ Toggle Status Updates", callback_data="toggle_status_updates")],
            [InlineKeyboardButton("❌ Toggle Debug Mode", callback_data="toggle_debug_mode")],
            [InlineKeyboardButton("🔕 Disable All", callback_data="disable_all_notifications")],
            [InlineKeyboardButton("🔔 Enable All", callback_data="enable_all_notifications")],
            [InlineKeyboardButton("🔙 Back", callback_data="show_settings")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            settings_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def cleanup_settings(query):
        """🧹 Cleanup and auto-delete settings"""
        settings_text = """
🧹 *CLEANUP SETTINGS*

🎯 *Auto-Delete Configuration:*

📱 *After Upload:*
• Downloads: ❌ Keep files
• Pictures: ❌ Keep files
• Documents: ❌ Keep files
• WhatsApp: ❌ Keep files

⏰ *Time-Based Cleanup:*
• Delete after: Not configured
• Min file age: Not set
• Keep recent: All files

💾 *Storage Management:*
• Free space threshold: 1GB
• Emergency cleanup: ✅ Enabled
• Backup before delete: ✅ Enabled

⚠️ *CAUTION: Auto-delete permanently removes files!*
        """
        
        keyboard = [
            [InlineKeyboardButton("📱 Downloads Auto-Delete", callback_data="autodel_downloads")],
            [InlineKeyboardButton("📸 Pictures Auto-Delete", callback_data="autodel_pictures")],
            [InlineKeyboardButton("📄 Documents Auto-Delete", callback_data="autodel_documents")],
            [InlineKeyboardButton("💬 WhatsApp Auto-Delete", callback_data="autodel_whatsapp")],
            [InlineKeyboardButton("⏰ Time Settings", callback_data="autodel_time")],
            [InlineKeyboardButton("🛡️ Safety Settings", callback_data="autodel_safety")],
            [InlineKeyboardButton("🔙 Back", callback_data="show_settings")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            settings_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def security_settings(query):
        """🔐 Security settings"""
        settings_text = """
🔐 *SECURITY SETTINGS*

🛡️ *Access Control:*
• Bot Owner: You (verified)
• Admin Users: 1 user
• Guest Access: ❌ Disabled
• Rate Limiting: ✅ Enabled

🔑 *Credentials Security:*
• Google Drive: 0 accounts loaded
• Encryption: ✅ Enabled
• Auto-lock: ✅ After 1 hour
• Backup credentials: ✅ Enabled

📊 *Audit & Logging:*
• Command logging: ✅ Enabled
• Error tracking: ✅ Enabled
• Usage statistics: ✅ Enabled
• Log retention: 7 days

⚠️ *Keep your credentials secure!*
        """
        
        keyboard = [
            [InlineKeyboardButton("👤 User Management", callback_data="security_users")],
            [InlineKeyboardButton("🔑 Credential Security", callback_data="security_credentials")],
            [InlineKeyboardButton("📊 Audit Settings", callback_data="security_audit")],
            [InlineKeyboardButton("🔒 Lock Bot Now", callback_data="security_lock")],
            [InlineKeyboardButton("🔄 Reset Security", callback_data="security_reset")],
            [InlineKeyboardButton("🔙 Back", callback_data="show_settings")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            settings_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def performance_settings(query):
        """⚡ Performance settings"""
        settings_text = """
⚡ *PERFORMANCE SETTINGS*

🚀 *Upload Configuration:*
• Concurrent uploads: 3 files
• Chunk size: 8MB
• Retry attempts: 3 times
• Timeout: 30 seconds

📊 *Monitoring Frequency:*
• File scan interval: 5 minutes
• Status check: 1 minute
• Cleanup check: 1 hour
• Health check: 5 minutes

💾 *Resource Management:*
• Memory limit: 512MB
• CPU throttling: ✅ Enabled
• Battery optimization: ✅ Enabled
• Network adaptation: ✅ Enabled

📱 *Mobile Optimization:*
• Background processing: ✅ Enabled
• Data saver mode: ❌ Disabled
• WiFi only uploads: ❌ Disabled
        """
        
        keyboard = [
            [InlineKeyboardButton("🚀 Upload Settings", callback_data="perf_upload")],
            [InlineKeyboardButton("📊 Monitoring", callback_data="perf_monitoring")],
            [InlineKeyboardButton("💾 Resources", callback_data="perf_resources")],
            [InlineKeyboardButton("📱 Mobile Opts", callback_data="perf_mobile")],
            [InlineKeyboardButton("⚡ Optimize Now", callback_data="perf_optimize")],
            [InlineKeyboardButton("🔙 Back", callback_data="show_settings")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            settings_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
