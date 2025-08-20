# 🚀 BackupHpDriveOtomatis-Termux

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot%20Ready-blue.svg)](https://core.telegram.org/bots)

**🤖 Sistem backup otomatis HP Android ke Google Drive dengan interface Telegram yang sangat user-friendly**

## ✨ Fitur Utama

- 🤖 **Telegram Bot Interface** - Control via chat dengan button navigation
- ☁️ **Unlimited Google Drive** - Multiple accounts support (15GB per akun)
- 📱 **Termux Optimized** - Khusus untuk Android Termux environment
- 🔄 **Auto Backup** - Scheduled & manual backup options
- 🗑️ **Smart Auto-Delete** - Toggle on/off hapus file setelah upload
- 📁 **Flexible Folders** - Backup folder apapun dengan 1-click setup
- 🎯 **User-Friendly UI** - Click-click interface, tidak perlu hafal command

## 🚀 Quick Start

### 1. Clone & Install
```bash
# Clone repository
git clone https://github.com/jhopan/BackupHpDriveOtomatis-Termux.git
cd BackupHpDriveOtomatis-Termux

# Auto install (recommended)
chmod +x quick_start.sh
./quick_start.sh
```

### 2. Setup Bot
1. **Buat Telegram Bot** - Message @BotFather
2. **Dapatkan User ID** - Message @userinfobot  
3. **Setup Google Drive** - Upload credentials via bot
4. **Mulai Backup** - Click "🚀 Quick Backup"

## 📱 Interface Bot Telegram

```
🤖 TERMUX BACKUP SYSTEM
📱 Android Backup dengan Unlimited Storage

👤 User: Nama Anda
📊 Status: ✅ Ready
🗃️ Accounts: 2 Google Drive
📁 Folders: 5 monitored

🎯 Main Menu:

[🚀 Quick Backup] [⏸️ Stop Backup]
[👥 Google Drive] [📁 Backup Folders]  
[⚙️ Auto-Delete Settings] [📊 System Status]
[💾 Manual Backup] [⏰ Schedule Backup]
[📋 View Logs] [❓ Help & Support]
```

## 🎯 Fitur Smart

### 🚀 Opsi Backup
- **Quick Backup** - Backup semua folder sekaligus
- **Custom Backup** - Pilih folder tertentu
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
