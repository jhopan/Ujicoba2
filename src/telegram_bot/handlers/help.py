"""
❓ Help Handler - Provide help and documentation
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

class HelpHandler:
    """❓ Handle help and documentation"""
    
    @staticmethod
    async def help_menu(query):
        """❓ Show help menu"""
        help_text = """
❓ *HELP & DOCUMENTATION*

🎯 *Welcome to Termux Backup Bot!*

This bot automatically backs up your Android files to Google Drive. Perfect for protecting your photos, downloads, and documents.

📚 *Help Topics:*
🚀 Getting Started Guide
📱 Android Setup  
⚡ Google Drive Setup
📁 Folder Management
🔄 Backup Operations
⚙️ Settings & Config
🛠️ Troubleshooting
📊 Monitoring & Logs

💡 *Quick Start: Setup → Folders → Backup!*
        """
        
        keyboard = [
            [InlineKeyboardButton("🚀 Getting Started", callback_data="help_getting_started")],
            [InlineKeyboardButton("📱 Android Setup", callback_data="help_android")],
            [InlineKeyboardButton("⚡ Google Drive", callback_data="help_drive")],
            [InlineKeyboardButton("📁 Folders", callback_data="help_folders")],
            [InlineKeyboardButton("🔄 Backup", callback_data="help_backup")],
            [InlineKeyboardButton("⚙️ Settings", callback_data="help_settings")],
            [InlineKeyboardButton("🛠️ Troubleshooting", callback_data="help_troubleshooting")],
            [InlineKeyboardButton("📊 Monitoring", callback_data="help_monitoring")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def getting_started(query):
        """🚀 Getting started guide"""
        guide_text = """
🚀 *GETTING STARTED GUIDE*

🎯 *Step-by-step setup process:*

**1. 📱 Setup Android (Required)**
• Install Termux from F-Droid
• Grant storage permissions
• Install Python and dependencies
• This step is usually done during installation

**2. ⚡ Setup Google Drive (Required)**
• Go to Google Cloud Console
• Create project and enable Drive API
• Download credentials JSON
• Upload to bot using Setup Google Drive

**3. 📁 Configure Folders (Required)**
• Choose folders to backup
• Downloads, Pictures, Documents, WhatsApp
• Set auto-delete preferences
• Configure monitoring settings

**4. 🚀 Start Backup (Ready!)**
• Run manual backup to test
• Setup automatic scheduling
• Monitor progress and logs
• Enjoy automatic protection!

*Each step has detailed help in respective sections.*
        """
        
        keyboard = [
            [InlineKeyboardButton("📱 Android Setup Help", callback_data="help_android")],
            [InlineKeyboardButton("⚡ Google Drive Help", callback_data="help_drive")],
            [InlineKeyboardButton("📁 Folder Setup Help", callback_data="help_folders")],
            [InlineKeyboardButton("🚀 Start Setup Now", callback_data="setup_drive")],
            [InlineKeyboardButton("🔙 Back", callback_data="show_help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            guide_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def android_help(query):
        """📱 Android setup help"""
        android_text = """
📱 *ANDROID SETUP HELP*

🎯 *Termux Installation:*

**1. Install Termux**
• Download from F-Droid (recommended)
• Or from GitHub releases
• NOT from Google Play (outdated)

**2. Grant Permissions**
```
termux-setup-storage
```
• Allow storage access when prompted
• This gives access to your files

**3. Install Dependencies**
```
pkg update && pkg upgrade
pkg install python git
pip install python-telegram-bot google-api-python-client
```

**4. Clone and Setup**
```
git clone [repository]
cd [project-folder]
chmod +x scripts/setup_termux.sh
./scripts/setup_termux.sh
```

🛠️ *Common Issues:*
• Permission denied → Run termux-setup-storage
• Python not found → pkg install python
• Git not found → pkg install git

*Most setup is automated by our install scripts!*
        """
        
        keyboard = [
            [InlineKeyboardButton("🔧 Troubleshooting", callback_data="help_troubleshooting")],
            [InlineKeyboardButton("⚡ Next: Google Drive", callback_data="help_drive")],
            [InlineKeyboardButton("📋 Installation Guide", callback_data="installation_guide")],
            [InlineKeyboardButton("🔙 Back", callback_data="show_help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            android_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def drive_help(query):
        """⚡ Google Drive setup help"""
        drive_text = """
⚡ *GOOGLE DRIVE SETUP HELP*

🎯 *Step-by-step Google Cloud setup:*

**1. Create Google Cloud Project**
• Go to console.cloud.google.com
• Create new project or select existing
• Name it something like "Termux Backup"

**2. Enable Google Drive API**
• Go to APIs & Services → Library
• Search "Google Drive API"
• Click Enable

**3. Create Credentials**
• APIs & Services → Credentials
• Create Credentials → Service Account
• Download JSON key file

**4. Share Drive Folder (Optional)**
• Create folder in Google Drive
• Share with service account email
• Copy service account email from JSON

**5. Upload to Bot**
• Use "Setup Google Drive" in main menu
• Send the JSON file to bot
• Bot will verify and save credentials

🔐 *Security Notes:*
• Keep credentials file secure
• Don't share with others
• Bot encrypts stored credentials

*Need the JSON file? Follow steps 1-3 above!*
        """
        
        keyboard = [
            [InlineKeyboardButton("⚡ Setup Google Drive", callback_data="setup_drive")],
            [InlineKeyboardButton("🔐 Security Info", callback_data="security_info")],
            [InlineKeyboardButton("📁 Next: Folders", callback_data="help_folders")],
            [InlineKeyboardButton("🔙 Back", callback_data="show_help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            drive_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def folders_help(query):
        """📁 Folder management help"""
        folders_text = """
📁 *FOLDER MANAGEMENT HELP*

🎯 *Understanding Folder Types:*

**📱 Downloads**
• Path: /storage/emulated/0/Download
• Contains: Browser downloads, app files
• Size: Usually large files
• Recommendation: Enable auto-delete after backup

**📸 Pictures/DCIM**
• Path: /storage/emulated/0/DCIM
• Contains: Camera photos, screenshots
• Size: Can be very large
• Recommendation: Keep originals, backup regularly

**📄 Documents**
• Path: /storage/emulated/0/Documents
• Contains: PDF files, text documents
• Size: Usually small
• Recommendation: Keep all, backup frequently

**💬 WhatsApp Media**
• Path: /storage/emulated/0/WhatsApp/Media
• Contains: Shared photos, videos, documents
• Size: Can be very large
• Recommendation: Auto-delete old media

🔧 *Folder Configuration:*
• Enable/disable monitoring per folder
• Set auto-delete preferences
• Configure backup frequency
• Set file type filters
        """
        
        keyboard = [
            [InlineKeyboardButton("📁 Configure Folders", callback_data="manage_folders")],
            [InlineKeyboardButton("🧹 Auto-Delete Settings", callback_data="settings_cleanup")],
            [InlineKeyboardButton("🔄 Next: Backup", callback_data="help_backup")],
            [InlineKeyboardButton("🔙 Back", callback_data="show_help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            folders_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def backup_help(query):
        """🔄 Backup operations help"""
        backup_text = """
🔄 *BACKUP OPERATIONS HELP*

🎯 *Types of Backup:*

**🚀 Quick Backup**
• Backs up all configured folders
• Uses all available Google Drive accounts
• Fastest option for complete backup
• Runs immediately

**📁 Custom Backup**
• Choose specific folders
• Select which accounts to use
• Useful for targeted backups
• More control over process

**🎯 Smart Backup**
• Only backs up changed/new files
• Skips already uploaded files
• Saves time and bandwidth
• Best for regular use

**📱 Single Folder**
• Backup just one folder
• Quick for testing
• Good for urgent files
• Minimal resource usage

**⏰ Scheduled Backup**
• Automatic at set times
• Hourly, daily, weekly options
• Runs in background
• Set and forget convenience

🔧 *Backup Features:*
• Progress monitoring
• Error recovery
• Multiple account support
• Bandwidth management
        """
        
        keyboard = [
            [InlineKeyboardButton("🚀 Start Backup", callback_data="quick_backup")],
            [InlineKeyboardButton("⏰ Schedule Backup", callback_data="schedule_backup")],
            [InlineKeyboardButton("⚙️ Next: Settings", callback_data="help_settings")],
            [InlineKeyboardButton("🔙 Back", callback_data="show_help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            backup_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def troubleshooting_help(query):
        """🛠️ Troubleshooting help"""
        troubleshooting_text = """
🛠️ *TROUBLESHOOTING GUIDE*

🚨 *Common Issues & Solutions:*

**❌ "Permission denied" errors**
• Run: `termux-setup-storage`
• Restart Termux app
• Check Android app permissions

**❌ "Google Drive API quota exceeded"**
• Wait 24 hours for quota reset
• Add more Google Drive accounts
• Contact Google Cloud support

**❌ "No space left on device"**
• Clear Termux cache
• Enable auto-delete after backup
• Move files to external storage

**❌ "Network connection failed"**
• Check internet connection
• Try different network (WiFi/mobile)
• Restart router/modem

**❌ "Bot not responding"**
• Check bot is running: `ps aux | grep python`
• Restart bot: `./scripts/start_bot.sh`
• Check logs: `tail -f logs/bot.log`

**❌ "Credentials invalid"**
• Re-download JSON from Google Cloud
• Upload new credentials to bot
• Check service account permissions

🔧 *Debug Tools:*
• Enable debug mode in Settings
• Check logs in Logs & Monitoring
• Run connectivity tests
        """
        
        keyboard = [
            [InlineKeyboardButton("🔧 Enable Debug Mode", callback_data="enable_debug")],
            [InlineKeyboardButton("📊 Check Logs", callback_data="show_logs")],
            [InlineKeyboardButton("⚙️ Check Settings", callback_data="show_settings")],
            [InlineKeyboardButton("🔙 Back", callback_data="show_help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            troubleshooting_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
