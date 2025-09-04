# 🚀 QUICK INSTALL GUIDE - Bot Telegram Backup

Bot Telegram untuk backup otomatis file HP ke Google Drive. **Siap pakai dengan one-command install!**

## 📱 INSTALL DI HP/TERMUX (1 PERINTAH)

```bash
# Download dan install otomatis
curl -O https://raw.githubusercontent.com/your-repo/termux_install.sh
chmod +x termux_install.sh
./termux_install.sh
```

## 🛠️ PERSIAPAN SEBELUM INSTALL

### 1. Buat Bot Telegram
1. Chat **@BotFather** di Telegram
2. Ketik `/newbot`
3. Ikuti instruksi, pilih nama bot
4. **SIMPAN TOKEN** yang diberikan

### 2. Dapatkan User ID Telegram
1. Chat **@userinfobot** di Telegram
2. **SIMPAN ID** yang diberikan

### 3. Setup Google Drive API
1. Buka [Google Cloud Console](https://console.cloud.google.com/)
2. Buat project baru atau pilih yang ada
3. **Enable Google Drive API**
4. Buat **OAuth 2.0 Credentials**
5. Download sebagai `google_credentials.json`

### 4. Edit Konfigurasi
```bash
# Edit file .env
nano .env

# Isi dengan data Anda:
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
ALLOWED_USER_IDS=123456789
```

### 5. Tambahkan Google Credentials
```bash
# Copy file ke folder credentials
cp google_credentials.json credentials/
```

## 🎯 JALANKAN BOT

```bash
python3 main.py
```

Bot siap digunakan! Chat bot Anda di Telegram untuk mulai backup.

## ✨ FITUR UTAMA

- 🔄 **Backup Otomatis** - Schedule backup harian
- 📱 **Multi Folder** - Documents, Pictures, DCIM, Download
- ☁️ **Multi Google Account** - Support unlimited akun Google Drive
- 📊 **Progress Real-time** - Monitor progress upload via Telegram
- 🗜️ **Kompresi Opsional** - Hemat storage dengan zip
- 🔐 **Aman** - Enkripsi credentials
- 📱 **Termux Optimized** - Khusus untuk Android

## 🤖 PERINTAH BOT

- `/start` - Mulai bot
- `/backup` - Backup manual
- `/folders` - Kelola folder
- `/accounts` - Kelola akun Google
- `/settings` - Pengaturan
- `/status` - Status sistem

## 🆘 TROUBLESHOOTING

### Bot tidak respon
```bash
# Cek log
tail -f logs/bot.log

# Restart bot
python3 main.py
```

### Error Google credentials
```bash
# Pastikan file ada
ls credentials/google_credentials.json

# Pastikan format benar (JSON)
cat credentials/google_credentials.json | head
```

### Error permission
```bash
# Setup storage access
termux-setup-storage

# Berikan permission saat diminta
```

## 📁 STRUKTUR PROJECT

```
📦 Ujicoba2/
├── 🤖 main.py                    # Entry point
├── ⚙️ .env                       # Konfigurasi (EDIT INI!)
├── 🛠️ setup_config.py            # Auto setup
├── 🚀 termux_install.sh          # One-command install
├── 📋 requirements.txt           # Dependencies
├── 📁 src/                       # Source code
├── ⚙️ config/                    # Konfigurasi
└── 🔐 credentials/               # Google credentials
```

## 🔒 KEAMANAN

- File `.env` dan `credentials/` **TIDAK** ikut diupload ke repository
- Token dan credentials disimpan lokal di HP
- Koneksi ke Google Drive menggunakan OAuth 2.0
- Log sistem untuk monitoring

---

**⚡ Quick Install**: Hanya butuh 2-3 menit setup, bot langsung jalan!
