#!/data/data/com.termux/files/usr/bin/bash

# 🚨 EMERGENCY RESTART SCRIPT
# Use this when bot is stuck or has event loop issues

clear
echo "🚨========================================"
echo "⛑️  EMERGENCY RESTART"
echo "🔧 Fix event loop & bot issues"
echo "========================================"
echo ""

echo "🛑 Step 1: Stopping all processes..."
# Kill all python processes safely
pkill -f python 2>/dev/null || echo "   No Python processes found"
pkill -f bot 2>/dev/null || echo "   No bot processes found"
pkill -f telegram 2>/dev/null || echo "   No telegram processes found"

echo "⏳ Waiting for cleanup..."
sleep 3

echo "🧹 Step 2: Clearing temp files..."
# Clear temporary files and logs that might cause issues
rm -rf temp/* 2>/dev/null || echo "   Temp folder empty"
rm -rf logs/*.log 2>/dev/null || echo "   No logs to clear"

# Clear Python cache that might be corrupted
find . -name "*.pyc" -delete 2>/dev/null
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null

echo "🔍 Step 3: Checking system..."
# Check if essential commands exist
if ! command -v python &> /dev/null; then
    echo "❌ Python not found! Installing..."
    pkg install python -y
fi

if ! command -v pip &> /dev/null; then
    echo "❌ pip not found! Installing..."
    pkg install python-pip -y
fi

# Verify key packages
echo "📦 Checking packages..."
python -c "import telegram" 2>/dev/null && echo "   ✅ Telegram Bot library OK" || echo "   ⚠️ Telegram library needs reinstall"
python -c "import asyncio" 2>/dev/null && echo "   ✅ Asyncio OK" || echo "   ❌ Asyncio missing"

echo ""
echo "🚀 Step 4: Restarting bot..."
echo "📱 Bot akan restart dalam mode fresh"
echo "⚠️  Jika masih error, gunakan: ./quick_start.sh"
echo ""

# Give user option to continue
echo "Ready to restart? (y/n)"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "🔄 Restarting now..."
    echo ""
    
    # Try different startup methods
    if [ -f "main.py" ]; then
        echo "🎯 Starting main.py..."
        python main.py
    elif [ -f "src/telegram/termux_telegram_bot.py" ]; then
        echo "🎯 Starting bot directly..."
        python src/telegram/termux_telegram_bot.py
    elif [ -f "run_bot.sh" ]; then
        echo "🎯 Using run_bot.sh..."
        chmod +x run_bot.sh
        ./run_bot.sh
    else
        echo "❌ No startup script found"
        echo "💡 Try: ./quick_start.sh"
    fi
else
    echo "❌ Restart cancelled"
    echo "💡 Manual commands:"
    echo "   ./quick_start.sh    # Full setup"
    echo "   python main.py      # Direct start"
fi

echo ""
echo "🏁 Emergency restart complete"
