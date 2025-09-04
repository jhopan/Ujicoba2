# 📋 CHECKLIST PERSIAPAN BOT TELEGRAM

## ✅ FILE YANG SUDAH DISEDIAKAN OTOMATIS:
- [x] setup_config.py (script otomatis setup)
- [x] termux_install.sh (script install one-command)
- [x] .env.template (template konfigurasi)
- [x] config/accounts.json (auto-generated)
- [x] config/folders.json (auto-generated) 
- [x] config/settings.json (auto-generated)

## 🔴 FILE YANG HARUS ANDA SIAPKAN:

### 1. File .env (WAJIB)
```bash
# Copy dari .env.template dan edit:
cp .env.template .env
nano .env

# Isi dengan data Anda:
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
ALLOWED_USER_IDS=123456789
```

### 2. Google Credentials (WAJIB)
```bash
# Download dari Google Cloud Console:
credentials/google_credentials.json
```

## 🚀 CARA INSTALL DI HP/TERMUX:

### Opsi 1: One Command Install
```bash
curl -O https://raw.githubusercontent.com/your-repo/termux_install.sh
chmod +x termux_install.sh
./termux_install.sh
```

### Opsi 2: Manual Clone
```bash
git clone https://github.com/your-repo/bot-telegram.git
cd bot-telegram
chmod +x termux_install.sh
./termux_install.sh
```

## 📝 LANGKAH PERSIAPAN SEBELUM UPLOAD:

1. **Setup Bot Telegram:**
   - Chat @BotFather di Telegram
   - Buat bot baru: `/newbot`
   - Simpan token yang diberikan

2. **Dapatkan User ID:**
   - Chat @userinfobot di Telegram
   - Simpan ID yang diberikan

3. **Setup Google Drive API:**
   - Buka https://console.cloud.google.com/
   - Buat project baru
   - Enable Google Drive API
   - Buat OAuth 2.0 credentials
   - Download sebagai `google_credentials.json`

4. **Edit File .env:**
   ```bash
   TELEGRAM_BOT_TOKEN=token_dari_botfather
   ALLOWED_USER_IDS=id_dari_userinfobot
   ```

5. **Upload ke Repository:**
   - Pastikan .env TIDAK ikut terupload (ada di .gitignore)
   - Pastikan google_credentials.json TIDAK ikut terupload
   - Upload semua file lainnya

## 🎯 HASIL AKHIR:
User hanya perlu:
1. Clone repository
2. Edit file .env dengan token mereka
3. Tambahkan google_credentials.json
4. Jalankan `./termux_install.sh`
5. Bot langsung jalan!
