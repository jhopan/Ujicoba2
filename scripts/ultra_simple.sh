#!/data/data/com.termux/files/usr/bin/bash

# 🚀 ULTRA SIMPLE BOT START
# No async, no complex error handling, just start bot

clear
echo "🚀========================================"
echo "⚡ ULTRA SIMPLE BOT START"
echo "🎯 Direct bot execution"
echo "========================================"
echo ""

cd ~/UjiCoba

# Kill any existing python processes
echo "🛑 Killing existing processes..."
pkill -f python >/dev/null 2>&1
sleep 1

# Ensure .env exists with minimal config
echo "📝 Ensuring config exists..."
cat > .env << 'EOF'
TELEGRAM_BOT_TOKEN=8224682609:AAFgmCwvosC9pJSkj73oXQ5a669YaFM7mHM
ALLOWED_USER_IDS=6600484135
SETUP_COMPLETED=true
EOF

mkdir -p credentials logs temp

echo "🚀 Starting bot..."
echo "📱 Bot akan start tanpa komplexitas..."
echo "⚠️  Press Ctrl+C untuk stop"
echo ""

# Method 1: Try Python with minimal complexity
export PYTHONPATH="src:$PYTHONPATH"
cd src/telegram

echo "🎯 Method 1: Direct python execution..."
python3 -c "
import asyncio
import sys
import os

# Simple bot starter
sys.path.insert(0, '..')
os.chdir('../..')

try:
    from telegram.termux_telegram_bot import TermuxTelegramBot
    
    async def simple_start():
        bot = TermuxTelegramBot()
        
        # Check if setup needed
        env_file = '../../.env'
        if not os.path.exists(env_file) or not bot._is_setup_complete():
            print('Setup required, but skipping for simplicity')
            return
        
        print('Starting normal bot...')
        await bot._run_termux_bot()
    
    # Run without complex signal handling
    asyncio.run(simple_start())
    
except KeyboardInterrupt:
    print('\n⏹️ Bot stopped')
except Exception as e:
    print(f'❌ Error: {e}')
    print('💡 Try: python3 termux_telegram_bot.py')
"

echo ""
echo "🏁 Bot execution finished"
