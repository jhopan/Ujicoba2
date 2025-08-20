# 🚀 Advanced Backup System for Android/Termux

## 📋 Project Overview

This is a comprehensive, Telegram bot-controlled backup system designed specifically for Android devices using Termux. The system automatically uploads files to multiple Google Drive accounts with advanced features like auto-retry, folder organization, and sophisticated file management - all controlled through an intuitive Telegram bot interface.

## ✨ Key Features

### 🤖 Complete Telegram Bot Control
- **No Code Editing Required** - Everything controlled through bot commands
- Interactive menus with inline keyboards
- Real-time progress updates
- Comprehensive status monitoring
- User-friendly command interface

### ☁️ Multi-Account Google Drive Integration
- Support for 2-3 Google Drive accounts (45GB total storage)
- Automatic account rotation when storage limits reached
- OAuth2 authentication flow
- Resumable uploads for large files
- Storage usage monitoring

### 🔄 Advanced Backup Features
- **Auto-retry mechanism** with exponential backoff
- Network connectivity checking
- Failed upload queue management
- Scheduled backups (configurable time)
- File organization by date and type
- Duplicate detection and handling

### 📁 Intelligent File Organization
- Date-based folder structure (YYYY-MM-DD)
- File type categorization (images, documents, videos, etc.)
- Automatic folder creation
- File manifest generation
- Storage optimization

### 🌐 Network Management
- Connection monitoring
- Automatic retry on network failures
- Bandwidth management
- Timeout handling
- Connectivity restoration waiting

### 📊 Comprehensive Monitoring
- SQLite database for backup logs
- Detailed statistics and reports
- System health monitoring
- Error tracking and notifications
- Export capabilities

## 🏗️ System Architecture

```
backup_system/
├── src/                           # Main source code
│   ├── main.py                   # Application entry point
│   ├── advanced_telegram_bot.py  # Telegram bot with full UI
│   ├── enhanced_backup_manager.py # Core backup logic
│   ├── enhanced_google_drive_manager.py # Google Drive operations
│   ├── database_manager.py       # Data persistence
│   └── utils/                    # Utility modules
│       ├── network_manager.py    # Network connectivity
│       ├── folder_manager.py     # File organization
│       ├── file_organizer.py     # Advanced file handling
│       ├── enhanced_settings.py  # Configuration management
│       └── telegram_utils.py     # Bot utilities
├── credentials/                   # Google Drive credentials
├── logs/                         # System logs
├── .env                          # Configuration file
├── requirements.txt              # Python dependencies
├── setup_termux.sh              # Automatic setup script
├── start_demo.sh                # Interactive demo script
└── INSTALLATION_GUIDE.md        # Complete setup guide
```

## 🚀 Quick Installation

### Option 1: Automated Setup (Recommended)
```bash
# Download and run setup script
curl -sSL https://raw.githubusercontent.com/your-repo/backup-system/main/setup_termux.sh | bash
```

### Option 2: Manual Installation
```bash
# Update Termux
pkg update && pkg upgrade -y

# Install dependencies
pkg install -y python python-pip git curl openssh-sftp-server libffi openssl

# Install Python packages
pip install -r requirements.txt

# Configure system
cp .env.example .env
nano .env
```

## ⚙️ Configuration

### 1. Telegram Bot Setup
1. Create bot with @BotFather
2. Get bot token
3. Get your user ID from @userinfobot
4. Update `.env` file:
```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
ALLOWED_USER_IDS=123456789
```

### 2. Google Drive Setup
1. Create Google Cloud project
2. Enable Google Drive API
3. Create OAuth2 credentials
4. Download credentials.json to `credentials/` folder

### 3. Path Configuration
```env
MONITOR_PATHS=/data/data/com.termux/files/home/storage/shared/Download,/data/data/com.termux/files/home/storage/shared/Pictures
```

## 📱 Telegram Bot Commands

### Main Commands
- `/start` - Show main menu with interactive buttons
- `/backup` - Start backup process with options
- `/status` - Display comprehensive system status
- `/accounts` - Manage Google Drive accounts
- `/settings` - Configure all system settings
- `/stop` - Stop current operations

### Interactive Menus
- **📱 Backup Management** - Start, stop, schedule backups
- **👥 Account Management** - Add, remove, configure accounts
- **📁 Folder Management** - Set paths, organize files
- **⚙️ Settings Control** - Network, logging, notifications
- **📊 Status Monitoring** - Progress, statistics, health

## 🔧 Advanced Features

### Auto-Retry System
- 3 retry attempts with exponential backoff
- Network connectivity checks before retry
- Failed file queue management
- Smart error handling

### File Organization
- Automatic date folders (YYYY-MM-DD)
- File type categories (images, documents, videos, etc.)
- Duplicate detection and handling
- Manifest file generation

### Network Management
- Connection monitoring and restoration
- Bandwidth limiting options
- Timeout management
- Resumable uploads

### Storage Management
- Multi-account rotation
- Storage usage tracking
- Warning thresholds
- Automatic cleanup options

## 📊 Monitoring and Logging

### Database Tracking
- Backup session logs
- File upload status
- Error tracking
- System events
- Statistics generation

### Log Files
- `logs/backup.log` - Main application log
- `logs/error.log` - Error-specific logging
- SQLite database for structured data

### Status Monitoring
- Real-time progress updates
- Network connectivity status
- Storage usage per account
- Success/failure rates
- System health metrics

## 🔒 Security Features

- OAuth2 for Google Drive authentication
- User ID verification for Telegram bot
- Secure credential storage
- No third-party data access
- Local encryption options

## 🚀 Usage Examples

### Starting the System
```bash
cd backup_system
python src/main.py
```

### Using Telegram Bot
1. Send `/start` to your bot
2. Use interactive menus for all operations
3. Monitor progress through status updates
4. Configure settings without touching code

### Quick Commands
```bash
# Quick backup
./quick_backup.sh

# Check status
./status.sh

# Start system
./start.sh
```

## 🛠️ Customization

### Backup Rules (backup_rules.yaml)
```yaml
include_paths:
  - ~/storage/shared/Download
  - ~/storage/shared/Pictures
exclude_paths:
  - ~/storage/shared/Download/temp
file_types:
  exclude: ['.tmp', '.log', '.cache']
size_limits:
  max_size: 104857600  # 100MB
```

### Network Settings
```env
CONNECTION_TIMEOUT=30
UPLOAD_TIMEOUT=300
MAX_CONCURRENT_UPLOADS=3
```

## 📈 Performance Optimization

### For Large Files
- Use resumable uploads
- Reduce concurrent uploads
- Increase timeout values

### For Many Small Files
- Enable compression
- Increase concurrent uploads
- Use batch operations

## 🆘 Troubleshooting

### Common Issues
1. **Import errors** - Install requirements: `pip install -r requirements.txt`
2. **Permission denied** - Run: `termux-setup-storage`
3. **Network issues** - Check connectivity and API limits
4. **Storage full** - Add more accounts or enable auto-delete

### Debug Mode
```bash
LOG_LEVEL=DEBUG python src/main.py
```

## 🔄 Maintenance

### Regular Tasks
- Check storage usage
- Review backup logs
- Update credentials
- Clean old files
- Monitor system health

### Backup Database
```bash
cp backup_system.db backup_system_$(date +%Y%m%d).db
```

## 📞 Support

- Check `logs/backup.log` for errors
- Review `.env` configuration
- Verify Google Drive API setup
- Test network connectivity
- Use interactive demo script

## 🎯 Project Goals Achieved

✅ **Complete Telegram Bot Control** - No manual code editing required
✅ **Multi-Account Google Drive** - Support for 2-3 accounts (45GB total)
✅ **Automatic Midnight Backups** - Configurable scheduled backups
✅ **Auto-Retry on Network Failure** - Robust network handling
✅ **Folder Organization** - Date and file type organization
✅ **Auto-Delete After Upload** - Configurable cleanup
✅ **Comprehensive Management** - All features accessible via bot
✅ **Android/Termux Optimized** - Designed specifically for mobile use

This system provides a complete, professional-grade backup solution that meets all your requirements for automated, intelligent file backup with sophisticated Telegram bot control.
