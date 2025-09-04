#!/bin/bash
# 🚀 QUICK SETUP SCRIPT untuk Termux

echo "🚀 Starting quick setup..."

# Update packages
echo "📦 Updating packages..."
pkg update -y && pkg upgrade -y

# Install required packages
echo "📦 Installing required packages..."
pkg install python git wget curl -y

# Install Python packages
echo "🐍 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Setup storage access
echo "📱 Setting up storage access..."
termux-setup-storage

# Check configuration
echo "🔍 Checking configuration..."
python3 setup_config.py

echo ""
echo "✅ Quick setup completed!"
echo ""
echo "📋 LANGKAH SELANJUTNYA:"
echo "1. Edit file .env dengan bot token dan user ID Anda"
echo "2. Tambahkan file google_credentials.json di folder credentials/"
echo "3. Jalankan: python3 main.py"
echo ""
