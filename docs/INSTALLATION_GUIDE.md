# Advanced Backup System - Complete Installation Guide

## 🚀 Quick Installation (Termux)

### 1. One-Command Setup
```bash
# Download and run the setup script
curl -sSL https://raw.githubusercontent.com/your-repo/backup-system/main/setup_termux.sh | bash
```

### 2. Manual Installation

#### Step 1: Install Dependencies
```bash
# Update Termux
pkg update && pkg upgrade -y

# Install Python and tools
pkg install -y python python-pip git curl wget openssh libffi openssl libjpeg-turbo libcrypt nano

# Set up storage access (PENTING!)
termux-setup-storage

# Install additional tools
pkg install -y which tree htop
```

#### Step 2: Install Python Packages
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 3: Configure the System
```bash
# Copy and edit the environment file
cp .env.example .env
nano .env
```

## ⚙️ Configuration Guide

### 1. Telegram Bot Setup

1. **Create a bot:**
   - Message @BotFather on Telegram
   - Use `/newbot` command
   - Get your bot token

2. **Get your User ID:**
   - Message @userinfobot on Telegram
   - Copy your numeric user ID

3. **Update .env file:**
   ```env
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ALLOWED_USER_IDS=123456789
   ```

### 2. Google Drive API Setup

1. **Google Cloud Console:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing
   - Enable Google Drive API

2. **Create Credentials:**
   - Go to Credentials → Create Credentials → OAuth 2.0 Client IDs
   - Choose "Desktop application"
   - Download the JSON file

3. **Setup Credentials:**
   ```bash
   # Place your credentials file
   mv ~/downloads/credentials.json credentials/account1_credentials.json
   ```

### 3. Storage Configuration

```env
# Monitor these paths (comma-separated)
MONITOR_PATHS=/data/data/com.termux/files/home/storage/shared/Download,/data/data/com.termux/files/home/storage/shared/Pictures

# Maximum file size (100MB)
MAX_FILE_SIZE=104857600

# Storage per account (15GB)
MAX_STORAGE_PER_ACCOUNT=16106127360

# Auto-delete files after upload
AUTO_DELETE_AFTER_UPLOAD=false
```

## 🚀 Starting the System

### Method 1: Direct Start
```bash
cd backup_system
python src/main.py
```

### Method 2: Using Scripts
```bash
./start.sh
```

### Method 3: Background Service
```bash
# Enable auto-start
systemctl --user enable backup-bot.service
systemctl --user start backup-bot.service
```

## 📱 Telegram Bot Usage

### Main Commands

- **`/start`** - Show main menu with buttons
- **`/backup`** - Start backup process
- **`/status`** - Show system status
- **`/accounts`** - Manage Google Drive accounts
- **`/settings`** - Configure system settings
- **`/stop`** - Stop current backup operation

### Interactive Menus

The bot provides interactive menus for:
- 📱 Backup management (start, stop, schedule)
- 👥 Account management (add, remove, configure)
- 📁 Folder management (add paths, set rules)
- ⚙️ Settings (backup rules, network settings)
- 📊 Status monitoring (progress, statistics)

### Backup Options

1. **Quick Backup** - Backup with current settings
2. **Custom Backup** - Choose specific files/folders
3. **Scheduled Backup** - Set automatic backup times
4. **Auto Backup Toggle** - Enable/disable auto backup

## 🔧 Advanced Configuration

### Backup Rules
```yaml
# backup_rules.yaml
include_paths:
  - ~/storage/shared/Download
  - ~/storage/shared/Pictures
  - ~/storage/shared/Documents

exclude_paths:
  - ~/storage/shared/Download/temp
  - "*/node_modules"

file_types:
  include: []  # Empty = all types
  exclude: ['.tmp', '.log', '.cache']

size_limits:
  min_size: 0
  max_size: 104857600  # 100MB
```

### Network Settings
```env
CONNECTION_TIMEOUT=30
UPLOAD_TIMEOUT=300
MAX_CONCURRENT_UPLOADS=3
```

### Logging Configuration
```env
LOG_LEVEL=INFO
LOG_TO_FILE=true
LOG_TO_TELEGRAM=true
```

## 📊 Monitoring and Maintenance

### Check System Status
```bash
./status.sh
```

### View Logs
```bash
# Real-time logs
tail -f logs/backup.log

# Recent activity
cat logs/backup.log | tail -50
```

### Database Management
```bash
# View backup statistics
python -c "
from src.database_manager import DatabaseManager
db = DatabaseManager()
stats = db.get_backup_statistics(30)
print(f'Last 30 days: {stats[\"total_files\"]} files')
print(f'Success rate: {stats[\"success_rate\"]:.1f}%')
"
```

### Storage Usage
```bash
# Check account storage
python -c "
from src.enhanced_settings import EnhancedSettings
settings = EnhancedSettings()
for account in settings.get_enabled_accounts():
    print(f'{account[\"name\"]}: {account.get(\"current_usage\", 0)} bytes used')
"
```

## 🔄 Automated Operations

### Schedule Configuration
```env
# Daily backup at midnight
BACKUP_SCHEDULE_TIME=00:00
AUTO_BACKUP_ENABLED=true
```

### Retry Mechanism
The system automatically retries failed uploads:
- 3 retry attempts with exponential backoff
- Network connectivity checks before retry
- Failed files queued for later retry

### File Organization
Files are automatically organized by:
- Date folders (YYYY-MM-DD)
- File type subfolders (images, documents, etc.)
- Duplicate detection and handling

## 🆘 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Permission Denied**
   ```bash
   chmod +x *.sh
   termux-setup-storage
   ```

3. **Google API Errors**
   - Check credentials.json placement
   - Verify API is enabled in Google Cloud Console
   - Complete OAuth flow through bot

4. **Network Issues**
   - Check internet connection
   - Verify API rate limits
   - Check firewall settings

5. **Storage Full**
   - Use `/accounts` command to check usage
   - Add more Google Drive accounts
   - Enable auto-delete after upload

### Debug Mode
```bash
# Run with debug logging
LOG_LEVEL=DEBUG python src/main.py
```

### Reset Configuration
```bash
# Reset to defaults
rm .env
cp .env.example .env
nano .env
```

## 📞 Support and Maintenance

### Log Files
- `logs/backup.log` - Main application log
- `logs/error.log` - Error-specific log
- `backup_system.db` - SQLite database

### Backup Database
```bash
# Backup the database
cp backup_system.db backup_system_$(date +%Y%m%d).db
```

### Update System
```bash
# Update Python packages
pip install --upgrade -r requirements.txt

# Restart service
systemctl --user restart backup-bot.service
```

## 🔐 Security Considerations

1. **Protect Credentials**
   - Keep credentials.json files secure
   - Don't share your bot token
   - Limit allowed user IDs

2. **Network Security**
   - Use HTTPS for all API calls
   - Enable OAuth2 for Google Drive
   - Monitor access logs

3. **Data Privacy**
   - Files are uploaded to your own Google Drive
   - No third-party data storage
   - Local encryption available

## 📈 Performance Optimization

### For Large Files
```env
MAX_CONCURRENT_UPLOADS=1
UPLOAD_TIMEOUT=900
USE_RESUMABLE_UPLOADS=true
```

### For Many Small Files
```env
MAX_CONCURRENT_UPLOADS=5
COMPRESS_FILES=true
```

### Memory Usage
```env
# Limit file size to manage memory
MAX_FILE_SIZE=52428800  # 50MB
```

This guide covers everything you need to set up and run the advanced backup system. The system is designed to be user-friendly through the Telegram bot interface while providing powerful automation and customization options.
