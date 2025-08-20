@echo off
title Ultimate Backup System - Dependency Installer

echo.
echo ========================================
echo 🚀 ULTIMATE BACKUP SYSTEM
echo 📦 Installing Dependencies...
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! 
    echo 📦 Please install Python 3.7+ from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found

REM Check pip
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip not found! Installing pip...
    python -m ensurepip --upgrade
)

echo ✅ pip available

echo.
echo 📦 Installing Ultimate Backup System dependencies...
echo ⏳ This may take a few minutes...
echo.

REM Core packages first (most important)
echo 🤖 Installing Telegram Bot support...
python -m pip install python-telegram-bot>=20.0

echo ☁️ Installing Google Drive API...
python -m pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

echo 🔄 Installing async file operations...
python -m pip install aiofiles aiohttp

echo ⚙️ Installing configuration tools...
python -m pip install python-dotenv pyyaml

echo 🌐 Installing network utilities...
python -m pip install requests urllib3 certifi

echo 📅 Installing date/time tools...
python -m pip install python-dateutil

echo 📝 Installing logging tools...
python -m pip install colorlog

echo 🖼️ Installing file processing...
python -m pip install Pillow

echo 📊 Installing monitoring tools...
python -m pip install tqdm psutil

echo ⏰ Installing scheduling...
python -m pip install schedule

echo 🔧 Installing additional utilities...
python -m pip install click

REM Verify installation
echo.
echo ✅ Verifying installation...
python -c "import telegram; print('✅ Telegram Bot OK')" 2>nul || echo "⚠️ Telegram Bot: Manual check needed"
python -c "import googleapiclient; print('✅ Google API OK')" 2>nul || echo "⚠️ Google API: Manual check needed"
python -c "import aiofiles; print('✅ Async Files OK')" 2>nul || echo "⚠️ Async Files: Manual check needed"

echo.
echo 🎉 INSTALLATION COMPLETE!
echo.
echo 🚀 Next steps:
echo   1. Run: START_BOT.bat
echo   2. Follow setup wizard
echo   3. Upload Google Drive credentials
echo   4. Start backing up!
echo.

pause
