#!/data/data/com.termux/files/usr/bin/bash

# 🚀 Simple Bot Launcher - BackupHpDriveOtomatis-Termux
# 📱 Direct launcher untuk bypass import issues

echo "🚀 BACKUP HP KE DRIVE OTOMATIS"
echo "📱 Starting bot..."

# Go to correct directory
cd "$(dirname "$0")/.."

# Check if bot exists
if [ -f "src/telegram/termux_telegram_bot.py" ]; then
    echo "✅ Found termux_telegram_bot.py"
    BOT_FILE="src/telegram/termux_telegram_bot.py"
elif [ -f "src/telegram/ultimate_telegram_bot.py" ]; then
    echo "✅ Found ultimate_telegram_bot.py"  
    BOT_FILE="src/telegram/ultimate_telegram_bot.py"
else
    echo "❌ No bot file found!"
    echo "📁 Available files:"
    ls -la src/telegram/
    exit 1
fi

# Check if config exists
if [ ! -f ".env" ]; then
    echo "⚙️ No config found. Creating basic config..."
    
    echo "📋 Setup Bot Token & User ID:"
    echo ""
    echo "1. Buka Telegram → cari @BotFather"
    echo "2. Send: /newbot → ikuti instruksi"
    echo "3. Copy bot token"
    echo ""
    
    read -p "🔑 Bot Token: " BOT_TOKEN
    
    echo ""
    echo "4. Buka Telegram → cari @userinfobot"  
    echo "5. Send: /start → copy User ID"
    echo ""
    
    read -p "👤 User ID: " USER_ID
    
    # Create .env
    cat > .env << EOF
TELEGRAM_BOT_TOKEN=$BOT_TOKEN
ALLOWED_USER_IDS=$USER_ID
AUTO_DELETE_AFTER_UPLOAD=false
UNLIMITED_ACCOUNTS=true
SETUP_COMPLETED=true
EOF
    
    echo "✅ Config saved!"
fi

echo ""
echo "🚀 Starting bot..."
echo "💡 Buka Telegram dan kirim /start ke bot"
echo ""

# Set Python path and run
export PYTHONPATH="$PWD/src:$PYTHONPATH"
python3 "$BOT_FILE"
