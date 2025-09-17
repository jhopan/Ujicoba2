"""
🤖 Bot Orchestrator - Simplified main bot class
📱 Demo modular architecture untuk Termux
"""

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Import all handlers
from .config.manager import config_manager
from .menus.main import MainMenuHandler
from .handlers.gdrive import GoogleDriveHandler
from .handlers.folders import FolderHandler
from .handlers.backup import BackupHandler
from .handlers.settings import SettingsHandler
from .handlers.logs import LogsHandler
from .handlers.help import HelpHandler

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TermuxTelegramBot:
    """🤖 Simplified bot orchestrator for demo"""
    
    def __init__(self, token: str):
        """Initialize bot with token"""
        self.token = token
        self.application = None
    
    def setup_handlers(self):
        """Setup basic command and callback handlers"""
        app = self.application
        
        # Command handlers
        app.add_handler(CommandHandler("start", self.start_command))
        app.add_handler(CommandHandler("menu", self.menu_command))
        app.add_handler(CommandHandler("help", self.help_command))
        app.add_handler(CommandHandler("status", self.status_command))
        app.add_handler(CommandHandler("add_folder", self.add_folder_command))
        
        # Main navigation callback handlers
        app.add_handler(CallbackQueryHandler(self.main_menu_callback, pattern="^back_to_main$"))
        app.add_handler(CallbackQueryHandler(self.main_menu_callback, pattern="^main_menu$"))
        
        # Google Drive handlers (hanya yang ada)
        app.add_handler(CallbackQueryHandler(self.setup_drive_callback, pattern="^setup_drive$"))
        
        # Folder management handlers
        app.add_handler(CallbackQueryHandler(self.manage_folders_callback, pattern="^manage_folders$"))
        app.add_handler(CallbackQueryHandler(self.add_downloads_callback, pattern="^add_downloads$"))
        app.add_handler(CallbackQueryHandler(self.add_pictures_callback, pattern="^add_pictures$"))
        app.add_handler(CallbackQueryHandler(self.add_documents_callback, pattern="^add_documents$"))
        app.add_handler(CallbackQueryHandler(self.add_whatsapp_callback, pattern="^add_whatsapp$"))
        app.add_handler(CallbackQueryHandler(self.add_dcim_callback, pattern="^add_dcim$"))
        app.add_handler(CallbackQueryHandler(self.add_custom_path_callback, pattern="^add_custom_path$"))
        app.add_handler(CallbackQueryHandler(self.view_all_folders_callback, pattern="^view_all_folders$"))
        app.add_handler(CallbackQueryHandler(self.remove_folder_callback, pattern="^remove_folder$"))
        
        # Backup operation handlers
        app.add_handler(CallbackQueryHandler(self.quick_backup_callback, pattern="^quick_backup$"))
        app.add_handler(CallbackQueryHandler(self.schedule_backup_callback, pattern="^schedule_backup$"))
        app.add_handler(CallbackQueryHandler(self.manual_backup_callback, pattern="^manual_backup$"))
        app.add_handler(CallbackQueryHandler(self.stop_backup_callback, pattern="^stop_backup$"))
        
        # Account management handlers
        app.add_handler(CallbackQueryHandler(self.manage_accounts_callback, pattern="^manage_accounts$"))
        
        # Settings handlers
        app.add_handler(CallbackQueryHandler(self.auto_delete_settings_callback, pattern="^auto_delete_settings$"))
        app.add_handler(CallbackQueryHandler(self.system_status_callback, pattern="^system_status$"))
        
        # Logs handlers
        app.add_handler(CallbackQueryHandler(self.view_logs_callback, pattern="^view_logs$"))
        
        # Help handlers
        app.add_handler(CallbackQueryHandler(self.help_menu_callback, pattern="^help_menu$"))
        
        # Dynamic folder removal handler
        app.add_handler(CallbackQueryHandler(self.remove_specific_folder_callback, pattern="^remove_folder_"))
        
        # Default callback handler for unmatched patterns
        app.add_handler(CallbackQueryHandler(self.handle_unknown_callback))
        
        logger.info("✅ Basic handlers setup complete (modular demo)")
    
    async def start_command(self, update: Update, context):
        """Handle /start command"""
        await MainMenuHandler.show_main_menu(update, context)
    
    async def menu_command(self, update: Update, context):
        """Handle /menu command"""
        await MainMenuHandler.show_main_menu(update, context)
    
    async def help_command(self, update: Update, context):
        """Handle /help command"""
        await HelpHandler.help_menu(update, context)
    
    async def status_command(self, update: Update, context):
        """Handle /status command - quick status check"""
        status = config_manager.get_system_status()
        
        status_text = f"""
🎯 *MODULAR BOT STATUS*

⚡ Google Drive: {status['credentials_count']} accounts
📁 Folders: {status['folder_count']} monitored  
🧹 Auto-Delete: {'✅ On' if status['auto_delete'] else '❌ Off'}
🔔 Notifications: {'✅ On' if status['notifications'] else '❌ Off'}

🎯 *Modular Architecture Active*
💡 Use /menu for full interface
        """
        
        await update.message.reply_text(status_text, parse_mode='Markdown')
    
    async def add_folder_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /add_folder command"""
        if not context.args:
            await update.message.reply_text(
                "📝 *Add Custom Folder*\n\n"
                "🎯 Usage: `/add_folder [name] [path]`\n\n"
                "📋 Examples:\n"
                "• `/add_folder /storage/emulated/0/MyFolder`\n"
                "• `/add_folder MyMusic /storage/emulated/0/Music`\n"
                "• `/add_folder Work /storage/emulated/0/Documents/Work`",
                parse_mode='Markdown'
            )
            return
        
        if len(context.args) == 1:
            # Only path provided, use folder name from path
            path = context.args[0]
            name = path.split('/')[-1] or "Custom Folder"
        else:
            # Name and path provided
            name = context.args[0]
            path = context.args[1]
        
        try:
            config_manager.save_folder_config(name, path)
            await update.message.reply_text(
                f"✅ *Folder Added*\n\n"
                f"📁 *Name:* {name}\n"
                f"📂 *Path:* `{path}`\n\n"
                f"💡 Use /menu to manage all folders",
                parse_mode='Markdown'
            )
        except Exception as e:
            await update.message.reply_text(
                f"❌ *Error adding folder:*\n`{str(e)}`",
                parse_mode='Markdown'
            )
    
    async def handle_unknown_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle unknown callback queries"""
        query = update.callback_query
        await query.answer("🤔 Demo feature. Try main menu options...")
        await MainMenuHandler.show_main_menu(query)
    
    async def error_handler(self, update: Update, context):
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}")
        
        # Try to notify user if possible
        if update and update.effective_chat:
            try:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="❌ An error occurred. This is a modular demo."
                )
            except:
                pass
    
    async def main_menu_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Wrapper for main menu callback"""
        await MainMenuHandler.show_main_menu(update, context)
    
    async def setup_drive_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Wrapper for setup drive callback"""
        await GoogleDriveHandler.setup_drive_menu(update.callback_query)
    
    async def manage_folders_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Wrapper for manage folders callback"""
        await FolderHandler.manage_folders_menu(update.callback_query)
    
    async def add_downloads_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Wrapper for add downloads callback"""
        await FolderHandler.add_downloads_folder(update.callback_query)
    
    async def add_pictures_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Wrapper for add pictures callback"""
        await FolderHandler.add_pictures_folder(update.callback_query)
    
    async def add_documents_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Wrapper for add documents callback"""
        await FolderHandler.add_documents_folder(update.callback_query)
    
    async def add_whatsapp_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Wrapper for add whatsapp callback"""
        await FolderHandler.add_whatsapp_folder(update.callback_query)
    
    async def add_dcim_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Wrapper for add dcim callback"""
        await FolderHandler.add_dcim_folder(update.callback_query)
    
    async def add_custom_path_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Wrapper for add custom path callback"""
        await FolderHandler.add_custom_path(update.callback_query)
    
    async def view_all_folders_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Wrapper for view all folders callback"""
        await FolderHandler.view_all_folders(update.callback_query)
    
    async def remove_folder_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Wrapper for remove folder callback"""
        await FolderHandler.remove_folder(update.callback_query)
    
    async def remove_specific_folder_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Wrapper for removing specific folder"""
        callback_data = update.callback_query.data
        # Extract folder name from callback_data "remove_folder_{folder_name}"
        folder_name = callback_data.replace("remove_folder_", "", 1)
        await FolderHandler.remove_specific_folder(update.callback_query, folder_name)
    
    async def quick_backup_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Wrapper for quick backup callback"""
        await BackupHandler.do_quick_backup(update.callback_query)
    
    async def schedule_backup_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Wrapper for schedule backup callback"""
        await BackupHandler.schedule_backup_menu(update.callback_query)
    
    async def manual_backup_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Wrapper for manual backup callback"""
        await BackupHandler.manual_backup_menu(update.callback_query)
    
    async def stop_backup_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Wrapper for stop backup callback"""
        await BackupHandler.stop_backup(update.callback_query)
    
    async def manage_accounts_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Wrapper for manage accounts callback"""
        await GoogleDriveHandler.manage_accounts(update.callback_query)
    
    async def auto_delete_settings_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Wrapper for auto delete settings callback"""
        await SettingsHandler.settings_menu(update.callback_query)
    
    async def system_status_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Wrapper for system status callback"""
        await SettingsHandler.settings_menu(update.callback_query)
    
    async def view_logs_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Wrapper for view logs callback"""
        await LogsHandler.logs_menu(update.callback_query)
    
    async def help_menu_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Wrapper for help menu callback"""
        await HelpHandler.help_menu(update.callback_query)
    
    def create_application(self):
        """Create and configure the bot application"""
        # Create application
        self.application = Application.builder().token(self.token).build()
        
        # Setup all handlers
        self.setup_handlers()
        
        # Add error handler
        self.application.add_error_handler(self.error_handler)
        
        logger.info("🤖 Modular bot application created and configured")
        return self.application
    
    def run(self):
        """Run the bot"""
        if not self.application:
            self.create_application()
        
        logger.info("🚀 Starting Termux Telegram Bot (Modular Demo)...")
        logger.info("📱 Ready for Android backup operations!")
        
        # Run the bot
        self.application.run_polling(
            allowed_updates=["message", "callback_query"]
        )

# Factory function for easy bot creation
def create_bot(token: str) -> TermuxTelegramBot:
    """Create and return configured bot instance"""
    bot = TermuxTelegramBot(token)
    bot.create_application()
    return bot
