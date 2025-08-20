#!/data/data/com.termux/files/usr/bin/bash

# 🚨 QUICK FIX untuk Error Event Loop
# Fix semua masalah yang ditemukan di debug

clear
echo "🚨========================================"
echo "⚡ QUICK FIX - Event Loop & Missing Files"
echo "🔧 Fix untuk HP Android Termux"
echo "========================================"
echo ""

cd ~/UjiCoba

echo "🔧 Step 1: Create missing .env file..."
cat > .env << 'EOF'
# 🤖 BackupHpDriveOtomatis-Termux Configuration
# Generated: 2025-08-21

# Telegram Bot
TELEGRAM_BOT_TOKEN=8224682609:AAFgmCwvosC9pJSkj73oXQ5a669YaFM7mHM
ALLOWED_USER_IDS=6600484135

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

echo "✅ .env file created"

echo ""
echo "📁 Step 2: Create missing directories..."
mkdir -p credentials logs temp
echo "✅ Directories created"

echo ""
echo "🔧 Step 3: Fix permissions..."
chmod +x scripts/*.sh
chmod +x *.sh
echo "✅ Permissions fixed"

echo ""
echo "🛑 Step 4: Kill any running processes..."
pkill -f python 2>/dev/null || echo "   No processes to kill"
pkill -f bot 2>/dev/null || echo "   No bot processes"
sleep 2

echo ""
echo "🧹 Step 5: Clear temp files..."
rm -rf temp/* 2>/dev/null
rm -rf logs/*.log 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null
echo "✅ Cleanup complete"

echo ""
echo "🧪 Step 6: Test bot import..."
python -c "
import sys
sys.path.insert(0, 'src')
try:
    from telegram.termux_telegram_bot import TermuxTelegramBot
    print('✅ Bot import: OK')
except Exception as e:
    print(f'❌ Bot import failed: {e}')
"

echo ""
echo "🚀 Step 7: Start bot dengan event loop fix..."
echo "📱 Bot akan start sekarang..."
echo "⚠️  Press Ctrl+C untuk stop bot"
echo ""

# Start bot dengan proper event loop handling
python3 << 'PYTHON_SCRIPT'
import sys
import os
import asyncio
import signal

# Add src to path
sys.path.insert(0, 'src')
os.chdir('/data/data/com.termux/files/home/UjiCoba')

def signal_handler(sig, frame):
    print("\n⏹️ Bot stopped by user")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

async def main():
    try:
        from telegram.termux_telegram_bot import TermuxTelegramBot
        
        print("🤖 Starting Termux Telegram Bot...")
        bot = TermuxTelegramBot()
        await bot.auto_start()
        
    except KeyboardInterrupt:
        print("\n⏹️ Bot stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("👋 Cleanup complete")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Final error: {e}")
PYTHON_SCRIPT

echo ""
echo "🏁 Quick fix complete!"
