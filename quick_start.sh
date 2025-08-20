#!/bin/bash

# 🚀 QUICK START - Advanced Backup System
# One-command setup untuk Android Termux

clear
echo "=================================================="
echo "🚀 ADVANCED BACKUP SYSTEM - QUICK START"
echo "📱 Android Termux with Telegram Bot Interface"
echo "=================================================="
echo ""

# Check if in Termux
if [[ ! "$PREFIX" == *"com.termux"* ]]; then
    echo "⚠️  This script is optimized for Termux"
    echo "📱 Install Termux from Google Play Store"
    echo ""
    read -p "Continue anyway? (y/n): " continue_anyway
    if [[ "$continue_anyway" != "y" ]]; then
        exit 1
    fi
fi

echo "🔍 Checking environment..."

# Install git if needed
if ! command -v git &> /dev/null; then
    echo "📦 Installing git..."
    pkg install git -y
fi

# Install Python if needed  
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "🐍 Installing Python..."
    pkg install python -y
fi

echo "✅ Environment ready"
echo ""

# Ask for installation method
echo "🎯 Choose installation method:"
echo "1. Auto-install (recommended)"
echo "2. Manual setup"
echo ""
read -p "Choice (1 or 2): " install_choice

if [[ "$install_choice" == "1" ]]; then
    # Auto install
    echo "🚀 Starting auto-installation..."
    
    if [ -f "scripts/install_termux.sh" ]; then
        chmod +x scripts/install_termux.sh
        ./scripts/install_termux.sh
    else
        echo "❌ Installer not found. Using manual setup..."
        install_choice="2"
    fi
fi

if [[ "$install_choice" == "2" ]]; then
    # Manual setup
    echo "🔧 Manual setup..."
    
    # Install dependencies
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    
    # Setup storage access
    echo "🗃️ Setting up storage access..."
    termux-setup-storage
    
    # Create directories
    mkdir -p credentials logs
    
    # Copy config
    if [ -f "config/.env.example" ]; then
        cp config/.env.example .env
        echo "⚙️ Config template created (.env)"
    fi
    
    echo "✅ Manual setup complete"
fi

echo ""
echo "=================================================="
echo "🎉 INSTALLATION COMPLETE!"
echo "=================================================="
echo ""
echo "📋 Next steps:"
echo ""
echo "1️⃣  Create Telegram Bot:"
echo "   - Open Telegram, message @BotFather"
echo "   - Send: /newbot"
echo "   - Copy bot token"
echo ""
echo "2️⃣  Get User ID:"
echo "   - Message @userinfobot"
echo "   - Copy your user ID"
echo ""
echo "=========================================="
echo "🔧 INTERACTIVE BOT SETUP"
echo "=========================================="
echo ""

# Check if .env already configured
if [ ! -f ".env" ] || ! grep -q "TELEGRAM_BOT_TOKEN=" .env || grep -q "your_bot_token" .env; then
    echo "📋 STEP 3: Create Telegram Bot"
    echo "1. Buka Telegram, cari @BotFather"
    echo "2. Kirim: /newbot"
    echo "3. Ikuti instruksi untuk buat bot"
    echo "4. Copy token yang diberikan"
    echo ""
    
    # Ask for bot token
    while true; do
        read -p "🔑 Paste Bot Token di sini: " BOT_TOKEN
        if [[ "$BOT_TOKEN" =~ ^[0-9]+:[A-Za-z0-9_-]+$ ]]; then
            break
        else
            echo "❌ Format token tidak valid. Coba lagi."
            echo "💡 Format: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
        fi
    done
    
    echo ""
    echo "� STEP 4: Get User ID"
    echo "1. Buka Telegram, cari @userinfobot"
    echo "2. Kirim: /start"
    echo "3. Copy User ID yang diberikan (angka saja)"
    echo ""
    
    # Ask for user ID
    while true; do
        read -p "👤 Paste User ID di sini: " USER_ID
        if [[ "$USER_ID" =~ ^[0-9]+$ ]]; then
            break
        else
            echo "❌ User ID harus berupa angka saja. Coba lagi."
        fi
    done
    
    # Create .env file
    echo "💾 Menyimpan konfigurasi..."
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

# Setup Status
SETUP_COMPLETED=true
PLATFORM=termux
EOF
    
    echo "✅ Konfigurasi tersimpan!"
else
    echo "✅ Bot sudah dikonfigurasi sebelumnya"
fi

echo ""
echo "=========================================="
echo "🚀 STARTING BOT"
echo "=========================================="
echo ""
echo "💡 Bot akan start sekarang..."
echo "📱 Buka Telegram dan kirim /start ke bot Anda"
echo "⚠️  Press Ctrl+C untuk stop bot"
echo ""

# Countdown
for i in {3..1}; do
    echo -ne "⏰ Starting in $i seconds... \r"
    sleep 1
done

echo ""
echo "🚀 Starting bot..."

if [ -f "scripts/start_bot.sh" ]; then
    chmod +x scripts/start_bot.sh
    ./scripts/start_bot.sh
elif [ -f "run_bot.sh" ]; then
    chmod +x run_bot.sh
    ./run_bot.sh
elif [ -f "main.py" ]; then
    python main.py
else
    echo "❌ No startup script found"
    echo "💡 Run: python src/telegram/termux_telegram_bot.py"
fi
