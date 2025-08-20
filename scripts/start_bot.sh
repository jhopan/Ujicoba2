#!/data/data/com.termux/files/usr/bin/bash

# 🚀 BackupHpDriveOtomatis-Termux - Start Bot
# 📱 Simple bot starter for Android Termux

echo "🤖========================================"
echo "🚀 BACKUP HP KE DRIVE OTOMATIS"
echo "📱 Starting Telegram Bot..."
echo "========================================"

# Go to project root
cd "$(dirname "$0")/.."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found!"
    echo "📦 Please run: pkg install python"
    exit 1
fi

echo "✅ Python3 found"

# Check if bot file exists
if [ -f "src/telegram/termux_telegram_bot.py" ]; then
    echo "✅ Found termux_telegram_bot.py"
    echo "🚀 Starting bot..."
    cd src/telegram
    python3 termux_telegram_bot.py
else
    echo "❌ Bot file not found!"
    echo "💡 Expected: src/telegram/termux_telegram_bot.py"
    exit 1
fi
