# 📱 UJI COBA DI HP ANDROID

## 🚀 Quick Test di Termux

### 1. Clone Repository Uji Coba
```bash
# Install git dan python dulu
pkg update && pkg upgrade -y
pkg install git python -y

# Clone repository uji coba
git clone https://github.com/jhopan/UjiCoba.git
cd UjiCoba
```

### 2. Quick Start Testing
```bash
# One-command installation
./quick_start.sh
```

### 3. Jika Ada Error Event Loop
```bash
# Emergency restart
./scripts/emergency_restart.sh
```

### 4. Jika pip Error
```bash
# Setup pip
./scripts/setup_pip.sh
```

### 5. 🆕 Jika Error Import "No module named 'telegram.termux_telegram_bot'"
```bash
# Test import paths
./scripts/test_import.sh

# Quick fix semua masalah
./scripts/quick_fix.sh
```

---

## 🔧 Testing Checklist

### ✅ Yang Sudah Diperbaiki:
- [x] Event loop error "Cannot close a running event loop"
- [x] pip installation otomatis
- [x] Graceful shutdown dengan Ctrl+C
- [x] Emergency recovery tools

### 🧪 Test di HP:
1. **Install Dependencies**
   ```bash
   ./quick_start.sh
   ```
   Expected: ✅ Semua package terinstall tanpa error

2. **Start Bot**
   ```bash
   python main.py
   ```
   Expected: ✅ Bot start tanpa event loop error

3. **Graceful Stop**
   ```
   Press Ctrl+C
   ```
   Expected: ✅ Bot stop dengan "Bot stopped by user"

4. **Emergency Test**
   ```bash
   ./scripts/emergency_restart.sh
   ```
   Expected: ✅ Cleanup dan restart berhasil

---

## 📊 Expected Results

### Before Fix:
```
❌ Error: Cannot close a running event loop
RuntimeWarning: coroutine 'Application.shutdown' was never awaited
```

### After Fix:
```
✅ Termux Bot Ready!
📱 Kirim /start ke bot Telegram Anda
⏹️ Bot stopped by user  # Saat Ctrl+C
```

---

## 🆘 Jika Masih Error

### Debug Information:
```bash
./scripts/debug_info.sh
```

### Complete Reset:
```bash
rm .env
./quick_start.sh
```

### Manual pip:
```bash
pkg install python-pip
pip install -r requirements.txt
```

---

## 📞 Report Testing

**Please test and report:**

1. ✅/❌ Installation berhasil
2. ✅/❌ Bot start tanpa error
3. ✅/❌ Graceful shutdown dengan Ctrl+C
4. ✅/❌ Emergency restart berfungsi
5. ✅/❌ pip terinstall otomatis

**Jika error, jalankan:**
```bash
./scripts/debug_info.sh
```
Dan kirim hasil file debug.

---

*Repository: https://github.com/jhopan/UjiCoba.git*
*Status: Ready for Android testing*
