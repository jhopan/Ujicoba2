#!/usr/bin/env python3
"""
🔍 Setup Checker - Validasi konfigurasi sebelum menjalankan bot
"""

import os
import json
from pathlib import Path

def check_env_file():
    """Cek file .env"""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ File .env tidak ditemukan")
        print("   Jalankan: cp .env.template .env")
        return False
    
    # Cek isi .env
    content = env_file.read_text()
    
    if "your_bot_token_here" in content:
        print("❌ TELEGRAM_BOT_TOKEN belum diisi di file .env")
        return False
    
    if "your_user_id_here" in content:
        print("❌ ALLOWED_USER_IDS belum diisi di file .env")
        return False
    
    print("✅ File .env sudah dikonfigurasi")
    return True

def check_credentials():
    """Cek Google credentials"""
    cred_file = Path("credentials/google_credentials.json")
    
    if not cred_file.exists():
        print("❌ File credentials/google_credentials.json tidak ditemukan")
        print("   Download dari Google Cloud Console")
        return False
    
    # Cek format JSON
    try:
        with open(cred_file, 'r') as f:
            data = json.load(f)
        
        if "client_id" not in data.get("installed", {}):
            print("❌ Format google_credentials.json tidak valid")
            return False
            
    except json.JSONDecodeError:
        print("❌ File google_credentials.json bukan format JSON yang valid")
        return False
    
    print("✅ Google credentials sudah ada")
    return True

def check_dependencies():
    """Cek Python dependencies"""
    try:
        import telegram
        print("✅ python-telegram-bot tersedia")
    except ImportError:
        print("❌ python-telegram-bot tidak terinstall")
        print("   Jalankan: pip install python-telegram-bot")
        return False
    
    try:
        import googleapiclient
        print("✅ google-api-python-client tersedia")
    except ImportError:
        print("❌ google-api-python-client tidak terinstall")
        print("   Jalankan: pip install google-api-python-client")
        return False
    
    return True

def check_config_files():
    """Cek file konfigurasi"""
    config_files = [
        "config/accounts.json",
        "config/folders.json", 
        "config/settings.json"
    ]
    
    for file_path in config_files:
        if not Path(file_path).exists():
            print(f"❌ File {file_path} tidak ditemukan")
            print("   Jalankan: python setup_config.py")
            return False
    
    print("✅ File konfigurasi sudah ada")
    return True

def check_permissions():
    """Cek permission untuk Termux"""
    storage_path = Path("/storage/emulated/0")
    
    if storage_path.exists():
        if os.access(storage_path, os.R_OK):
            print("✅ Akses storage tersedia")
            return True
        else:
            print("❌ Tidak ada akses ke storage")
            print("   Jalankan: termux-setup-storage")
            return False
    else:
        print("⚠️  Path storage tidak ditemukan (mungkin bukan Termux)")
        return True

def main():
    """Jalankan semua pengecekan"""
    print("🔍 SETUP CHECKER")
    print("=" * 40)
    
    checks = [
        ("Environment File", check_env_file),
        ("Google Credentials", check_credentials),
        ("Python Dependencies", check_dependencies),
        ("Config Files", check_config_files),
        ("Storage Permissions", check_permissions)
    ]
    
    all_good = True
    
    for name, check_func in checks:
        print(f"\n📋 {name}:")
        if not check_func():
            all_good = False
    
    print("\n" + "=" * 40)
    
    if all_good:
        print("🎉 SEMUA KONFIGURASI SUDAH SIAP!")
        print("🚀 Bot siap dijalankan: python3 main.py")
    else:
        print("⚠️  ADA KONFIGURASI YANG BELUM SELESAI")
        print("📋 Selesaikan item di atas terlebih dahulu")

if __name__ == "__main__":
    main()
