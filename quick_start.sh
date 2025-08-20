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
echo "3️⃣  Start Bot:"
echo "   ./scripts/start_bot.sh"
echo "   OR"
echo "   python main.py"
echo ""
echo "4️⃣  Setup via Bot:"
echo "   - Send /start to your bot"
echo "   - Follow setup wizard"
echo "   - Upload Google Drive credentials"
echo ""
echo "🚀 Quick start commands:"
echo "   chmod +x scripts/start_bot.sh"
echo "   ./scripts/start_bot.sh"
echo ""

# Ask if want to start now
read -p "🤖 Start bot now? (y/n): " start_now

if [[ "$start_now" == "y" ]]; then
    echo ""
    echo "🚀 Starting bot..."
    
    if [ -f "scripts/start_bot.sh" ]; then
        chmod +x scripts/start_bot.sh
        ./scripts/start_bot.sh
    elif [ -f "main.py" ]; then
        python main.py
    else
        echo "❌ No startup script found"
        echo "💡 Run: python src/telegram/termux_telegram_bot.py"
    fi
else
    echo ""
    echo "👋 Setup complete! Run the bot when ready:"
    echo "   ./scripts/start_bot.sh"
fi
