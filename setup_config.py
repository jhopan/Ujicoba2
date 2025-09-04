#!/usr/bin/env python3
"""
🛠️ Setup Configuration Script
Otomatis membuat file konfigurasi yang dibutuhkan untuk quick install
"""

import os
import json
from pathlib import Path

def create_env_file():
    """Buat file .env dari template"""
    project_root = Path(__file__).parent
    env_example = project_root / "config" / ".env.example"
    env_file = project_root / ".env"
    
    if env_file.exists():
        print("✅ File .env sudah ada")
        return
    
    if env_example.exists():
        # Copy template dan berikan instruksi
        content = env_example.read_text()
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("📝 File .env dibuat dari template")
        print("⚠️  WAJIB EDIT file .env dengan nilai yang benar:")
        print("   - TELEGRAM_BOT_TOKEN (dari @BotFather)")
        print("   - ALLOWED_USER_IDS (dari @userinfobot)")
    else:
        # Buat .env basic
        content = """# 🤖 Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
ALLOWED_USER_IDS=your_user_id_here
AUTO_DELETE_AFTER_UPLOAD=false
MAX_FILE_SIZE=104857600
ORGANIZE_BY_DATE=true
UNLIMITED_ACCOUNTS=true
MAX_ACCOUNTS=20
SETUP_COMPLETED=false
PLATFORM=termux
"""
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("📝 File .env dibuat dengan template basic")

def create_default_configs():
    """Buat file konfigurasi default"""
    project_root = Path(__file__).parent
    config_dir = project_root / "config"
    config_dir.mkdir(exist_ok=True)
    
    # accounts.json
    accounts_file = config_dir / "accounts.json"
    if not accounts_file.exists():
        accounts_config = {
            "accounts": [],
            "last_updated": "",
            "max_accounts": 20
        }
        with open(accounts_file, 'w') as f:
            json.dump(accounts_config, f, indent=2)
        print("📝 File config/accounts.json dibuat")
    
    # folders.json
    folders_file = config_dir / "folders.json"
    if not folders_file.exists():
        folders_config = {
            "folders": {
                "Documents": "/storage/emulated/0/Documents",
                "Pictures": "/storage/emulated/0/Pictures",
                "DCIM": "/storage/emulated/0/DCIM",
                "Download": "/storage/emulated/0/Download"
            },
            "last_updated": ""
        }
        with open(folders_file, 'w') as f:
            json.dump(folders_config, f, indent=2)
        print("📝 File config/folders.json dibuat dengan folder default")
    
    # settings.json
    settings_file = config_dir / "settings.json"
    if not settings_file.exists():
        settings_config = {
            "backup": {
                "auto_schedule": True,
                "schedule_time": "00:00",
                "max_file_size": 104857600,
                "retry_attempts": 3,
                "delete_after_upload": False,
                "compress_files": False
            },
            "notifications": {
                "send_progress": True,
                "send_completion": True,
                "send_errors": True
            }
        }
        with open(settings_file, 'w') as f:
            json.dump(settings_config, f, indent=2)
        print("📝 File config/settings.json dibuat")

def create_credentials_structure():
    """Buat struktur folder credentials"""
    project_root = Path(__file__).parent
    cred_dir = project_root / "credentials"
    cred_dir.mkdir(exist_ok=True)
    
    # Buat file README dengan instruksi
    readme_file = cred_dir / "README.md"
    readme_content = """# 🔐 Credentials Directory

## File yang dibutuhkan:

### 1. google_credentials.json (WAJIB)
```
File OAuth credentials dari Google Cloud Console
- Buka https://console.cloud.google.com/
- Buat project baru atau pilih yang ada
- Enable Google Drive API
- Buat OAuth 2.0 credentials
- Download sebagai google_credentials.json
```

### 2. Token files (dibuat otomatis)
```
token_account_0.json  # Akun Google pertama (dibuat otomatis)
token_account_1.json  # Akun Google kedua (dibuat otomatis)
token_account_2.json  # Akun Google ketiga (dibuat otomatis)
```

## ⚠️ PENTING:
- JANGAN commit file credentials ke repository!
- Simpan backup credentials di tempat aman
- File token akan dibuat otomatis saat setup akun Google
"""
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("📝 File credentials/README.md dibuat dengan instruksi")

def create_quick_setup_script():
    """Buat script quick setup untuk Termux"""
    project_root = Path(__file__).parent
    
    script_content = '''#!/bin/bash
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
'''
    
    script_file = project_root / "quick_setup.sh"
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(script_content)
    os.chmod(script_file, 0o755)  # Make executable
    print("📝 File quick_setup.sh dibuat")

def main():
    """Jalankan semua setup"""
    print("🛠️ Setup Configuration Script")
    print("=" * 40)
    
    # Buat semua file yang dibutuhkan
    create_env_file()
    create_default_configs()
    create_credentials_structure()
    create_quick_setup_script()
    
    print("\n✅ SETUP SELESAI!")
    print("\n📋 YANG PERLU ANDA LAKUKAN:")
    print("1. Edit file .env:")
    print("   - Isi TELEGRAM_BOT_TOKEN dari @BotFather")
    print("   - Isi ALLOWED_USER_IDS dari @userinfobot")
    print("\n2. Tambahkan file credentials/google_credentials.json:")
    print("   - Download dari Google Cloud Console")
    print("   - Enable Google Drive API terlebih dahulu")
    print("\n3. Di HP/Termux jalankan:")
    print("   chmod +x quick_setup.sh")
    print("   ./quick_setup.sh")
    print("\n4. Jalankan bot:")
    print("   python3 main.py")

if __name__ == "__main__":
    main()
