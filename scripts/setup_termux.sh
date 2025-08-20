#!/bin/bash

# Advanced Backup System Setup Script for Termux
# This script sets up the complete backup system with all dependencies

echo "🚀 Setting up Advanced Backup System for Termux..."
echo "=================================================="

# Update package manager
echo "📦 Updating packages..."
pkg update && pkg upgrade -y

# Install Python and essential tools
echo "🐍 Installing Python and essential tools..."
pkg install -y python python-pip git curl openssh-sftp-server

# Install system dependencies for Python packages
echo "🔧 Installing system dependencies..."
pkg install -y libffi openssl libjpeg-turbo libcrypt

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Create backup system directory
echo "📁 Setting up project directory..."
BACKUP_DIR="$HOME/backup_system"
mkdir -p "$BACKUP_DIR"
cd "$BACKUP_DIR"

# Install Python requirements
echo "📚 Installing Python packages..."
pip install --no-cache-dir -r requirements.txt

# Create necessary directories
echo "📂 Creating directory structure..."
mkdir -p logs
mkdir -p credentials
mkdir -p backups
mkdir -p temp

# Set up environment file
echo "⚙️ Setting up configuration..."
if [ ! -f .env ]; then
    cat > .env << 'EOF'
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
ALLOWED_USER_IDS=your_telegram_user_id_here

# Backup Configuration
BACKUP_BASE_DIR=/data/data/com.termux/files/home/backups
MAX_FILE_SIZE=104857600
AUTO_DELETE_AFTER_UPLOAD=false
COMPRESS_FILES=false

# Storage Configuration  
MAX_STORAGE_PER_ACCOUNT=16106127360
STORAGE_WARNING_THRESHOLD=0.9

# Network Configuration
CONNECTION_TIMEOUT=30
UPLOAD_TIMEOUT=300
MAX_CONCURRENT_UPLOADS=3

# Logging Configuration
LOG_LEVEL=INFO
LOG_TO_FILE=true
LOG_TO_TELEGRAM=true

# Paths to monitor (comma-separated)
MONITOR_PATHS=/data/data/com.termux/files/home/storage/shared/Download,/data/data/com.termux/files/home/storage/shared/Pictures,/data/data/com.termux/files/home/storage/shared/Documents

# Schedule Configuration
BACKUP_SCHEDULE_TIME=00:00
AUTO_BACKUP_ENABLED=true
EOF
    
    echo "✅ Created .env file. Please edit it with your tokens and settings."
    echo "📝 Edit the .env file: nano .env"
fi

# Create systemd-style service for auto-start
echo "🔄 Setting up auto-start service..."
mkdir -p "$HOME/.config/systemd/user"
cat > "$HOME/.config/systemd/user/backup-bot.service" << EOF
[Unit]
Description=Advanced Backup System Bot
After=network.target

[Service]
Type=simple
ExecStart=/data/data/com.termux/files/usr/bin/python $BACKUP_DIR/src/main.py
Restart=always
RestartSec=10
WorkingDirectory=$BACKUP_DIR

[Install]
WantedBy=default.target
EOF

# Create startup script
echo "📱 Creating startup script..."
cat > "$BACKUP_DIR/start.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
echo "🚀 Starting Advanced Backup System..."
python src/main.py
EOF

chmod +x "$BACKUP_DIR/start.sh"

# Create quick commands
echo "⚡ Creating quick commands..."
cat > "$BACKUP_DIR/quick_backup.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
echo "🔄 Running quick backup..."
python -c "
import asyncio
from src.enhanced_backup_manager import EnhancedBackupManager
async def quick_backup():
    manager = EnhancedBackupManager()
    await manager.run_quick_backup()
asyncio.run(quick_backup())
"
EOF

chmod +x "$BACKUP_DIR/quick_backup.sh"

# Create status check script
cat > "$BACKUP_DIR/status.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
echo "📊 Checking backup system status..."
python -c "
from src.database_manager import DatabaseManager
db = DatabaseManager()
stats = db.get_backup_statistics(7)
print(f'Last 7 days: {stats[\"total_files\"]} files, {stats[\"success_rate\"]:.1f}% success rate')
"
EOF

chmod +x "$BACKUP_DIR/status.sh"

# Set up Termux storage access
echo "📱 Setting up storage access..."
termux-setup-storage

# Create alias for easy access
echo "🔗 Creating aliases..."
echo "alias backup-start='cd $BACKUP_DIR && ./start.sh'" >> "$HOME/.bashrc"
echo "alias backup-quick='cd $BACKUP_DIR && ./quick_backup.sh'" >> "$HOME/.bashrc"
echo "alias backup-status='cd $BACKUP_DIR && ./status.sh'" >> "$HOME/.bashrc"

# Final setup instructions
echo ""
echo "🎉 Setup completed successfully!"
echo "================================="
echo ""
echo "📋 Next steps:"
echo "1. Edit configuration: nano .env"
echo "2. Add your Telegram bot token"
echo "3. Add your Telegram user ID" 
echo "4. Set up Google Drive credentials (see README.md)"
echo "5. Start the system: ./start.sh"
echo ""
echo "🔧 Quick commands:"
echo "• Start system: backup-start"
echo "• Quick backup: backup-quick" 
echo "• Check status: backup-status"
echo ""
echo "📁 Project directory: $BACKUP_DIR"
echo "📖 For detailed setup instructions, see README.md"
echo ""
echo "⚠️  Important: Restart Termux to load new aliases"

# Create README with setup instructions
cat > "$BACKUP_DIR/README.md" << 'EOF'
# Advanced Backup System for Termux

## 🚀 Quick Start

1. **Configure the system:**
   ```bash
   nano .env
   ```
   Add your Telegram bot token and user ID.

2. **Set up Google Drive credentials:**
   - Create a project in Google Cloud Console
   - Enable Google Drive API
   - Download credentials.json to the `credentials/` folder
   - Run the bot once to complete OAuth setup

3. **Start the system:**
   ```bash
   ./start.sh
   ```

## 📱 Telegram Bot Commands

- `/start` - Show main menu
- `/backup` - Start backup process
- `/status` - Show system status
- `/accounts` - Manage Google Drive accounts
- `/settings` - Configure system settings
- `/stop` - Stop current backup

## 🔧 Configuration

Edit `.env` file to configure:
- Telegram bot settings
- Backup paths and rules
- Storage limits
- Network settings
- Logging preferences

## 📊 Monitoring

- Check status: `./status.sh`
- View logs: `tail -f logs/backup.log`
- Quick backup: `./quick_backup.sh`

## 🔄 Auto-start

The system includes auto-start capability. Enable with:
```bash
systemctl --user enable backup-bot.service
systemctl --user start backup-bot.service
```

## 📂 Directory Structure

```
backup_system/
├── src/                    # Source code
├── credentials/            # Google Drive credentials
├── logs/                   # Log files
├── backups/               # Local backup staging
├── .env                   # Configuration
└── *.sh                   # Utility scripts
```

## 🆘 Troubleshooting

1. **Import errors:** Ensure all packages are installed with `pip install -r requirements.txt`
2. **Permission denied:** Run `chmod +x *.sh` to make scripts executable
3. **Storage access:** Run `termux-setup-storage` if file access fails
4. **Network issues:** Check your internet connection and API limits

## 📞 Support

For issues and feature requests, check the logs in `logs/backup.log` and ensure your `.env` configuration is correct.
EOF

echo "📖 Created README.md with detailed instructions"
echo "✅ Setup script completed!"
