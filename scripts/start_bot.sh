#!/data/data/com.termux/files/usr/bin/bash

# 🚀 BackupHpDriveOtomatis-Termux - Smart Launcher
# 📱 Launcher khusus untuk Android Termux dengan Interactive Setup

echo "🤖========================================"
echo "🚀 BACKUP HP KE DRIVE OTOMATIS"
echo "📱 Starting Smart Setup & Bot..."
echo "========================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found!"
    echo "📦 Please run: ./scripts/install_termux.sh first"
    exit 1
fi

echo "✅ Python3 found"

# Check if we're in the right directory and find bot file
BOT_FILE=""
if [ -f "src/telegram/termux_telegram_bot.py" ]; then
    BOT_FILE="src/telegram/termux_telegram_bot.py"
elif [ -f "src/telegram/ultimate_telegram_bot.py" ]; then
    BOT_FILE="src/telegram/ultimate_telegram_bot.py"
else
    echo "❌ Bot file not found!"
    echo "📁 Available files:"
    ls -la src/telegram/ 2>/dev/null || echo "   No src/telegram/ directory"
    echo ""
    echo "💡 Make sure you're in the project root directory"
    echo "   Try: cd ~/BackupHpDriveOtomatis-Termux"
    exit 1
fi

echo "✅ Bot file found: $BOT_FILE"

# Check if .env exists and configured
if [ ! -f ".env" ]; then
    echo "⚙️ Creating configuration file..."
    cp config/.env.example .env 2>/dev/null || echo "# Configuration file" > .env
fi

# Interactive setup if not configured
if ! grep -q "TELEGRAM_BOT_TOKEN=" .env || grep -q "your_bot_token" .env; then
    echo ""
    echo "🔧 INTERACTIVE SETUP REQUIRED"
    echo "========================================"
    echo ""
    echo "📋 STEP 1: Create Telegram Bot"
    echo "1. Open Telegram, search @BotFather"
    echo "2. Send: /newbot"
    echo "3. Follow instructions to create bot"
    echo "4. Copy the bot token"
    echo ""
    
    # Ask for bot token
    while true; do
        read -p "🔑 Paste your Bot Token: " BOT_TOKEN
        if [[ "$BOT_TOKEN" =~ ^[0-9]+:[A-Za-z0-9_-]+$ ]]; then
            break
        else
            echo "❌ Invalid token format. Try again."
        fi
    done
    
    echo ""
    echo "📋 STEP 2: Get User ID"
    echo "1. Open Telegram, search @userinfobot"
    echo "2. Send: /start"
    echo "3. Copy your User ID (numbers only)"
    echo ""
    
    # Ask for user ID
    while true; do
        read -p "👤 Paste your User ID: " USER_ID
        if [[ "$USER_ID" =~ ^[0-9]+$ ]]; then
            break
        else
            echo "❌ Invalid User ID format. Must be numbers only."
        fi
    done
    
    # Update .env file
    echo "💾 Saving configuration..."
    
    # Create or update .env
    cat > .env << EOF
# 🤖 BackupHpDriveOtomatis-Termux Configuration
# Generated: $(date)

# Telegram Bot
TELEGRAM_BOT_TOKEN=$BOT_TOKEN
ALLOWED_USER_IDS=$USER_ID

# Backup Settings
AUTO_DELETE_AFTER_UPLOAD=false
MAX_FILE_SIZE=104857600
ORGANIZE_BY_DATE=true

# Google Drive
UNLIMITED_ACCOUNTS=true
MAX_ACCOUNTS=20

# Termux Settings
BACKUP_BASE_DIR=/data/data/com.termux/files/home/backups
STORAGE_SHARED=/data/data/com.termux/files/home/storage/shared

# Setup Status
SETUP_COMPLETED=true
PLATFORM=termux
EOF
    
    echo "✅ Configuration saved!"
fi

echo ""
echo "🚀 STARTING BOT..."
echo "========================================"

# Set environment for Android
export PYTHONPATH="$PWD/src:$PYTHONPATH"
export ANDROID_DATA="/data"
export ANDROID_ROOT="/system"

echo "� Bot akan start sekarang..."
echo "� Buka Telegram dan kirim /start ke bot Anda"
echo "⚠️  Press Ctrl+C to stop the bot"
echo ""

# Run the bot with proper error handling
python3 "$BOT_FILE" 2>&1 || {
    echo ""
    echo "❌ Bot failed to start!"
    echo "🔧 Troubleshooting:"
    echo "1. Check internet connection"
    echo "2. Verify bot token in .env file"
    echo "3. Install missing packages: pip install -r requirements.txt"
    echo "4. Restart Termux and try again"
    exit 1
}
