"""
🚀 TERMUX TELEGRAM BOT - User Friendly Interface
📱 Bot khusus untuk Android Termux dengan button interface
🎯 Click-click interface, tidak perlu ketik command manual
"""

import os
import sys
import json
import asyncio
import logging
import signal
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand, ReplyKeyboardMarkup, KeyboardButton
    from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler
    from telegram.constants import ParseMode
    TELEGRAM_AVAILABLE = True
    logger.info("✅ Telegram library loaded")
except ImportError:
    TELEGRAM_AVAILABLE = False
    logger.error("❌ Telegram library not available")
    print("📦 Install: pip install python-telegram-bot")

# Project paths untuk Termux
PROJECT_ROOT = Path(__file__).parent.parent.parent
TERMUX_HOME = Path("/data/data/com.termux/files/home")
STORAGE_PATH = TERMUX_HOME / "storage" / "shared"

class TermuxTelegramBot:
    """🤖 Termux Telegram Bot dengan Interface User-Friendly"""
    
    def __init__(self):
        self.app = None
        self.is_setup_mode = False
        self.user_data = {}
        
        logger.info("🤖 Termux Telegram Bot initialized")
    
    async def auto_start(self):
        """🚀 Auto start dengan deteksi setup untuk Termux"""
        logger.info("📱 Starting Termux bot...")
        
        env_file = PROJECT_ROOT / ".env"
        
        if not env_file.exists() or not self._is_setup_complete():
            logger.info("🛠️ Setup required...")
            await self._run_termux_setup()
        else:
            logger.info("✅ Setup complete, starting bot...")
            await self._run_termux_bot()
    
    def _is_setup_complete(self) -> bool:
        """✅ Check setup status"""
        try:
            env_file = PROJECT_ROOT / ".env"
            if not env_file.exists():
                return False
            
            with open(env_file, 'r') as f:
                content = f.read()
            
            has_token = 'TELEGRAM_BOT_TOKEN=' in content and 'your_bot_token' not in content.lower()
            has_user_id = 'ALLOWED_USER_IDS=' in content and 'your_user_id' not in content.lower()
            
            return has_token and has_user_id
        except:
            return False
    
    async def _run_termux_setup(self):
        """🛠️ Interactive setup untuk Termux"""
        print("\n" + "="*50)
        print("🤖 TERMUX BACKUP SYSTEM - AUTO SETUP")
        print("📱 Setup khusus untuk Android Termux")
        print("="*50)
        
        # Step 1: Bot Token
        print("\n📋 STEP 1: Telegram Bot Setup")
        print("1. Buka Telegram, cari @BotFather")
        print("2. Kirim: /newbot")
        print("3. Ikuti instruksi buat bot")
        print("4. Copy token yang diberikan")
        
        while True:
            token = input("\n🔑 Paste Bot Token: ").strip()
            if token and len(token) > 40:
                break
            print("❌ Token tidak valid. Coba lagi.")
        
        # Step 2: User ID
        print("\n📋 STEP 2: User ID Setup")
        print("1. Buka Telegram, cari @userinfobot")
        print("2. Kirim: /start")
        print("3. Copy User ID yang diberikan")
        
        while True:
            user_id = input("\n👤 Paste User ID: ").strip()
            if user_id and user_id.isdigit():
                break
            print("❌ User ID harus angka. Coba lagi.")
        
        # Save config
        await self._save_termux_config(token, user_id)
        
        print(f"\n✅ Setup selesai!")
        print(f"🚀 Starting bot...")
        
        await self._start_termux_bot(token)
    
    async def _save_termux_config(self, token: str, user_id: str):
        """💾 Save config untuk Termux"""
        env_content = f"""# 🤖 Termux Backup System Configuration
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# 📱 Telegram Bot
TELEGRAM_BOT_TOKEN={token}
ALLOWED_USER_IDS={user_id}

# 📁 Termux Paths
BACKUP_BASE_DIR={TERMUX_HOME}/backups
STORAGE_SHARED={STORAGE_PATH}

# ⚙️ Settings
MAX_FILE_SIZE=0
AUTO_DELETE_AFTER_UPLOAD=false
ORGANIZE_BY_DATE=true

# ☁️ Google Drive
UNLIMITED_ACCOUNTS=true
MAX_ACCOUNTS=20

# 📝 Logging
LOG_LEVEL=INFO
LOG_TO_TELEGRAM=true

# ✅ Status
SETUP_COMPLETED=true
PLATFORM=termux
"""
        
        env_file = PROJECT_ROOT / ".env"
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        logger.info("✅ Termux configuration saved")
    
    async def _start_termux_bot(self, token: str):
        """🤖 Start bot untuk setup mode"""
        try:
            self.app = Application.builder().token(token).build()
            
            # Setup handlers
            self.app.add_handler(CommandHandler("start", self._setup_start))
            self.app.add_handler(CallbackQueryHandler(self._setup_callback))
            self.app.add_handler(MessageHandler(filters.Document.ALL, self._setup_document))
            
            print(f"\n🤖 Bot setup mode aktif!")
            print(f"📱 Buka Telegram, kirim /start ke bot Anda")
            print(f"⏳ Waiting for Google Drive credentials...")
            
            await self.app.run_polling(stop_signals=None)
            
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"❌ Error: {e}")
        finally:
            if self.app:
                try:
                    await self.app.shutdown()
                except:
                    pass
    
    async def _setup_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """🎯 Setup start handler"""
        user_id = update.effective_user.id
        allowed_user = os.getenv('ALLOWED_USER_IDS', '')
        
        if str(user_id) != allowed_user:
            await update.message.reply_text(f"❌ Access denied\nYour ID: {user_id}")
            return
        
        welcome_text = f"""
🎉 *SELAMAT DATANG!*

🤖 *Termux Backup System berhasil terhubung!*

📋 *Setup Progress: 70% Complete*

🔄 *Langkah terakhir:*
Upload Google Drive credentials untuk unlimited backup

📁 *Cara mendapatkan credentials:*
• Buka: console.cloud.google.com
• Buat project baru
• Enable Google Drive API
• Buat OAuth 2.0 Credentials (Desktop app)
• Download file JSON

📎 *Upload file JSON di sini sekarang*
        """
        
        keyboard = [
            [InlineKeyboardButton("📖 Panduan Detail", callback_data="guide")],
            [InlineKeyboardButton("⏭️ Skip (Setup Nanti)", callback_data="skip")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def _setup_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """⚙️ Setup callback handler"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "guide":
            guide_text = """
📚 *Panduan Google Drive API:*

*1. Buka Browser:*
console.cloud.google.com

*2. Buat Project:*
• New Project → "Termux Backup"
• Create

*3. Enable API:*
• APIs & Services → Library
• Cari "Google Drive API" → Enable

*4. Buat Credentials:*
• Credentials → Create Credentials
• OAuth 2.0 Client IDs
• Desktop application
• Download JSON

*5. Upload:*
• Kembali ke chat ini
• Upload file JSON
• Bot akan restart otomatis
            """
            
            await query.edit_message_text(
                guide_text,
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif query.data == "skip":
            await self._finalize_setup_skip()
            
            skip_text = """
⏭️ *Setup Mode Selesai*

🚀 *Bot akan restart dalam mode normal...*

📱 *Setelah restart:*
• Kirim /start untuk menu utama
• Gunakan /accounts untuk add credentials nanti
• Semua fitur accessible via button

⚡ *Restarting...*
            """
            
            await query.edit_message_text(
                skip_text,
                parse_mode=ParseMode.MARKDOWN
            )
            
            await asyncio.sleep(3)
            await self._restart_to_normal()
    
    async def _setup_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """📎 Handle credentials upload"""
        try:
            document = update.message.document
            
            if not document.file_name.endswith('.json'):
                await update.message.reply_text("❌ File harus .json format")
                return
            
            # Download file
            file_obj = await context.bot.get_file(document.file_id)
            credentials_dir = PROJECT_ROOT / "credentials"
            credentials_dir.mkdir(exist_ok=True)
            
            # Save credentials
            existing_files = list(credentials_dir.glob("account*.json"))
            account_number = len(existing_files) + 1
            credentials_path = credentials_dir / f"account{account_number}_credentials.json"
            
            await file_obj.download_to_drive(credentials_path)
            
            # Validate JSON
            try:
                with open(credentials_path, 'r') as f:
                    cred_data = json.load(f)
                
                if 'client_id' not in cred_data.get('installed', {}):
                    credentials_path.unlink()
                    raise ValueError("Invalid credentials format")
                
            except Exception as e:
                await update.message.reply_text(f"❌ Invalid JSON: {e}")
                return
            
            # Success
            await self._finalize_setup_complete()
            
            success_text = f"""
✅ *CREDENTIALS UPLOADED!*

🎉 *Setup 100% Complete!*

📁 *Saved as:* account{account_number}_credentials.json

🔄 *Bot restarting ke mode normal...*

📱 *Setelah restart:*
• Kirim /start untuk menu utama
• Semua fitur sudah ready
• Unlimited accounts support active

⚡ *Restarting in 5 seconds...*
            """
            
            await update.message.reply_text(
                success_text,
                parse_mode=ParseMode.MARKDOWN
            )
            
            await asyncio.sleep(5)
            await self._restart_to_normal()
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
    
    async def _finalize_setup_complete(self):
        """✅ Finalize setup with credentials"""
        env_file = PROJECT_ROOT / ".env"
        
        if env_file.exists():
            with open(env_file, 'r') as f:
                content = f.read()
            
            content = content.replace('SETUP_COMPLETED=true', 'SETUP_COMPLETED=true\nCREDENTIALS_UPLOADED=true')
            
            with open(env_file, 'w') as f:
                f.write(content)
    
    async def _finalize_setup_skip(self):
        """⏭️ Finalize setup without credentials"""
        env_file = PROJECT_ROOT / ".env"
        
        if env_file.exists():
            with open(env_file, 'r') as f:
                content = f.read()
            
            content += "\nCREDENTIALS_UPLOADED=false\n"
            
            with open(env_file, 'w') as f:
                f.write(content)
    
    async def _restart_to_normal(self):
        """🔄 Restart ke normal mode"""
        print("🔄 Restarting to normal mode...")
        await asyncio.sleep(2)
        await self._run_termux_bot()
    
    async def _run_termux_bot(self):
        """🚀 Run normal bot mode untuk Termux"""
        logger.info("🚀 Starting normal Termux bot...")
        
        # Load environment
        env_file = PROJECT_ROOT / ".env"
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.strip().startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
        
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not token:
            raise ValueError("No bot token found")
        
        # Setup bot
        self.app = Application.builder().token(token).build()
        self._setup_termux_handlers()
        
        # Set commands
        commands = [
            BotCommand("start", "🏠 Menu Utama"),
            BotCommand("backup", "💾 Start Backup"),
            BotCommand("accounts", "👥 Google Drive Accounts"),
            BotCommand("folders", "📁 Backup Folders"),
            BotCommand("settings", "⚙️ Auto-Delete & Settings"),
            BotCommand("status", "📊 System Status"),
            BotCommand("help", "❓ Bantuan")
        ]
        
        # Initialize and start with proper async sequence
        await self.app.initialize()
        await self.app.start()
        
        try:
            await self.app.bot.set_my_commands(commands)
            
            print("✅ Termux Bot Ready!")
            print("📱 Kirim /start ke bot Telegram Anda")
            
            # Proper async polling sequence
            await self.app.updater.start_polling()
            
            # Keep running
            import signal
            stop_signals = (signal.SIGTERM, signal.SIGINT)
            loop = asyncio.get_running_loop()
            
            for sig in stop_signals:
                loop.add_signal_handler(sig, lambda: None)
            
            await asyncio.Event().wait()
            
        except KeyboardInterrupt:
            print("\n⏹️ Bot stopped by user")
        except Exception as e:
            logger.error(f"Error in bot: {e}")
            print(f"❌ Error: {e}")
        finally:
            # Proper shutdown
            try:
                await self.app.updater.stop()
                await self.app.stop()
                await self.app.shutdown()
            except:
                pass
    
    def _setup_termux_handlers(self):
        """⚙️ Setup handlers untuk Termux"""
        # Main commands
        self.app.add_handler(CommandHandler("start", self.termux_start))
        self.app.add_handler(CommandHandler("backup", self.termux_backup))
        self.app.add_handler(CommandHandler("accounts", self.termux_accounts))
        self.app.add_handler(CommandHandler("folders", self.termux_folders))
        self.app.add_handler(CommandHandler("settings", self.termux_settings))
        self.app.add_handler(CommandHandler("status", self.termux_status))
        self.app.add_handler(CommandHandler("help", self.termux_help))
        
        # Callback handler
        self.app.add_handler(CallbackQueryHandler(self.termux_callback))
        
        # Document handler
        self.app.add_handler(MessageHandler(filters.Document.ALL, self.termux_document))
    
    # ============================================================================
    # 🎯 TERMUX BOT HANDLERS - User Friendly Interface
    # ============================================================================
    
    async def termux_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """🏠 Main menu dengan button interface"""
        user_id = update.effective_user.id
        
        if not self._check_permission(user_id):
            await update.message.reply_text("❌ Access denied")
            return
        
        # Get status
        credentials_count = self._count_credentials()
        folders_count = self._get_folder_count()
        
        welcome_text = f"""
🤖 *TERMUX BACKUP SYSTEM*
📱 *Android Backup dengan Unlimited Storage*

👤 *User:* {update.effective_user.first_name}
📊 *Status:* {'✅ Ready' if credentials_count > 0 else '⚠️ Setup Needed'}
🗃️ *Accounts:* {credentials_count} Google Drive
📁 *Folders:* {folders_count} monitored

🎯 *Pilih menu:*
        """
        
        # Create user-friendly keyboard
        keyboard = []
        
        # Quick actions
        if credentials_count > 0:
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
    
    async def termux_backup(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """💾 Backup menu dengan options"""
        backup_text = """
💾 *BACKUP OPTIONS*

🎯 *Pilih jenis backup:*

🚀 *Quick Backup* - Backup semua folder
📁 *Custom Backup* - Pilih folder tertentu
🎯 *Smart Backup* - Hanya file yang berubah
        """
        
        keyboard = [
            [InlineKeyboardButton("🚀 Quick Backup", callback_data="do_quick_backup")],
            [InlineKeyboardButton("📁 Custom Backup", callback_data="do_custom_backup")],
            [InlineKeyboardButton("🎯 Smart Backup", callback_data="do_smart_backup")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            backup_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def termux_accounts(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """👥 Google Drive accounts management"""
        credentials_count = self._count_credentials()
        
        accounts_text = f"""
👥 *GOOGLE DRIVE ACCOUNTS*

📊 *Total Accounts:* {credentials_count}
💾 *Storage:* Unlimited (15GB per account)

🎯 *Account Management:*
        """
        
        keyboard = [
            [InlineKeyboardButton("➕ Add Account", callback_data="add_new_account")],
            [InlineKeyboardButton("📊 View Usage", callback_data="view_usage")],
            [InlineKeyboardButton("🔧 Manage", callback_data="manage_account_list")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            accounts_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def termux_folders(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """📁 Folder management"""
        folders_text = """
📁 *BACKUP FOLDERS*

🎯 *Configure folders untuk backup:*

📱 *Quick Add:*
• Download folder
• Pictures/DCIM
• Documents
• WhatsApp Media

📝 *Custom path juga bisa*
        """
        
        keyboard = [
            [InlineKeyboardButton("📥 Add Downloads", callback_data="add_downloads")],
            [InlineKeyboardButton("📸 Add Pictures", callback_data="add_pictures")],
            [InlineKeyboardButton("📄 Add Documents", callback_data="add_documents")],
            [InlineKeyboardButton("💬 Add WhatsApp", callback_data="add_whatsapp")],
            [InlineKeyboardButton("📝 Custom Path", callback_data="add_custom_path")],
            [InlineKeyboardButton("📋 View All", callback_data="view_all_folders")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            folders_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def termux_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """⚙️ Settings menu dengan auto-delete toggle"""
        # Get current settings
        auto_delete = self._get_setting('AUTO_DELETE_AFTER_UPLOAD', 'false') == 'true'
        
        settings_text = f"""
⚙️ *SYSTEM SETTINGS*

🗑️ *Auto-Delete:* {'✅ ON' if auto_delete else '❌ OFF'}
📏 *File Size Limit:* Unlimited
📱 *Platform:* Android Termux

🎯 *Configure settings:*
        """
        
        keyboard = [
            [InlineKeyboardButton(
                f"🗑️ Auto-Delete: {'ON' if auto_delete else 'OFF'}", 
                callback_data="toggle_auto_delete"
            )],
            [InlineKeyboardButton("📏 File Size Limit", callback_data="set_file_limit")],
            [InlineKeyboardButton("⏰ Schedule Settings", callback_data="schedule_settings")],
            [InlineKeyboardButton("🔔 Notifications", callback_data="notification_settings")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            settings_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def termux_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """📊 System status"""
        credentials_count = self._count_credentials()
        folders_count = self._get_folder_count()
        
        status_text = f"""
📊 *SYSTEM STATUS*

🤖 *Bot:* ✅ Online
📱 *Platform:* Android Termux
🗃️ *Accounts:* {credentials_count} configured
📁 *Folders:* {folders_count} monitored

💾 *Storage:*
• Local: Available
• Google Drive: {credentials_count * 15}GB total

🔄 *Last Backup:* Not available
⏰ *Next Backup:* Manual only

📊 *Performance:* Ready
        """
        
        keyboard = [
            [InlineKeyboardButton("🔄 Refresh", callback_data="refresh_status")],
            [InlineKeyboardButton("📋 Detailed Info", callback_data="detailed_status")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            status_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def termux_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """❓ Help menu"""
        help_text = """
❓ *TERMUX BACKUP SYSTEM HELP*

🎯 *Quick Guide:*

*1. Setup:*
• Add Google Drive account
• Select backup folders
• Enable auto-delete if needed

*2. Backup:*
• Quick backup = backup all
• Custom = select specific
• Smart = only changed files

*3. Settings:*
• Auto-delete toggle
• File size limits
• Schedule options

📱 *Termux Specific:*
• Storage access granted
• Background operation
• Battery optimization

📞 *Support:*
• Check logs for errors
• Verify internet connection
• Re-setup if needed
        """
        
        keyboard = [
            [InlineKeyboardButton("📖 Full Guide", callback_data="full_guide")],
            [InlineKeyboardButton("🛠️ Troubleshooting", callback_data="troubleshoot")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def termux_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """⚙️ Handle all callback queries"""
        query = update.callback_query
        await query.answer()
        
        if not self._check_permission(update.effective_user.id):
            await query.edit_message_text("❌ Access denied")
            return
        
        data = query.data
        
        if data == "back_to_main":
            await self.termux_start(update, context)
        elif data == "toggle_auto_delete":
            await self._toggle_auto_delete(query)
        elif data == "setup_drive":
            await self._setup_google_drive(query)
        elif data == "quick_backup":
            await self._do_quick_backup(query)
        elif data == "add_downloads":
            await self._add_downloads_folder(query)
        elif data == "add_pictures":
            await self._add_pictures_folder(query)
        elif data == "view_usage":
            await self._view_account_usage(query)
        else:
            await query.edit_message_text(f"🔧 Feature: {data}\n(In development...)")
    
    async def termux_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """📎 Handle document uploads"""
        await update.message.reply_text("📎 Document received\n(Processing feature in development)")
    
    # ============================================================================
    # 🎯 HELPER METHODS
    # ============================================================================
    
    def _check_permission(self, user_id: int) -> bool:
        """✅ Check user permission"""
        allowed_ids = os.getenv('ALLOWED_USER_IDS', '').split(',')
        return str(user_id) in allowed_ids
    
    def _count_credentials(self) -> int:
        """📊 Count credentials files"""
        credentials_dir = PROJECT_ROOT / "credentials"
        if not credentials_dir.exists():
            return 0
        return len(list(credentials_dir.glob("*.json")))
    
    def _get_folder_count(self) -> int:
        """📁 Get monitored folder count"""
        # Placeholder - integrate with actual settings
        return 0
    
    def _get_setting(self, key: str, default: str = '') -> str:
        """⚙️ Get setting value"""
        return os.getenv(key, default)
    
    # Placeholder methods untuk callback handlers
    async def _toggle_auto_delete(self, query):
        """🗑️ Toggle auto-delete setting"""
        current = self._get_setting('AUTO_DELETE_AFTER_UPLOAD', 'false') == 'true'
        new_value = 'true' if not current else 'false'
        
        # Update env file
        env_file = PROJECT_ROOT / ".env"
        if env_file.exists():
            with open(env_file, 'r') as f:
                content = f.read()
            
            if 'AUTO_DELETE_AFTER_UPLOAD=' in content:
                content = content.replace(
                    f'AUTO_DELETE_AFTER_UPLOAD={"true" if current else "false"}',
                    f'AUTO_DELETE_AFTER_UPLOAD={new_value}'
                )
            else:
                content += f"\nAUTO_DELETE_AFTER_UPLOAD={new_value}\n"
            
            with open(env_file, 'w') as f:
                f.write(content)
        
        status = "ON" if new_value == 'true' else "OFF"
        await query.answer(f"✅ Auto-Delete: {status}")
        await self.termux_settings(query, None)
    
    async def _setup_google_drive(self, query):
        """☁️ Setup Google Drive"""
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
    
    async def _do_quick_backup(self, query):
        """🚀 Quick backup"""
        await query.edit_message_text("🚀 Starting quick backup...\n(Feature in development)")
    
    async def _add_downloads_folder(self, query):
        """📥 Add downloads folder"""
        downloads_path = str(STORAGE_PATH / "Download")
        await query.answer("✅ Downloads folder added")
        await query.edit_message_text(f"✅ Added folder:\n{downloads_path}\n\n(Feature in development)")
    
    async def _add_pictures_folder(self, query):
        """📸 Add pictures folder"""
        pictures_path = str(STORAGE_PATH / "Pictures")
        await query.answer("✅ Pictures folder added")
        await query.edit_message_text(f"✅ Added folder:\n{pictures_path}\n\n(Feature in development)")
    
    async def _view_account_usage(self, query):
        """📊 View account usage"""
        usage_text = """
📊 *ACCOUNT USAGE*

*Account 1:*
• Used: 2.3GB / 15GB
• Available: 12.7GB
• Status: ✅ Active

*Total Storage:*
• Accounts: 1
• Total: 15GB
• Used: 2.3GB
• Available: 12.7GB

(Real data will be implemented)
        """
        
        keyboard = [
            [InlineKeyboardButton("🔄 Refresh", callback_data="refresh_usage")],
            [InlineKeyboardButton("🔙 Back", callback_data="manage_accounts")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            usage_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )


# ============================================================================
# 🚀 MAIN ENTRY POINT
# ============================================================================

async def main():
    """🚀 Main function untuk Termux"""
    try:
        if not TELEGRAM_AVAILABLE:
            print("❌ Telegram library not available")
            print("📦 Install: pip install python-telegram-bot")
            return
        
        print("🤖 Starting Termux Telegram Bot...")
        
        bot = TermuxTelegramBot()
        await bot.auto_start()
        
    except KeyboardInterrupt:
        print("\n⏹️ Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🤖 Termux Backup System - Telegram Bot")
    print("📱 Click-click interface, user-friendly")
    print("="*50)
    
    try:
        # Simple asyncio run without complex policies
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Final error: {e}")
