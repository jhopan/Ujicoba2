#!/bin/bash
# 🚀 TERMUX QUICK INSTALL - One Command Setup

clear
echo "=================================================="
echo "🚀 TERMUX TELEGRAM BOT - QUICK INSTALL"
echo "📱 Siap pakai untuk backup otomatis ke Google Drive"
echo "=================================================="
echo ""

# Cek apakah di Termux
if [[ ! "$PREFIX" == *"com.termux"* ]]; then
    echo "⚠️  Script ini dioptimalkan untuk Termux"
    echo "📱 Install Termux dari Google Play Store"
    echo ""
    read -p "Lanjutkan? (y/n): " continue_anyway
    if [[ "$continue_anyway" != "y" ]]; then
        exit 1
    fi
fi

echo "🔍 Memulai instalasi..."

# Update dan install packages
echo "📦 Update packages..."
pkg update -y && pkg upgrade -y

echo "📦 Install dependencies..."
pkg install python git wget curl -y

# Setup storage access
echo "📱 Setup akses storage..."
termux-setup-storage
sleep 2

# Install Python packages
echo "🐍 Install Python dependencies..."
pip install --upgrade pip

# Install core packages one by one untuk better error handling
echo "📦 Installing telegram bot..."
pip install python-telegram-bot

echo "📦 Installing Google APIs..."
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

echo "📦 Installing utilities..."
pip install python-dotenv pyyaml aiofiles schedule

# Optional packages (skip if error)
echo "📦 Installing optional packages..."
pip install aiohttp || echo "⚠️ aiohttp installation skipped"
pip install psutil || echo "⚠️ psutil installation skipped"

# Setup konfigurasi
echo "🛠️ Setup konfigurasi..."
python3 setup_config.py

# Cek konfigurasi
echo "🔍 Validasi setup..."
python3 check_setup.py

echo ""
echo "✅ INSTALASI SELESAI!"
echo ""
echo "📋 LANGKAH TERAKHIR:"
echo "1. Edit file .env dengan data Anda:"
echo "   nano .env"
echo ""
echo "2. Tambahkan file google_credentials.json:"
echo "   - Download dari Google Cloud Console"
echo "   - Simpan di folder credentials/"
echo ""
echo "3. Validasi setup:"
echo "   python3 check_setup.py"
echo ""
echo "4. Jalankan bot:"
echo "   python3 main.py"
echo ""
echo "🎉 Bot siap digunakan!"
