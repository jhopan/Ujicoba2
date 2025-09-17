"""
📖 Google Drive Setup Guide - Detailed setup instructions and quick start
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

from ...config.manager import config_manager


class GoogleDriveSetupHandler:
    """📖 Handle Google Drive setup instructions and guides"""
    
    @staticmethod
    async def setup_drive_menu(query):
        """☁️ Show Google Drive main setup menu"""
        await query.answer("☁️ Google Drive")
        
        credentials_count = config_manager.count_credentials()
        
        setup_text = f"""
☁️ *GOOGLE DRIVE BACKUP SYSTEM*

📊 *Current Status:*
• Accounts: {credentials_count}
• Storage: {credentials_count * 15}GB
• Status: {'✅ Ready' if credentials_count > 0 else '⚠️ Setup needed'}

🎯 *What you can do:*

📤 **Backup Files**
• Automatic folder backup
• Real-time file monitoring  
• Multiple account support
• Unlimited storage (15GB per account)

👥 **Account Management**
• Add unlimited Google accounts
• Switch between accounts
• Monitor storage usage
• Remove old accounts

📁 **File Operations**
• Upload/download files
• Browse Google Drive
• Search and organize
• Share files easily

🚀 **Quick Start:**
{f"• Ready to backup! Files: {len(config_manager.get_folder_config())} folders monitored" if credentials_count > 0 else "• Add Google Drive account first"}
        """
        
        if credentials_count == 0:
            keyboard = [
                [InlineKeyboardButton("🚀 Quick Setup (2 mins)", callback_data="show_quick_setup")],
                [InlineKeyboardButton("📖 Detailed Guide", callback_data="show_setup_guide")],
                [InlineKeyboardButton("❓ Setup Help", callback_data="setup_help")],
                [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main")]
            ]
        else:
            keyboard = [
                [InlineKeyboardButton("👥 Manage Accounts", callback_data="manage_accounts")],
                [InlineKeyboardButton("📁 File Operations", callback_data="show_drive_operations")],
                [InlineKeyboardButton("🚀 Quick Backup", callback_data="quick_backup")],
                [InlineKeyboardButton("➕ Add More Accounts", callback_data="add_new_account")],
                [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main")]
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            setup_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def show_setup_guide(query):
        """📖 Show detailed setup guide"""
        await query.answer("📖 Setup guide")
        
        guide_text = """
📖 *GOOGLE DRIVE SETUP GUIDE*

🎯 *Complete step-by-step setup:*

**STEP 1: Google Cloud Console**
• Open: console.cloud.google.com
• Sign in with your Google account
• Click "Create Project" or select existing
• Name your project (e.g., "My Backup Bot")

**STEP 2: Enable Google Drive API**
• Go to "APIs & Services" > "Library"
• Search for "Google Drive API"
• Click on it and press "Enable"
• Wait for activation (30 seconds)

**STEP 3: Create Credentials**
• Go to "APIs & Services" > "Credentials"
• Click "Create Credentials" > "OAuth 2.0 Client ID"
• Choose "Desktop application"
• Name it (e.g., "Backup Bot")
• Click "Create"

**STEP 4: Download JSON**
• Click download button (📥) next to your credential
• Save the JSON file to your device
• Keep this file safe and secure

**STEP 5: Upload to Bot**
• Return to this chat
• Drag & drop the JSON file here
• Bot will process and activate your account
• Setup complete! 🎉

💡 *Need help?* Use Quick Setup for simplified steps.
        """
        
        keyboard = [
            [InlineKeyboardButton("⚡ Quick Setup Instead", callback_data="show_quick_setup")],
            [InlineKeyboardButton("❓ Common Issues", callback_data="setup_troubleshooting")],
            [InlineKeyboardButton("📱 Mobile Setup", callback_data="mobile_setup_guide")],
            [InlineKeyboardButton("☁️ Back to Google Drive", callback_data="setup_drive")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            guide_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def show_quick_setup(query):
        """⚡ Show quick setup instructions"""
        await query.answer("⚡ Quick setup")
        
        account_count = config_manager.count_credentials()
        next_account = account_count + 1
        
        quick_text = f"""
⚡ *QUICK SETUP - 2 MINUTES*

🎯 *Setting up Account #{next_account}:*

**🔗 Direct Links:**
1. Open: bit.ly/gcp-console
2. Click: "New Project" → Name it → "Create"
3. Click: "Enable APIs" → Search "Drive" → Enable
4. Click: "Create Credentials" → "OAuth 2.0"
5. Choose: "Desktop app" → Name it → "Create"
6. Click: Download (📥) → Save JSON file

**📱 Upload Here:**
• Drag JSON file to this chat
• Bot validates automatically
• Account ready in seconds!

💡 *Benefits:*
• +15GB storage per account
• Unlimited accounts
• Automatic backups
• File sharing & sync

⚠️ *Important:*
• Use your own Google account
• Keep JSON file secure
• Don't share credentials

🚀 *After upload: Ready to backup!*
        """
        
        keyboard = [
            [InlineKeyboardButton("📖 Need Detailed Guide?", callback_data="show_setup_guide")],
            [InlineKeyboardButton("📱 Mobile Setup Tips", callback_data="mobile_setup_guide")],
            [InlineKeyboardButton("❓ Common Problems", callback_data="setup_troubleshooting")],
            [InlineKeyboardButton("☁️ Back to Google Drive", callback_data="setup_drive")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            quick_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def setup_help(query):
        """❓ Show setup help and FAQ"""
        await query.answer("❓ Setup help")
        
        help_text = """
❓ *SETUP HELP & FAQ*

🤔 **Common Questions:**

**Q: Is this safe?**
A: Yes! You create credentials in YOUR Google account. Bot only accesses what you authorize.

**Q: What data is stored?**
A: Only credentials file you upload. No passwords or personal data stored.

**Q: How many accounts can I add?**
A: Unlimited! Each Google account gives 15GB free storage.

**Q: Will this affect my Google Drive?**
A: No! Bot creates separate backup folders. Your existing files are untouched.

**Q: Can I remove accounts later?**
A: Yes! Remove accounts anytime from account management.

**Q: What happens to my files if I remove the bot?**
A: Files stay in your Google Drive. Bot only manages backup copies.

🔧 **Technical Requirements:**
• Active Google account
• Internet connection
• JSON credentials file
• About 2 minutes setup time

🆘 **Need More Help?**
• Try Quick Setup first
• Check troubleshooting guide  
• Contact support if stuck
        """
        
        keyboard = [
            [InlineKeyboardButton("⚡ Try Quick Setup", callback_data="show_quick_setup")],
            [InlineKeyboardButton("🛠️ Troubleshooting", callback_data="setup_troubleshooting")],
            [InlineKeyboardButton("📖 Detailed Guide", callback_data="show_setup_guide")],
            [InlineKeyboardButton("☁️ Back to Google Drive", callback_data="setup_drive")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def setup_troubleshooting(query):
        """🛠️ Setup troubleshooting guide"""
        await query.answer("🛠️ Troubleshooting")
        
        troubleshooting_text = """
🛠️ *SETUP TROUBLESHOOTING*

❌ **Common Issues & Solutions:**

**1. "Project creation failed"**
• ✅ Make sure you're signed in to Google
• ✅ Try different project name
• ✅ Check internet connection
• ✅ Use desktop browser (not mobile)

**2. "Can't find Google Drive API"**
• ✅ Search for "Google Drive API" (exact)
• ✅ Make sure project is selected
• ✅ Refresh the page
• ✅ Try different browser

**3. "OAuth error"**
• ✅ Choose "Desktop application" (not web)
• ✅ Don't configure redirect URIs
• ✅ Use simple name without spaces
• ✅ Try creating new credentials

**4. "Invalid JSON file"**
• ✅ Download fresh JSON from Google
• ✅ Don't edit the file
• ✅ Check file extension is .json
• ✅ Ensure complete download

**5. "Permission denied"**
• ✅ Use your own Google account
• ✅ Make sure you own the project
• ✅ Check billing is not required
• ✅ Verify API is enabled

💡 **Pro Tips:**
• Use Chrome/Firefox for best results
• Clear browser cache if stuck
• Try incognito mode
• Double-check each step
        """
        
        keyboard = [
            [InlineKeyboardButton("⚡ Start Fresh Setup", callback_data="show_quick_setup")],
            [InlineKeyboardButton("📱 Mobile Setup Tips", callback_data="mobile_setup_guide")],
            [InlineKeyboardButton("❓ More Help", callback_data="setup_help")],
            [InlineKeyboardButton("☁️ Back to Google Drive", callback_data="setup_drive")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            troubleshooting_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def mobile_setup_guide(query):
        """📱 Mobile setup tips"""
        await query.answer("📱 Mobile setup")
        
        mobile_text = """
📱 *MOBILE SETUP GUIDE*

📞 **Setup from Android/iPhone:**

**Option 1: Mobile Browser** (Recommended)
• Open Chrome/Safari on your phone
• Go to: console.cloud.google.com
• Follow same steps as desktop
• Download JSON to phone
• Share/upload JSON file to this chat

**Option 2: Desktop + File Transfer**
• Setup on computer/laptop
• Download JSON file
• Transfer to phone (email/cloud/USB)
• Upload JSON file to this chat

**Option 3: Cloud Storage**
• Setup on any device with browser
• Save JSON to Google Drive/Dropbox
• Download on phone from cloud
• Upload to this chat

📱 **Mobile Browser Tips:**
• Use "Desktop mode" if needed
• Zoom in/out for better navigation
• Download files go to "Downloads" folder
• Use file manager to find JSON

📨 **File Transfer Methods:**
• Email JSON to yourself
• Upload to Google Drive → download
• Use messaging apps
• USB cable to computer

✅ **Best Practice:**
• Setup on computer if possible
• Transfer JSON securely
• Delete JSON after upload
• Test backup immediately
        """
        
        keyboard = [
            [InlineKeyboardButton("⚡ Quick Setup Steps", callback_data="show_quick_setup")],
            [InlineKeyboardButton("📖 Detailed Guide", callback_data="show_setup_guide")],
            [InlineKeyboardButton("🛠️ Troubleshooting", callback_data="setup_troubleshooting")],
            [InlineKeyboardButton("☁️ Back to Google Drive", callback_data="setup_drive")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            mobile_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def setup_troubleshooting(query):
        """🛠️ Setup troubleshooting guide (alias for setup_troubleshooting method)"""
        await GoogleDriveSetupHandler.setup_troubleshooting(query)
    
    @staticmethod
    async def setup_help(query):
        """❓ Setup help and FAQ (alias for setup_help method)"""
        await GoogleDriveSetupHandler.setup_help(query)