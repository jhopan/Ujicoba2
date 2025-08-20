#!/bin/bash

# Quick Start Script for Advanced Backup System
# This script demonstrates the system functionality

echo "🚀 Advanced Backup System - Quick Start Demo"
echo "============================================="

# Check if we're in the right directory
if [ ! -f "src/main.py" ]; then
    echo "❌ Error: Please run this script from the backup_system directory"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "📝 Creating example .env file..."
    cat > .env << 'EOF'
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
ALLOWED_USER_IDS=your_telegram_user_id_here

# Backup Configuration
BACKUP_BASE_DIR=/data/data/com.termux/files/home/backups
MAX_FILE_SIZE=104857600
AUTO_DELETE_AFTER_UPLOAD=false
COMPRESS_FILES=false

# Storage Configuration  
MAX_STORAGE_PER_ACCOUNT=16106127360
STORAGE_WARNING_THRESHOLD=0.9

# Network Configuration
CONNECTION_TIMEOUT=30
UPLOAD_TIMEOUT=300
MAX_CONCURRENT_UPLOADS=3

# Logging Configuration
LOG_LEVEL=INFO
LOG_TO_FILE=true
LOG_TO_TELEGRAM=true

# Paths to monitor (comma-separated)
MONITOR_PATHS=/data/data/com.termux/files/home/storage/shared/Download,/data/data/com.termux/files/home/storage/shared/Pictures,/data/data/com.termux/files/home/storage/shared/Documents

# Schedule Configuration
BACKUP_SCHEDULE_TIME=00:00
AUTO_BACKUP_ENABLED=true
EOF
    
    echo "✅ Created .env file with default settings"
    echo "📝 Please edit .env file with your actual tokens:"
    echo "   nano .env"
    echo ""
fi

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p logs
mkdir -p credentials  
mkdir -p backups
mkdir -p temp

# Check Python installation
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ Python is not installed. Please install Python first."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "🐍 Using Python: $PYTHON_CMD"

# Check and install dependencies
echo "📦 Checking dependencies..."
if [ -f "requirements.txt" ]; then
    echo "Installing Python packages..."
    $PYTHON_CMD -m pip install -r requirements.txt
else
    echo "⚠️ requirements.txt not found, installing essential packages..."
    $PYTHON_CMD -m pip install python-telegram-bot aiohttp python-dotenv
fi

# Check .env configuration
echo "⚙️ Checking configuration..."
if grep -q "your_bot_token_here" .env; then
    echo "⚠️ Warning: Telegram bot token not configured"
    echo "📝 Please edit .env file and add your bot token"
    echo "🤖 Create a bot: https://t.me/BotFather"
    echo ""
fi

if grep -q "your_telegram_user_id_here" .env; then
    echo "⚠️ Warning: Telegram user ID not configured"  
    echo "📱 Get your ID: https://t.me/userinfobot"
    echo ""
fi

# Function to show system status
show_status() {
    echo "📊 System Status:"
    echo "=================="
    
    # Check if database exists
    if [ -f "backup_system.db" ]; then
        echo "✅ Database: Ready"
    else
        echo "⭕ Database: Not initialized"
    fi
    
    # Check log directory
    if [ -d "logs" ]; then
        log_count=$(ls -1 logs/ 2>/dev/null | wc -l)
        echo "📝 Logs: $log_count files in logs/"
    else
        echo "📝 Logs: Directory not found"
    fi
    
    # Check credentials
    if [ -d "credentials" ] && [ "$(ls -A credentials 2>/dev/null)" ]; then
        cred_count=$(ls -1 credentials/ 2>/dev/null | wc -l)
        echo "🔐 Credentials: $cred_count files found"
    else
        echo "🔐 Credentials: No credential files found"
    fi
    
    echo ""
}

# Function to run a quick test
run_test() {
    echo "🧪 Running system test..."
    
    $PYTHON_CMD -c "
import sys
sys.path.insert(0, 'src')

try:
    from utils.enhanced_settings import EnhancedSettings
    from database_manager import DatabaseManager
    
    print('✅ Settings module: OK')
    print('✅ Database module: OK')
    
    settings = EnhancedSettings()
    db = DatabaseManager()
    
    print('✅ Settings initialization: OK')
    print('✅ Database initialization: OK')
    
    print('📊 Settings summary:')
    print(f\"  Auto backup: {settings.get('backup.auto_schedule')}\"")
    print(f\"  Schedule time: {settings.get('backup.schedule_time')}\"")
    print(f\"  Max file size: {settings.get('backup.max_file_size')} bytes\"")
    
except ImportError as e:
    print(f'❌ Import error: {e}')
    print('💡 Try: pip install -r requirements.txt')
except Exception as e:
    print(f'❌ Error: {e}')
"
}

# Main menu
while true; do
    echo ""
    echo "🎯 What would you like to do?"
    echo "1. 🚀 Start the backup system"
    echo "2. 📊 Show system status"
    echo "3. 🧪 Run system test"
    echo "4. 📝 Edit configuration"
    echo "5. 📋 View logs"
    echo "6. 🔧 Install missing dependencies"
    echo "7. 📖 Show help"
    echo "8. ❌ Exit"
    echo ""
    read -p "Choose option (1-8): " choice
    
    case $choice in
        1)
            echo "🚀 Starting backup system..."
            echo "📱 Use your Telegram bot to control the system"
            echo "🛑 Press Ctrl+C to stop"
            echo ""
            $PYTHON_CMD src/main.py
            ;;
        2)
            show_status
            ;;
        3)
            run_test
            ;;
        4)
            if command -v nano &> /dev/null; then
                nano .env
            elif command -v vim &> /dev/null; then
                vim .env
            else
                echo "📝 Please edit .env file with your preferred editor"
                echo "📄 File location: $(pwd)/.env"
            fi
            ;;
        5)
            if [ -f "logs/backup.log" ]; then
                echo "📋 Recent log entries:"
                echo "====================="
                tail -20 logs/backup.log
            else
                echo "📝 No log file found. Run the system first."
            fi
            ;;
        6)
            echo "🔧 Installing/updating dependencies..."
            $PYTHON_CMD -m pip install --upgrade pip
            $PYTHON_CMD -m pip install -r requirements.txt
            ;;
        7)
            cat << 'EOF'
📖 Advanced Backup System Help
==============================

🚀 Quick Start:
1. Edit .env file with your Telegram bot token
2. Add your Telegram user ID to .env
3. Start the system (option 1)
4. Use your Telegram bot to control backups

🤖 Telegram Bot Commands:
• /start - Show main menu
• /backup - Start backup
• /status - Show system status
• /accounts - Manage Google Drive accounts
• /settings - Configure system

🔧 Setup Requirements:
• Python 3.7+
• Telegram bot token (from @BotFather)
• Google Drive API credentials
• Internet connection

📁 Directory Structure:
• src/ - Source code
• logs/ - Log files
• credentials/ - Google Drive credentials
• .env - Configuration file

💡 Tips:
• Keep your bot token secure
• Test with small files first
• Monitor logs for issues
• Use /status command regularly

🆘 Troubleshooting:
• Check .env configuration
• Verify internet connection
• Review logs/backup.log
• Ensure Google Drive API is enabled
EOF
            ;;
        8)
            echo "👋 Goodbye! Thanks for using Advanced Backup System"
            exit 0
            ;;
        *)
            echo "❌ Invalid option. Please choose 1-8."
            ;;
    esac
done
