# 🤖 TERMUX TELEGRAM BOT - User Friendly Interface

📱 **Bot backup khusus untuk Android Termux dengan interface click-click yang sangat mudah!**

## ✨ Features Utama

🎯 **Click-Click Interface** - Tidak perlu ketik command manual  
🔘 **Button Navigation** - Semua fitur accessible via button  
⚡ **Auto-Setup Wizard** - Setup Google Drive dalam 2 menit  
♾️ **Unlimited Accounts** - Multiple Google Drive accounts  
🗑️ **Auto-Delete Toggle** - On/off delete after upload  
🚀 **Smart Backup Options** - Quick, Custom, Smart backup  
📱 **Termux Optimized** - Khusus untuk Android Termux  

## 🎯 Super User-Friendly

Bot ini dibuat khusus dengan interface yang **sangat mudah** untuk user. Tidak ada command manual yang perlu diingat, semua lewat **button click**!

### Menu Utama:
- 🚀 **Quick Backup** - Backup semua dengan 1 click
- 👥 **Google Drive** - Manage accounts dengan mudah
- 📁 **Folders** - Add folder dengan quick selection
- ⚙️ **Auto-Delete Settings** - Toggle on/off simple
- 📊 **Status** - Lihat status sistem
- 💾 **Manual Backup** - Backup custom
- ⏰ **Schedule** - Set jadwal otomatis

### Quick Features:
- 📥 Add Downloads folder (1 click)
- 📸 Add Pictures folder (1 click)  
- 📄 Add Documents folder (1 click)
- 💬 Add WhatsApp Media (1 click)

## 🚀 Installation & Setup

### 1. Install di Termux:
```bash
# Clone repository
git clone [your-repo] backup_system
cd backup_system

# Install dependencies
chmod +x install_termux.sh
./install_termux.sh
```

### 2. Start Bot:
```bash
# Start bot
chmod +x start_termux_bot.sh
./start_termux_bot.sh
```

### 3. Setup (Super Easy):
1. **Bot Token**: 
   - Buka @BotFather di Telegram
   - Create bot, copy token
   - Paste di setup

2. **User ID**:
   - Buka @userinfobot di Telegram  
   - Copy User ID
   - Paste di setup

3. **Google Drive** (Optional):
   - Upload credentials file
   - Atau skip dulu, add nanti

**Setup selesai! Bot langsung ready!**

## 💡 Usage Examples

### Backup Quick & Easy:
1. Kirim `/start` ke bot
2. Click "🚀 Quick Backup"  
3. Done! Semua folder ter-backup

### Add Google Drive Account:
1. Menu utama → "👥 Google Drive"
2. Click "➕ Add Account"
3. Upload credentials JSON
4. Done! Unlimited storage ready

### Configure Auto-Delete:
1. Menu utama → "⚙️ Auto-Delete Settings"
2. Click toggle button
3. Done! Auto-delete on/off

### Add Backup Folders:
1. Menu utama → "📁 Folders"
2. Click quick add (Downloads, Pictures, etc)
3. Done! Folder added

## 🎯 Interface Screenshots

```
🤖 TERMUX BACKUP SYSTEM
📱 Android Backup dengan Unlimited Storage

👤 User: John
📊 Status: ✅ Ready  
🗃️ Accounts: 2 Google Drive
📁 Folders: 5 monitored

🎯 Pilih menu:

[🚀 Quick Backup] [⏸️ Stop]
[👥 Google Drive] [📁 Folders]
[⚙️ Auto-Delete Settings] [📊 Status]
[💾 Manual Backup] [⏰ Schedule]
[📋 Logs] [❓ Help]
```

## 🔧 Advanced Features

### Smart Backup:
- **Quick Backup**: Backup semua folder
- **Custom Backup**: Pilih folder tertentu  
- **Smart Backup**: Hanya file yang berubah

### Account Management:
- View usage per account
- Auto-switch account kalau full
- Unlimited account support

### Auto-Delete Options:
- Toggle on/off dengan 1 click
- Smart delete (keep important files)
- Manual delete control

## 📱 Termux Specific

Bot ini khusus dioptimize untuk Android Termux:

- ✅ Storage access permission otomatis
- ✅ Background operation support  
- ✅ Battery optimization aware
- ✅ Network handling untuk mobile
- ✅ Termux package compatibility
- ✅ Android path structure

## 🛠️ Troubleshooting

### Bot tidak start:
1. Check internet connection
2. Verify bot token di `.env`  
3. Restart: `./start_termux_bot.sh`

### Upload error:
1. Check Google Drive credentials
2. Verify storage permission
3. Check file size limit

### Button tidak respond:
1. Restart bot
2. Check Telegram connection
3. Verify user permission

## 📞 Support

- **Logs**: Check di bot → "📋 Logs"
- **Status**: Check di bot → "📊 Status"  
- **Help**: Menu di bot → "❓ Help"

---

🎉 **Enjoy the most user-friendly backup system for Termux!**  
📱 **Click-click interface, no manual commands needed!**
