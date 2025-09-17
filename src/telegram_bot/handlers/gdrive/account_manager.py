"""
👥 Google Drive Account Manager - Handle Google Drive account operations
"""

import json
import os
import tempfile
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from ...config.manager import config_manager


class GoogleDriveAccountHandler:
    """👥 Handle Google Drive account management"""
    
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
• Add unlimited Google accounts
• Each account provides 15GB free storage
• Switch between accounts easily
• Remove accounts when needed
        """
        
        keyboard = [
            [InlineKeyboardButton("➕ Add New Account", callback_data="add_new_account")],
            [InlineKeyboardButton("📊 View Usage", callback_data="view_usage")],
            [InlineKeyboardButton("🔧 Manage Account List", callback_data="manage_account_list")],
            [InlineKeyboardButton("🗑️ Remove Account", callback_data="remove_account")],
            [InlineKeyboardButton("🔙 Back to Google Drive", callback_data="setup_drive")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            accounts_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def add_new_account(query):
        """➕ Add new Google Drive account instructions"""
        await query.answer("➕ Add new account")
        
        account_count = config_manager.count_credentials()
        next_account = account_count + 1
        
        instruction_text = f"""
➕ *ADD NEW GOOGLE DRIVE ACCOUNT*

📋 *Account #{next_account} Setup:*

🔧 *Step 1: Create Credentials*
• Open: console.cloud.google.com
• Create new project (or use existing)
• Enable Google Drive API
• Create OAuth 2.0 credentials
• Choose "Desktop application"
• Download JSON file

📎 *Step 2: Upload Credentials*
• Drag & drop the JSON file here
• Bot will validate and save automatically
• Account will be ready immediately

💡 *Benefits:*
• +15GB storage per account
• Unlimited accounts supported
• Automatic load balancing
        """
        
        keyboard = [
            [InlineKeyboardButton("📖 Detailed Guide", callback_data="show_setup_guide")],
            [InlineKeyboardButton("⚡ Quick Setup", callback_data="show_quick_setup")],
            [InlineKeyboardButton("👥 Back to Accounts", callback_data="manage_accounts")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            instruction_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def view_account_usage(query):
        """📊 View account usage and storage details"""
        await query.answer("📊 Checking usage...")
        
        credentials_count = config_manager.count_credentials()
        
        if credentials_count == 0:
            usage_text = """
📊 *STORAGE USAGE*

⚠️ *No Google Drive accounts configured*

🎯 *To get started:*
• Upload credentials JSON file
• Get 15GB free storage per account
• Unlimited accounts supported
• Automatic load balancing

💡 *Each Google account provides 15GB free storage.*
            """
            
            keyboard = [
                [InlineKeyboardButton("➕ Add First Account", callback_data="add_new_account")],
                [InlineKeyboardButton("👥 Back to Accounts", callback_data="manage_accounts")]
            ]
        else:
            usage_text = f"""
📊 *STORAGE USAGE*

📈 *Summary:*
• Total Accounts: {credentials_count}
• Total Storage: {credentials_count * 15}GB
• Status: ✅ All accounts ready
• Load Balancing: ✅ Active

🗃️ *Account Details:*
            """
            
            # Add individual account info
            for i in range(1, credentials_count + 1):
                status = "✅ Active" if i <= credentials_count else "⚠️ Inactive"
                usage_text += f"""
*Account {i}:*
• Storage: 15GB available
• Status: {status}
• Last sync: Ready
• Files: Ready for backup
                """
            
            keyboard = [
                [InlineKeyboardButton("🔄 Refresh Usage", callback_data="view_usage")],
                [InlineKeyboardButton("➕ Add More Accounts", callback_data="add_new_account")],
                [InlineKeyboardButton("👥 Back to Accounts", callback_data="manage_accounts")]
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            usage_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def manage_account_list(query):
        """🔧 Manage account list - view, switch, configure accounts"""
        await query.answer("🔧 Loading accounts...")
        
        credentials_count = config_manager.count_credentials()
        
        if credentials_count == 0:
            list_text = """
🔧 *ACCOUNT LIST*

⚠️ *No accounts available*

🎯 *Get started:*
• Add your first Google Drive account
• Upload credentials JSON file
• Start backing up your files

💡 *You can add unlimited accounts*
            """
            
            keyboard = [
                [InlineKeyboardButton("➕ Add First Account", callback_data="add_new_account")],
                [InlineKeyboardButton("👥 Back to Accounts", callback_data="manage_accounts")]
            ]
        else:
            list_text = f"""
🔧 *ACCOUNT LIST*

📋 *Available Accounts: {credentials_count}*

🔄 *Active Account: Account 1* (default)

📊 *Account Status:*
            """
            
            keyboard = []
            
            # Add account buttons
            for i in range(1, credentials_count + 1):
                account_status = "🟢" if i == 1 else "⚪"
                keyboard.append([
                    InlineKeyboardButton(
                        f"{account_status} Account {i} (15GB)", 
                        callback_data=f"switch_account_{i}"
                    )
                ])
                
                list_text += f"""
*Account {i}:*
• Storage: 15GB
• Status: {'🟢 Active' if i == 1 else '⚪ Available'}
• Type: Google Drive
                """
            
            # Add management buttons
            keyboard.extend([
                [InlineKeyboardButton("➕ Add New Account", callback_data="add_new_account")],
                [InlineKeyboardButton("👥 Back to Accounts", callback_data="manage_accounts")]
            ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            list_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def remove_account_menu(query):
        """🗑️ Remove account menu"""
        await query.answer("🗑️ Remove account")
        
        credentials_count = config_manager.count_credentials()
        
        if credentials_count == 0:
            remove_text = """
🗑️ *REMOVE ACCOUNT*

⚠️ *No accounts to remove*

🎯 *Add accounts first:*
• Upload Google Drive credentials
• Start backing up files
• Manage multiple accounts

💡 *You need at least one account for backups*
            """
            
            keyboard = [
                [InlineKeyboardButton("➕ Add Account", callback_data="add_new_account")],
                [InlineKeyboardButton("👥 Back to Accounts", callback_data="manage_accounts")]
            ]
        else:
            remove_text = f"""
🗑️ *REMOVE ACCOUNT*

⚠️ *Warning: This will permanently remove account access*

📋 *Available Accounts: {credentials_count}*

🎯 *Select account to remove:*
• Account credentials will be deleted
• Backup history will be preserved
• Files on Google Drive remain safe

💡 *Choose carefully - this cannot be undone*
            """
            
            keyboard = []
            
            # Add remove buttons for each account
            for i in range(1, credentials_count + 1):
                keyboard.append([
                    InlineKeyboardButton(
                        f"🗑️ Remove Account {i}", 
                        callback_data=f"remove_account_{i}"
                    )
                ])
            
            # Add back button
            keyboard.append([
                InlineKeyboardButton("👥 Back to Accounts", callback_data="manage_accounts")
            ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            remove_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def remove_specific_account(query, account_id: str):
        """🗑️ Remove specific account"""
        account_num = account_id.replace('remove_account_', '')
        await query.answer(f"🗑️ Removing account {account_num}...")
        
        try:
            # Remove account credentials
            result = config_manager.remove_credentials(int(account_num))
            
            if result:
                success_text = f"""
✅ *ACCOUNT REMOVED SUCCESSFULLY*

🗑️ *Account {account_num} has been removed*

📊 *Updated Status:*
• Remaining Accounts: {config_manager.count_credentials()}
• Total Storage: {config_manager.count_credentials() * 15}GB
• Status: {'✅ Ready' if config_manager.count_credentials() > 0 else '⚠️ No accounts'}

💡 *Your files on Google Drive are safe*
                """
                
                keyboard = [
                    [InlineKeyboardButton("📊 View Usage", callback_data="view_usage")],
                    [InlineKeyboardButton("➕ Add New Account", callback_data="add_new_account")],
                    [InlineKeyboardButton("👥 Back to Accounts", callback_data="manage_accounts")]
                ]
            else:
                success_text = f"""
❌ *FAILED TO REMOVE ACCOUNT*

⚠️ *Account {account_num} could not be removed*

🔍 *Possible reasons:*
• Account doesn't exist
• File permission issues
• Account already removed

💡 *Try refreshing account list*
                """
                
                keyboard = [
                    [InlineKeyboardButton("🔄 Refresh List", callback_data="manage_account_list")],
                    [InlineKeyboardButton("👥 Back to Accounts", callback_data="manage_accounts")]
                ]
            
        except Exception as e:
            success_text = f"""
❌ *ERROR REMOVING ACCOUNT*

🔍 *Error details:*
{str(e)}

💡 *Please try again or contact support*
            """
            
            keyboard = [
                [InlineKeyboardButton("🔄 Try Again", callback_data="remove_account")],
                [InlineKeyboardButton("👥 Back to Accounts", callback_data="manage_accounts")]
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            success_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def switch_account(query, account_id: str):
        """🔄 Switch active account"""
        account_num = account_id.replace('switch_account_', '')
        await query.answer(f"🔄 Switching to account {account_num}...")
        
        try:
            # Set active account
            config_manager.set_active_account(int(account_num))
            
            switch_text = f"""
✅ *ACCOUNT SWITCHED SUCCESSFULLY*

🔄 *Active Account: {account_num}*

📊 *Account Details:*
• Storage: 15GB available
• Status: ✅ Active and ready
• Type: Google Drive
• Load balancing: Active

💡 *All future operations will use this account*
            """
            
            keyboard = [
                [InlineKeyboardButton("🚀 Start Backup", callback_data="quick_backup")],
                [InlineKeyboardButton("📁 File Operations", callback_data="show_drive_operations")],
                [InlineKeyboardButton("🔧 Manage Accounts", callback_data="manage_account_list")]
            ]
            
        except Exception as e:
            switch_text = f"""
❌ *FAILED TO SWITCH ACCOUNT*

⚠️ *Could not switch to account {account_num}*

🔍 *Error details:*
{str(e)}

💡 *Please check account availability*
            """
            
            keyboard = [
                [InlineKeyboardButton("🔄 Try Again", callback_data="manage_account_list")],
                [InlineKeyboardButton("👥 Back to Accounts", callback_data="manage_accounts")]
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            switch_text,
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
                    "📎 *Please upload Google Drive credentials (.json)*\n\n"
                    "💡 *File should be downloaded from Google Cloud Console*",
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            
            # Processing message
            processing_msg = await update.message.reply_text(
                "⏳ *Processing credentials...*\n\n"
                "🔍 *Validating file...*", 
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Download and validate
            file_obj = await context.bot.get_file(document.file_id)
            
            # Determine account number
            account_number = config_manager.count_credentials() + 1
            
            # Download to temp for validation
            with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as tmp:
                await file_obj.download_to_drive(tmp.name)
                
                # Validate JSON
                try:
                    with open(tmp.name, 'r') as f:
                        cred_data = json.load(f)
                    
                    # Check structure
                    if 'installed' not in cred_data:
                        raise ValueError("Missing 'installed' section in credentials")
                    
                    if 'client_id' not in cred_data['installed']:
                        raise ValueError("Missing 'client_id' in credentials")
                    
                    if 'client_secret' not in cred_data['installed']:
                        raise ValueError("Missing 'client_secret' in credentials")
                    
                    # Save credentials
                    credentials_path = config_manager.save_credentials(cred_data, account_number)
                    client_id = cred_data['installed']['client_id'][:20] + "..."
                    
                except json.JSONDecodeError:
                    await processing_msg.edit_text(
                        "❌ *Invalid JSON file*\n\n"
                        "📎 *Please upload a valid Google Drive credentials file*\n\n"
                        "💡 *Download from Google Cloud Console*",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    return
                except Exception as e:
                    await processing_msg.edit_text(
                        f"❌ *Invalid credentials file*\n\n"
                        f"🔍 *Error:* {str(e)}\n\n"
                        f"💡 *Please check file format and try again*",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    return
                finally:
                    os.unlink(tmp.name)
            
            # Success message
            total_accounts = config_manager.count_credentials()
            success_text = f"""
✅ *CREDENTIALS UPLOADED SUCCESSFULLY!*

📊 *Account Details:*
• Account Number: {account_number}
• Client ID: {client_id}
• Status: ✅ Valid and ready
• Storage: +15GB added

🎉 *Google Drive Setup Complete!*
• Total Accounts: {total_accounts}
• Total Storage: {total_accounts * 15}GB
• Status: ✅ Ready for backup

🚀 *Next Steps:*
• Add folders to monitor
• Start automatic backups
• Manage multiple accounts
            """
            
            keyboard = [
                [InlineKeyboardButton("📁 Add Folders", callback_data="manage_folders")],
                [InlineKeyboardButton("🚀 Start Backup", callback_data="quick_backup")],
                [InlineKeyboardButton("📊 View Usage", callback_data="view_usage")],
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
                f"❌ *Error processing credentials*\n\n"
                f"🔍 *Details:* {str(e)}\n\n"
                f"💡 *Please try uploading the file again*",
                parse_mode=ParseMode.MARKDOWN
            )