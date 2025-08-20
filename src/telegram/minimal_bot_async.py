#!/usr/bin/env python3
"""
🚀 MINIMAL TELEGRAM BOT - FULL ASYNC VERSION  
📱 Proper async pattern dengan semua await
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
🤖 **TERMUX BACKUP BOT (Async)**
✅ Bot berhasil terhubung!

📱 Full async version dengan proper await!
    """
    
    await update.message.reply_text(welcome_text)

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show status"""
    user_id = str(update.effective_user.id)
    
    if user_id != ALLOWED_USER:
        await update.message.reply_text("❌ Access denied")
        return
    
    await update.message.reply_text("✅ Async bot running perfectly!")

async def main():
    """Full async main with proper await sequence"""
    print("🤖 Starting Full Async Bot...")
    print(f"🔑 Token: {TOKEN[:10]}...")
    print(f"👤 Allowed User: {ALLOWED_USER}")
    
    # Create application
    app = Application.builder().token(TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("status", status_command))
    
    print("✅ Bot Ready!")
    print("📱 Send /start to your bot")
    
    # PROPER async sequence - all methods awaited
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    try:
        await app.updater.idle()
    finally:
        # Proper shutdown sequence
        await app.updater.stop()
        await app.stop()
        await app.shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())  # OK to use asyncio.run with full async pattern
    except KeyboardInterrupt:
        print("\n⏹️ Async bot stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
