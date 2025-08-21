"""
☁️ Google Drive Handler - Handle Google Drive operations
"""

import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from ..config.manager import config_manager

class GoogleDriveHandler:
    """☁️ Handle Google Drive operations"""
    
    @staticmethod
    async def setup_drive_menu(query):
        """☁️ Show Google Drive setup instructions"""
        setup_text = """
☁️ *SETUP GOOGLE DRIVE*

📎 *Upload credentials file (.json):*

1. Buka: console.cloud.google.com
2. Buat project baru
3. Enable Google Drive API
4. Buat OAuth credentials (Desktop app)
5. Download JSON file
6. Upload file di sini

💡 *Drag & drop file JSON ke chat ini*
        """
        
        keyboard = [
            [InlineKeyboardButton("📖 Detailed Guide", callback_data="drive_guide")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            setup_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def manage_accounts(query):
        """👥 Manage Google Drive accounts"""
        credentials_count = config_manager.count_credentials()
        
        accounts_text = f"""
👥 *GOOGLE DRIVE ACCOUNTS*

📊 *Current Status:*
• Total Accounts: {credentials_count}
• Total Storage: {credentials_count * 15}GB
• Status: {'✅ Ready' if credentials_count > 0 else '⚠️ No accounts'}

🎯 *Account Management:*
        """
        
        keyboard = [
            [InlineKeyboardButton("➕ Add New Account", callback_data="add_new_account")],
            [InlineKeyboardButton("📊 View Usage", callback_data="view_usage")],
            [InlineKeyboardButton("🔧 Manage Accounts", callback_data="manage_account_list")],
            [InlineKeyboardButton("🗑️ Remove Account", callback_data="remove_account")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            accounts_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def view_account_usage(query):
        """📊 View account usage"""
        credentials_count = config_manager.count_credentials()
        
        if credentials_count == 0:
            usage_text = """
📊 *ACCOUNT USAGE*

⚠️ *No Google Drive accounts configured*

🎯 *To add account:*
• Upload credentials JSON file
• Get 15GB free storage per account
• Unlimited accounts supported

💡 *Each Google account provides 15GB free storage.*
            """
            
            keyboard = [
                [InlineKeyboardButton("➕ Add Account", callback_data="setup_drive")],
                [InlineKeyboardButton("🔙 Back", callback_data="manage_accounts")]
            ]
        else:
            usage_text = f"""
📊 *ACCOUNT USAGE*

📈 *Summary:*
• Total Accounts: {credentials_count}
• Total Storage: {credentials_count * 15}GB
• Used: Calculating...
• Available: ~{credentials_count * 15}GB

🗃️ *Account Details:*
            """
            
            # Add individual account info
            for i in range(1, credentials_count + 1):
                usage_text += f"""
*Account {i}:*
• Storage: 15GB
• Status: ✅ Active
• Last backup: Ready
                """
            
            keyboard = [
                [InlineKeyboardButton("🔄 Refresh Usage", callback_data="refresh_usage")],
                [InlineKeyboardButton("➕ Add Account", callback_data="setup_drive")],
                [InlineKeyboardButton("🔙 Back", callback_data="manage_accounts")]
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            usage_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def process_credentials(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """📎 Process uploaded Google Drive credentials"""
        try:
            document = update.message.document
            user_id = update.effective_user.id
            
            if not config_manager.check_permission(user_id):
                await update.message.reply_text("❌ Access denied")
                return
            
            # Check file type
            if not document.file_name.endswith('.json'):
                await update.message.reply_text(
                    "❌ *Invalid file type*\n\n"
                    "📎 *Please upload Google Drive credentials (.json)*",
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            
            # Processing message
            processing_msg = await update.message.reply_text(
                "⏳ *Processing credentials...*", 
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Download and validate
            file_obj = await context.bot.get_file(document.file_id)
            
            # Determine account number
            account_number = config_manager.count_credentials() + 1
            
            # Download to temp for validation
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as tmp:
                await file_obj.download_to_drive(tmp.name)
                
                # Validate JSON
                try:
                    with open(tmp.name, 'r') as f:
                        cred_data = json.load(f)
                    
                    # Check structure
                    if 'installed' not in cred_data:
                        raise ValueError("Missing 'installed' section")
                    
                    if 'client_id' not in cred_data['installed']:
                        raise ValueError("Missing 'client_id'")
                    
                    # Save credentials
                    credentials_path = config_manager.save_credentials(cred_data, account_number)
                    client_id = cred_data['installed']['client_id'][:20] + "..."
                    
                except Exception as e:
                    await processing_msg.edit_text(
                        f"❌ *Invalid credentials file*\n\n"
                        f"*Error:* {str(e)}",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    return
                finally:
                    import os
                    os.unlink(tmp.name)
            
            # Success message
            success_text = f"""
✅ *CREDENTIALS UPLOADED SUCCESSFULLY!*

📊 *Account Details:*
• Account Number: {account_number}
• Client ID: {client_id}
• Status: ✅ Valid

🎉 *Google Drive Setup Complete!*
• Storage: +15GB added
• Total Accounts: {account_number}
• Total Storage: {account_number * 15}GB
            """
            
            keyboard = [
                [InlineKeyboardButton("📁 Add Folders", callback_data="manage_folders")],
                [InlineKeyboardButton("🚀 Start Backup", callback_data="quick_backup")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="back_to_main")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await processing_msg.edit_text(
                success_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
            
        except Exception as e:
            await update.message.reply_text(
                f"❌ *Error processing file*\n\n*Details:* {str(e)}",
                parse_mode=ParseMode.MARKDOWN
            )
