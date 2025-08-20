#!/data/data/com.termux/files/usr/bin/bash

# 🚀 Ultimate Backup System - Termux Auto Installer
# 📱 Khusus untuk Android Termux
# ⚡ One-command installation

echo "🚀========================================"
echo "🤖 ULTIMATE BACKUP SYSTEM - TERMUX"
echo "📱 Auto installer untuk Android"
echo "========================================"

echo ""
echo "📦 Step 1: Update Termux..."
pkg update -y && pkg upgrade -y

echo ""
echo "🐍 Step 2: Install Python & Tools..."
pkg install -y python python-pip git curl wget openssh libffi openssl libjpeg-turbo libcrypt nano which tree htop

echo ""
echo "📁 Step 3: Setup Storage Access..."
echo "⚠️  PENTING: Klik 'Allow' saat muncul permission popup!"
termux-setup-storage
sleep 3

echo ""
echo "📦 Step 4: Install Python Packages..."
pip install --upgrade pip

echo "🤖 Installing Telegram Bot..."
pip install python-telegram-bot>=20.0

echo "☁️ Installing Google Drive API..."
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib google-auth

echo "🔄 Installing Async Operations..."
pip install aiofiles aiohttp asyncio-throttle

echo "⚙️ Installing Configuration Tools..."
pip install python-dotenv pyyaml

echo "🌐 Installing Network Tools..."
pip install requests urllib3 certifi

echo "📅 Installing Date/Time Tools..."
pip install python-dateutil

echo "📝 Installing Logging..."
pip install colorlog

echo "🖼️ Installing File Processing..."
pip install Pillow

echo "📊 Installing Monitoring..."
pip install tqdm psutil

echo "⏰ Installing Scheduler..."
pip install schedule

echo ""
echo "📁 Step 5: Create Project Structure..."
mkdir -p ~/backup_system/{src/telegram,credentials,backups,logs,temp,config,utils}

echo ""
echo "✅ Step 6: Verify Installation..."
python3 -c "import telegram; print('✅ Telegram Bot OK')" 2>/dev/null || echo "⚠️ Telegram: Check needed"
python3 -c "import googleapiclient; print('✅ Google API OK')" 2>/dev/null || echo "⚠️ Google API: Check needed"
python3 -c "import aiofiles; print('✅ Async Files OK')" 2>/dev/null || echo "⚠️ Async: Check needed"

echo ""
echo "🎉 INSTALLATION COMPLETE!"
echo ""
echo "🚀 Next Steps:"
echo "1. cd ~/backup_system"
echo "2. ./start_bot.sh"
echo "3. Follow setup wizard"
echo "4. Upload Google Drive credentials"
echo "5. Open your Telegram bot and send /start"
echo ""
echo "📱 Happy Backing Up!"
