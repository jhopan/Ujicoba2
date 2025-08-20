# 🚀 Quick Start Guide - Advanced Backup System

## 📱 Panduan Cepat untuk Pemula

### 1️⃣ Persiapan Termux
```bash
# Update Termux terlebih dahulu
pkg update && pkg upgrade -y

# Install Python dan tools yang diperlukan
pkg install -y python python-pip git curl
```

### 2️⃣ Download dan Setup
```bash
# Clone atau download project ini
git clone <repository-url> backup_system
cd backup_system

# Jalankan script setup otomatis
bash setup_termux.sh

# Atau install manual
pip install -r requirements.txt
```

### 3️⃣ Konfigurasi Bot Telegram
1. **Buat Bot Telegram:**
   - Buka Telegram, cari @BotFather
   - Kirim `/newbot`
   - Ikuti instruksi, simpan token bot

2. **Dapatkan User ID:**
   - Cari @userinfobot di Telegram
   - Kirim `/start`, catat User ID

3. **Edit Konfigurasi:**
   ```bash
   cp .env.example .env
   nano .env
   ```
   
   Isi bagian berikut:
   ```env
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ALLOWED_USER_IDS=123456789
   ```

### 4️⃣ Setup Google Drive
1. **Buka Google Cloud Console:**
   - Kunjungi: https://console.cloud.google.com/
   - Buat project baru atau gunakan yang ada
   - Aktifkan Google Drive API

2. **Buat Credentials:**
   - Pilih "Credentials" → "Create Credentials"
   - Pilih "OAuth 2.0 Client IDs"
   - Pilih "Desktop application"
   - Download file JSON

3. **Upload Credentials:**
   ```bash
   # Copy file credentials ke folder yang tepat
   cp ~/downloads/credentials.json credentials/account1_credentials.json
   ```

### 5️⃣ Set Storage Access (Termux)
```bash
# Berikan akses storage untuk Termux
termux-setup-storage
```

### 6️⃣ Jalankan Sistem
```bash
# Jalankan sistem backup
python src/main.py

# Atau gunakan script demo
./start_demo.sh
```

### 7️⃣ Gunakan Bot Telegram

Sekarang buka Telegram dan cari bot Anda:

1. **Kirim `/start`** untuk melihat menu utama
2. **Pilih "📱 Start Backup"** untuk memulai backup
3. **Gunakan "👥 Manage Accounts"** untuk menambah akun Google Drive
4. **Pakai "⚙️ Settings"** untuk mengatur konfigurasi

## 🎯 Menu Bot Telegram

### Menu Utama
- **📱 Start Backup** - Mulai proses backup
- **⏸️ Stop Backup** - Hentikan backup yang sedang berjalan
- **👥 Manage Accounts** - Kelola akun Google Drive
- **📁 Manage Folders** - Atur folder yang akan di-backup
- **⚙️ Settings** - Pengaturan sistem
- **📊 Status** - Lihat status dan statistik
- **📋 View Logs** - Lihat log aktivitas
- **❓ Help** - Bantuan

### Opsi Backup
- **🚀 Quick Backup** - Backup cepat dengan pengaturan default
- **📋 Custom Backup** - Pilih folder/file tertentu
- **⏰ Schedule Backup** - Atur jadwal backup otomatis
- **🔄 Auto Backup On/Off** - Nyalakan/matikan backup otomatis

## 🔧 Tips dan Trik

### ✅ Yang Harus Dilakukan
- Selalu test dengan file kecil dulu
- Gunakan `/status` untuk monitor sistem
- Backup file penting secara berkala
- Periksa storage Google Drive secara rutin

### ❌ Yang Harus Dihindari
- Jangan share token bot dengan orang lain
- Jangan backup file yang terlalu besar (>100MB)
- Jangan lupa setup termux-setup-storage
- Jangan hapus file credentials

### 🚨 Troubleshooting Cepat

**Problem: Bot tidak merespon**
```bash
# Cek apakah sistem berjalan
ps aux | grep python

# Restart sistem
python src/main.py
```

**Problem: Error import module**
```bash
# Install ulang dependencies
pip install -r requirements.txt
```

**Problem: Permission denied**
```bash
# Setup storage access
termux-setup-storage

# Berikan permission ke script
chmod +x *.sh
```

**Problem: Google Drive error**
- Pastikan API sudah diaktifkan di Google Cloud Console
- Cek file credentials.json sudah benar
- Jalankan OAuth flow melalui bot

## 📞 Bantuan Lebih Lanjut

### 📚 Dokumentasi Lengkap
- `INSTALLATION_GUIDE.md` - Panduan instalasi detail
- `PROJECT_SUMMARY.md` - Overview sistem lengkap
- `CHANGELOG.md` - Riwayat perubahan

### 🔍 Debug dan Log
```bash
# Lihat log real-time
tail -f logs/backup.log

# Jalankan dalam mode debug
LOG_LEVEL=DEBUG python src/main.py
```

### 📱 Kontak
- Cek issue di repository GitHub
- Gunakan command `/help` di bot Telegram
- Review log error di `logs/backup.log`

---

**🎉 Selamat! Sistem backup Anda siap digunakan!**

Mulai dengan backup file kecil untuk testing, lalu konfigurasikan sesuai kebutuhan Anda.
