@echo off
title Ultimate Backup System - Telegram Bot

echo.
echo ========================================
echo 🚀 ULTIMATE BACKUP SYSTEM
echo 📱 Telegram Bot - Auto Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python 3.7+
    echo 📦 Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found

REM Change to script directory
cd /d "%~dp0"

echo 🚀 Starting Ultimate Telegram Bot...
echo 📱 Follow the setup wizard in the console
echo ⚡ Bot will auto-restart after configuration
echo.

REM Run the bot
python run_bot.py

echo.
echo 👋 Bot stopped
pause
