# 🔧 TROUBLESHOOTING GUIDE
## BackupHpDriveOtomatis-Termux

---

## 🚨 Common Issues & Solutions

### 1. "Cannot close a running event loop" Error

**Symptom:**
```
RuntimeWarning: coroutine 'Application.shutdown' was never awaited
❌ Error: Cannot close a running event loop
```

**Solution:**
✅ **Fixed in latest version**
- Updated event loop handling
- Proper signal handling for Ctrl+C
- Graceful shutdown process

**Manual Fix:**
```bash
# Stop all Python processes
pkill -f python

# Restart bot
./quick_start.sh
```

---

### 2. pip Not Found

**Symptom:**
```
bash: pip: command not found
```

**Solution:**
```bash
# Install pip
pkg install python-pip

# Or use python module
python -m ensurepip --upgrade

# Verify installation
pip --version
```

**Auto-fix:** ✅ Added to install scripts

---

### 3. Telegram Library Not Found

**Symptom:**
```
❌ Telegram library not available
```

**Solution:**
```bash
# Install telegram bot library
pip install python-telegram-bot>=20.0

# Verify installation
python -c "import telegram; print('OK')"
```

---

### 4. Storage Permission Denied

**Symptom:**
```
Permission denied: /storage/emulated/0/
```

**Solution:**
```bash
# Setup storage access
termux-setup-storage

# Grant permission in popup
# Then restart bot
```

---

### 5. Bot Token Invalid

**Symptom:**
```
telegram.error.InvalidToken: Invalid token
```

**Solution:**
1. Check token format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
2. Get new token from @BotFather
3. Update .env file
4. Restart bot

---

### 6. Google Drive API Errors

**Symptom:**
```
googleapiclient.errors.HttpError
```

**Solution:**
1. Check credentials.json file
2. Enable Google Drive API in Google Cloud Console
3. Download fresh credentials
4. Upload to bot via Telegram

---

## 🔄 Quick Fixes

### Reset Everything
```bash
# Remove config
rm .env

# Restart setup
./quick_start.sh
```

### Clear Python Cache
```bash
# Clear Python cache
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +

# Restart
python main.py
```

### Force Stop All
```bash
# Kill all python processes
pkill -f python

# Kill specific bot
pkill -f "termux_telegram_bot"

# Restart
./quick_start.sh
```

---

## 📊 Check System Status

### Python Environment
```bash
# Check Python
python --version
python3 --version

# Check pip
pip --version
pip3 --version

# Check packages
pip list | grep telegram
pip list | grep google
```

### Bot Status
```bash
# Check if bot is running
ps aux | grep python

# Check logs
tail -f logs/*.log

# Check ports
netstat -an | grep LISTEN
```

---

## 🆘 Emergency Commands

### Force Restart
```bash
#!/bin/bash
echo "🚨 Emergency restart..."

# Kill all related processes
pkill -f python
pkill -f bot
sleep 2

# Clear temp files
rm -rf temp/*
rm -rf logs/*.log

# Restart
echo "🚀 Restarting..."
./quick_start.sh
```

### Reset Installation
```bash
#!/bin/bash
echo "🔄 Complete reset..."

# Remove all config
rm -f .env
rm -rf credentials/*
rm -rf logs/*
rm -rf temp/*

# Reinstall
echo "📦 Reinstalling..."
./quick_start.sh
```

---

## 📞 Getting Help

### Debug Mode
```bash
# Run with debug logging
export LOG_LEVEL=DEBUG
python main.py
```

### Collect System Info
```bash
# System information
echo "=== SYSTEM INFO ==="
uname -a
python --version
pip --version

echo "=== TERMUX INFO ==="
echo $PREFIX
echo $HOME

echo "=== INSTALLED PACKAGES ==="
pip list

echo "=== RUNNING PROCESSES ==="
ps aux | grep python
```

### Contact Support
- 📧 Create GitHub Issue with system info
- 📱 Include error messages
- 🔍 Mention Android version and Termux version

---

## ✅ Prevention Tips

1. **Always use official Termux** from F-Droid or Google Play
2. **Keep packages updated:** `pkg upgrade`
3. **Don't force-kill** processes (use Ctrl+C)
4. **Check permissions** before running
5. **Backup credentials** regularly

---

*Last updated: $(date)*
