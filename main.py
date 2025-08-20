#!/usr/bin/env python3
"""
🚀 Advanced Backup System - Main Entry Point
📱 Optimized for Android Termux with Telegram Bot Interface

Usage:
    python main.py              # Start Telegram bot
"""

import sys
import os
from pathlib import Path

# Add src to Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

def main():
    """Main entry point - Start the Telegram bot"""
    try:
        # Import and start the Termux Telegram bot
        from telegram.termux_telegram_bot import main as start_bot
        print("🚀 Starting Advanced Backup System...")
        print("📱 Telegram Bot Interface")
        print("=" * 50)
        start_bot()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        print("💡 Make sure you have configured the .env file")
        print("💡 Run: ./quick_start.sh for setup")
        sys.exit(1)

if __name__ == "__main__":
    main()
