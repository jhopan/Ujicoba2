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
        
        # Main navigation callback handlers
        app.add_handler(CallbackQueryHandler(self.main_menu_callback, pattern="^back_to_main$"))
        app.add_handler(CallbackQueryHandler(self.main_menu_callback, pattern="^main_menu$"))
        
        # Google Drive handlers (hanya yang ada)
        app.add_handler(CallbackQueryHandler(self.setup_drive_callback, pattern="^setup_drive$"))
        
        # Folder management handlers (hanya yang ada)
        app.add_handler(CallbackQueryHandler(FolderHandler.manage_folders_menu, pattern="^manage_folders$"))
        
        # Backup operation handlers (hanya yang ada)
        app.add_handler(CallbackQueryHandler(BackupHandler.manual_backup_menu, pattern="^quick_backup$"))
        app.add_handler(CallbackQueryHandler(BackupHandler.schedule_backup_menu, pattern="^schedule_backup$"))
        
        # Settings handlers (hanya yang ada)
        app.add_handler(CallbackQueryHandler(SettingsHandler.settings_menu, pattern="^show_settings$"))
        
        # Logs handlers (hanya yang ada) 
        app.add_handler(CallbackQueryHandler(LogsHandler.logs_menu, pattern="^show_logs$"))
        
        # Help handlers (hanya yang ada)
        app.add_handler(CallbackQueryHandler(HelpHandler.help_menu, pattern="^show_help$"))
        
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
    
    async def handle_unknown_callback(self, query):
        """Handle unknown callback queries"""
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
        await GoogleDriveHandler.setup_drive_menu(update, context)
    
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
