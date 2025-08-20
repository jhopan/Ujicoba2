#!/usr/bin/env python3
"""
🚀 Advanced Backup System - Main Entry Point
📱 Optimized for Android Termux with Telegram Bot Interface

Usage:
    python main.py              # Start with auto-detection
    python main.py --setup      # Force setup mode
    python main.py --bot        # Start bot directly
    python main.py --help       # Show help
"""

import sys
import os
import asyncio
import argparse
from pathlib import Path

# Add src to Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

def setup_logging():
    """Setup basic logging"""
    import logging
    
    # Create logs directory
    logs_dir = PROJECT_ROOT / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(logs_dir / "main.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)

def check_termux_environment():
    """Check if running in Termux"""
    return "com.termux" in os.environ.get("PREFIX", "")

def check_requirements():
    """Check if required packages are installed"""
    try:
        import telegram
        import google.auth
        return True
    except ImportError as e:
        print(f"❌ Missing requirements: {e}")
        print("📦 Install: pip install -r requirements.txt")
        return False

async def start_termux_bot():
    """Start the Termux-optimized bot"""
    try:
        # Try to import the termux bot first
        try:
            from src.telegram.termux_telegram_bot import TermuxTelegramBot
            
            print("🤖 Starting Termux Telegram Bot...")
            bot = TermuxTelegramBot()
            await bot.auto_start()
            return True
            
        except ImportError:
            # Fallback to any available bot
            print("🔄 Termux bot not found, trying alternatives...")
            
            # Check what bots are available
            import os
            telegram_dir = PROJECT_ROOT / "src" / "telegram"
            if telegram_dir.exists():
                bot_files = list(telegram_dir.glob("*bot.py"))
                print(f"📁 Available bots: {[f.name for f in bot_files]}")
                
                # Try to run any available bot
                for bot_file in bot_files:
                    if "termux" in bot_file.name:
                        print(f"🚀 Starting {bot_file.name}...")
                        # Run the bot file directly
                        import subprocess
                        result = subprocess.run([
                            "python3", str(bot_file)
                        ], cwd=str(PROJECT_ROOT))
                        return result.returncode == 0
            
            print("❌ No suitable bot found")
            return False
        
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        print("💡 Try: python src/telegram/termux_telegram_bot.py")
        return False

async def start_generic_bot():
    """Start generic backup system"""
    try:
        # Try to import and start main backup system
        print("🚀 Starting generic backup system...")
        # Placeholder for generic implementation
        print("⚠️ Generic mode not yet implemented")
        print("💡 Use Termux bot for full functionality")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("🚀 ADVANCED BACKUP SYSTEM")
    print("📱 Telegram Bot with Google Drive Integration")
    print("🤖 User-Friendly Interface for Android Termux")
    print("=" * 60)
    print()

def print_system_info():
    """Print system information"""
    import platform
    
    is_termux = check_termux_environment()
    
    print("📊 System Information:")
    print(f"   🐍 Python: {platform.python_version()}")
    print(f"   💻 Platform: {platform.system()}")
    print(f"   📱 Termux: {'✅ Yes' if is_termux else '❌ No'}")
    print(f"   📁 Project: {PROJECT_ROOT}")
    print()

async def main():
    """Main entry point"""
    # Parse arguments
    parser = argparse.ArgumentParser(description="Advanced Backup System")
    parser.add_argument("--setup", action="store_true", help="Force setup mode")
    parser.add_argument("--bot", action="store_true", help="Start bot directly")
    parser.add_argument("--info", action="store_true", help="Show system info")
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging()
    logger.info("Starting Advanced Backup System")
    
    # Print banner
    print_banner()
    
    # Show system info if requested
    if args.info:
        print_system_info()
        return
    
    # Check requirements
    if not check_requirements():
        return
    
    # Determine environment and start appropriate bot
    is_termux = check_termux_environment()
    
    if is_termux or args.bot:
        print("📱 Detected Termux environment")
        success = await start_termux_bot()
    else:
        print("💻 Using generic mode")
        success = await start_generic_bot()
    
    if not success:
        print("❌ Failed to start backup system")
        sys.exit(1)

if __name__ == "__main__":
    try:
        # Check Python version
        if sys.version_info < (3, 8):
            print("❌ Python 3.8+ required")
            sys.exit(1)
        
        # Run main
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print("\n⏹️ Backup system stopped")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
