# 🔐 Credentials Directory

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
