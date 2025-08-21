#!/usr/bin/env python3
"""
🚀 TERMUX BACKUP SYSTEM - MODULAR MAIN
📱 Main entry point for modular Termux Telegram Bot
🎯 Simplified and clean architecture
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

# Import our modular telegram bot
from telegram.termux_telegram_bot import TermuxTelegramBot

# Configure logging
def setup_logging():
    """Set up logging configuration"""
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "bot.log"),
            logging.StreamHandler()
        ]
    )

def print_banner():
    """Print startup banner"""
    print("=" * 60)
    print("🤖 TERMUX BACKUP SYSTEM - MODULAR ARCHITECTURE")
    print("📱 Telegram Bot Controlled (Android Termux)")
    print("☁️ Google Drive Integration")
    print("🎯 Clean & Maintainable Code Structure")
    print("=" * 60)

async def main():
    """Main entry point for modular system"""
    try:
        # Set up logging
        setup_logging()
        
        # Print startup banner
        print_banner()
        
        logging.info("🚀 Starting Termux Backup System with modular architecture...")
        
        # Check if running in Termux
        is_termux = os.path.exists("/data/data/com.termux")
        if is_termux:
            logging.info("📱 Termux environment detected")
        else:
            logging.info("💻 Development environment detected")
        
        # Create and start the modular bot
        bot = TermuxTelegramBot()
        
        try:
            await bot.auto_start()
            return 0
        except KeyboardInterrupt:
            logging.info("🔌 Received keyboard interrupt")
            return 0
        except Exception as e:
            logging.error(f"❌ Bot error: {e}")
            return 1
            
    except Exception as e:
        logging.error(f"❌ Fatal error: {e}")
        print(f"❌ Fatal error: {e}")
        return 1

def main_sync():
    """Synchronous main entry point"""
    return asyncio.run(main())

if __name__ == "__main__":
    # Ensure proper event loop handling
    if sys.platform == "win32":
        # Use ProactorEventLoop on Windows for better compatibility
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    try:
        exit_code = main_sync()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n🔌 Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
