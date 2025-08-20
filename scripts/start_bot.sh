#!/data/data/com.termux/files/usr/bin/bash

# 🚀 Ultimate Backup System - Termux Launcher
# 📱 Launcher khusus untuk Android Termux

echo "🤖========================================"
echo "🚀 ULTIMATE BACKUP SYSTEM"
echo "📱 Starting Telegram Bot..."
echo "========================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found!"
    echo "📦 Please run: ./install_termux.sh first"
    exit 1
fi

echo "✅ Python3 found"

# Check if we're in the right directory
if [ ! -f "src/telegram/ultimate_telegram_bot.py" ]; then
    echo "❌ Bot file not found!"
    echo "📁 Make sure you're in the backup_system directory"
    echo "💡 Try: cd ~/backup_system"
    exit 1
fi

echo "✅ Bot files found"

# Set environment for Android
export PYTHONPATH="$PWD/src:$PYTHONPATH"
export ANDROID_DATA="/data"
export ANDROID_ROOT="/system"

echo "🚀 Starting Ultimate Telegram Bot..."
echo "📱 Open your Telegram and send /start to your bot"
echo "⚠️  Press Ctrl+C to stop the bot"
echo ""

# Run the bot
python3 -c "
import sys
sys.path.append('src')
import asyncio
from telegram.ultimate_telegram_bot import UltimateTelegramBot

async def main():
    bot = UltimateTelegramBot()
    await bot.auto_start()

if __name__ == '__main__':
    asyncio.run(main())
"
