#!/usr/bin/env python3
"""
🚀 MINIMAL TELEGRAM BOT
📱 Super simple version without complex error handling
"""

import os
import asyncio
import logging
from pathlib import Path

# Setup minimal logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from telegram.ext import Application, CommandHandler
    from telegram import Update
    from telegram.ext import ContextTypes
    TELEGRAM_AVAILABLE = True
except ImportError:
    print("❌ Install: pip install python-telegram-bot")
    exit(1)

# Get bot token
PROJECT_ROOT = Path(__file__).parent.parent.parent
env_file = PROJECT_ROOT / ".env"

if not env_file.exists():
    print("❌ .env file not found")
    print("📝 Create .env with TELEGRAM_BOT_TOKEN and ALLOWED_USER_IDS")
    exit(1)

# Read config
config = {}
with open(env_file, 'r') as f:
    for line in f:
        if '=' in line and not line.strip().startswith('#'):
            key, value = line.strip().split('=', 1)
            config[key] = value

TOKEN = config.get('TELEGRAM_BOT_TOKEN')
ALLOWED_USER = config.get('ALLOWED_USER_IDS')

if not TOKEN or not ALLOWED_USER:
    print("❌ Missing TELEGRAM_BOT_TOKEN or ALLOWED_USER_IDS in .env")
    exit(1)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Simple start command"""
    user_id = str(update.effective_user.id)
    
    if user_id != ALLOWED_USER:
        await update.message.reply_text(f"❌ Access denied. Your ID: {user_id}")
        return
    
    welcome_text = """
🤖 **TERMUX BACKUP BOT**
✅ Bot berhasil terhubung!

🎯 **Available Commands:**
/start - Show this message
/status - Show bot status
/help - Show help

📱 Bot ready for Android backup!
    """
    
    await update.message.reply_text(welcome_text)

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show status"""
    user_id = str(update.effective_user.id)
    
    if user_id != ALLOWED_USER:
        await update.message.reply_text("❌ Access denied")
        return
    
    await update.message.reply_text("✅ Bot is running normally!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help"""
    user_id = str(update.effective_user.id)
    
    if user_id != ALLOWED_USER:
        await update.message.reply_text("❌ Access denied")
        return
    
    help_text = """
🆘 **HELP**

📋 **Commands:**
/start - Main menu
/status - Check bot status  
/help - This help message

🚀 **Next Steps:**
1. Send /start to begin
2. Set up Google Drive credentials
3. Configure backup folders

🤖 Bot is ready!
    """
    
    await update.message.reply_text(help_text)

def main():
    """Main bot function - sync version"""
    print("🤖 Starting Minimal Telegram Bot...")
    print(f"🔑 Token: {TOKEN[:10]}...")
    print(f"👤 Allowed User: {ALLOWED_USER}")
    
    # Create application
    app = Application.builder().token(TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("help", help_command))
    
    print("✅ Bot Ready!")
    print("📱 Send /start to your bot")
    
    # Let PTB handle event loop completely
    app.run_polling(close_loop=True)

if __name__ == "__main__":
    try:
        main()  # NO asyncio.run() here!
    except KeyboardInterrupt:
        print("\n⏹️ Bot stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
