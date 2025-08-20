#!/data/data/com.termux/files/usr/bin/bash

# 🚀 Simple Bot Launcher - BackupHpDriveOtomatis-Termux
# 📱 Direct launcher for Termux

echo "🚀 BACKUP HP KE DRIVE OTOMATIS"
echo "📱 Starting Termux Telegram Bot..."
echo "========================================"

# Go to project root
cd "$(dirname "$0")"

# Check if bot file exists
if [ -f "src/telegram/termux_telegram_bot.py" ]; then
    echo "✅ Found termux_telegram_bot.py"
    cd src/telegram
    python3 termux_telegram_bot.py
else
    echo "❌ Bot file not found!"
    echo "💡 Expected: src/telegram/termux_telegram_bot.py"
    exit 1
fi
