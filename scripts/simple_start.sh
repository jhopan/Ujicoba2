#!/data/data/com.termux/files/usr/bin/bash

# 🚀 SIMPLE BOT STARTER
# Start bot langsung tanpa komplikasi

clear
echo "🚀========================================"
echo "🤖 SIMPLE BOT STARTER"
echo "📱 Start bot langsung tanpa ribet"
echo "========================================"
echo ""

cd ~/UjiCoba

echo "🔧 Step 1: Setup basic requirements..."

# Ensure .env exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cat > .env << 'EOF'
TELEGRAM_BOT_TOKEN=8224682609:AAFgmCwvosC9pJSkj73oXQ5a669YaFM7mHM
ALLOWED_USER_IDS=6600484135
SETUP_COMPLETED=true
PLATFORM=termux
EOF
    echo "✅ .env created"
fi

# Ensure directories exist
mkdir -p credentials logs temp
echo "✅ Directories ready"

echo ""
echo "🛑 Step 2: Kill any existing processes..."
pkill -f python 2>/dev/null || echo "   No processes to kill"
sleep 2

echo ""
echo "🚀 Step 3: Start bot dengan method sederhana..."
echo "📱 Bot akan start sekarang..."
echo "⚠️  Press Ctrl+C untuk stop"
echo ""

# Simple direct bot start
cd src/telegram
python3 termux_telegram_bot.py

echo ""
echo "🏁 Bot stopped"
