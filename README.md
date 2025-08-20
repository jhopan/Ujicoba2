# 🚀 BackupHpDriveOtomatis-Termux

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot%20Ready-blue.svg)](https://core.telegram.org/bots)

**🤖 Sistem backup otomatis HP Android ke Google Drive dengan interface Telegram yang sangat user-friendly**

## ⭐ Highlights

- 🎯 **Super User-Friendly** - Click-click interface, tidak perlu hafal command
- ☁️ **Unlimited Storage** - Support multiple Google Drive accounts (15GB per akun)
- 📱 **Termux Optimized** - Khusus untuk Android, tidak perlu root
- 🗑️ **Smart Auto-Delete** - Toggle hapus file setelah backup sukses
- ⚡ **One-Command Install** - Setup dalam 2 menit

## 🎯 Siapa yang Perlu Tool Ini?

✅ **Pengguna Android** yang ingin backup file otomatis  
✅ **User Termux** yang butuh solusi backup simpel  
✅ **Yang punya banyak file** di HP dan butuh storage unlimited  
✅ **Yang males ribet** - tinggal click button aja  
✅ **Yang butuh auto-delete** untuk hemat storage HP  

## 📱 Demo Interface Bot

```
🤖 TERMUX BACKUP SYSTEM
📱 Android Backup dengan Unlimited Storage

👤 User: Jhosua Armando
📊 Status: ⚠️ Setup Needed
🗃️ Accounts: 0 Google Drive
📁 Folders: 0 monitored

🎯 Pilih menu:

[⚡ Setup Google Drive]
[👥 Google Drive] [📁 Folders]
[⚙️ Auto-Delete Setting] [📊 Status]
[💾 Manual Backup] [⏰ Schedule]
[📋 Logs] [❓ Help]
```

## ⚡ Instalasi Super Cepat

### Method 1: Auto Install (Recommended)
```bash
# Clone & auto install
git clone https://github.com/jhopan/BackupHpDriveOtomatis-Termux.git
cd BackupHpDriveOtomatis-Termux
chmod +x quick_start.sh
./quick_start.sh
```

**Setup akan otomatis minta:**
- 🔑 **Bot Token** - Dari @BotFather
- 👤 **User ID** - Dari @userinfobot

### Method 2: Manual Install
```bash
# Install dependencies
pkg update && pkg upgrade -y
pkg install python python-pip git -y

# Clone repository  
git clone https://github.com/jhopan/BackupHpDriveOtomatis-Termux.git
cd BackupHpDriveOtomatis-Termux

# Install packages
pip install -r requirements.txt

# Setup storage
termux-setup-storage

# Start bot
python main.py
```

## � Security Features

⚡ **Bot Token Required** - Hanya bot Anda yang bisa jalan  
👤 **User ID Protection** - Hanya Anda yang bisa akses bot  
�️ **No Public Access** - Bot pribadi, bukan untuk umum  

## 🚀 Quick Start Guide

1. **Buat Bot Telegram:**
   - Chat @BotFather → `/newbot`
   - Copy Bot Token

2. **Dapatkan User ID:**
   - Chat @userinfobot → `/start`
   - Copy User ID (angka)

3. **Jalankan Quick Install:**
   ```bash
   ./quick_start.sh
   ```

4. **Paste Token & User ID** saat diminta

5. **Done!** Bot langsung jalan dan siap dipakai
- **Smart Backup** - Hanya file yang berubah
- **Scheduled Backup** - Otomatis sesuai jadwal

### 📁 Setup Folder Mudah  
- 📥 **Downloads** - Add dengan 1 click
- 📸 **Pictures/DCIM** - Add dengan 1 click
- 📄 **Documents** - Add dengan 1 click
- 💬 **WhatsApp Media** - Add dengan 1 click
- 📝 **Custom Path** - Add path apapun

### ⚙️ Pengaturan Pintar
- 🗑️ **Auto-Delete Toggle** - On/off setelah upload
- 📏 **Batas Ukuran File** - Configure max size
- ⏰ **Pengaturan Jadwal** - Set waktu backup
- 🔔 **Notifikasi** - Update real-time

## 📊 Struktur Project

```
BackupHpDriveOtomatis-Termux/
├── 📁 src/                    # Source code
│   ├── 🤖 telegram/          # Telegram bot modules
│   ├── ☁️ backup_manager.py   # Backup engine
│   ├── 💾 database_manager.py # Database operations
│   └── 🔧 utils/             # Utility functions
├── 📚 docs/                   # Dokumentasi
│   ├── 📖 INSTALLATION_GUIDE.md
│   ├── 🤖 TERMUX_BOT_README.md
│   └── 📝 CHANGELOG.md
├── 🔧 scripts/               # Installation & startup scripts
│   ├── ⚡ install_termux.sh  # Auto installer
│   └── 🚀 start_bot.sh       # Bot launcher
├── ⚙️ config/                # Configuration files
│   └── 📄 .env.example       # Environment template
├── 🔐 credentials/           # Google Drive credentials
├── 📊 logs/                  # Application logs
└── 📋 requirements.txt       # Python dependencies
```

## 🛠️ Konfigurasi Lanjutan

### Environment Variables
```env
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token
ALLOWED_USER_IDS=your_user_id

# Pengaturan Backup
AUTO_DELETE_AFTER_UPLOAD=false
MAX_FILE_SIZE=104857600
ORGANIZE_BY_DATE=true

# Google Drive
UNLIMITED_ACCOUNTS=true
MAX_ACCOUNTS=20
```

## 🔧 Troubleshooting

### Masalah Umum

**Bot tidak respond:**
```bash
# Restart bot
./scripts/start_bot.sh
```

**Upload gagal:**
- Check koneksi internet
- Verify Google Drive credentials
- Check quota storage

**Permission error:**
```bash
# Fix Termux permissions
termux-setup-storage
chmod +x scripts/*
```

### Debug Mode
```bash
# Run dengan debug logging
LOG_LEVEL=DEBUG ./scripts/start_bot.sh
```

## 📞 Support & Dokumentasi

- 📖 **[Panduan Instalasi](docs/INSTALLATION_GUIDE.md)** - Petunjuk setup detail
- 🤖 **[Panduan Bot Termux](docs/TERMUX_BOT_README.md)** - Usage & features
- 📝 **[Changelog](docs/CHANGELOG.md)** - Riwayat versi
- 🆘 **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Solusi masalah umum

## 📄 License

Project ini menggunakan MIT License - lihat [LICENSE](LICENSE) file untuk detail.

## 🙏 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API
- [Google Drive API](https://developers.google.com/drive) - Cloud storage
- [Termux](https://termux.com/) - Android terminal emulator

---

🎉 **Dibuat dengan ❤️ untuk komunitas Android Termux Indonesia**

⭐ **Jika project ini membantu, jangan lupa kasih star!** ⭐
