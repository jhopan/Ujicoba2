#!/usr/bin/env python3
"""
Advanced Backup System with Telegram Bot Control
Main entry point for the backup system
"""

import os
import sys
import asyncio
import logging
import signal
from pathlib import Path
from datetime import datetime

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

# Import our modules (updated for modular architecture)
from telegram.termux_telegram_bot import TermuxTelegramBot

# Configure logging
def setup_logging():
    """Set up logging configuration"""
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / "backup.log"
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Setup file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Reduce noise from external libraries
    logging.getLogger('telegram').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('google.auth').setLevel(logging.WARNING)

class BackupSystemManager:
    """Main manager for the backup system"""
    
    def __init__(self):
        self.settings = EnhancedSettings()
        self.database = DatabaseManager()
        self.network_manager = NetworkManager()
        self.backup_manager = None
        self.telegram_bot = None
        self.running = False
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logging.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False
    
    async def initialize(self):
        """Initialize all components"""
        try:
            logging.info("🚀 Initializing Advanced Backup System...")
            
            # Check network connectivity
            if not await self.network_manager.check_connectivity():
                logging.warning("⚠️ No network connectivity detected")
            
            # Initialize backup manager
            self.backup_manager = EnhancedBackupManager(
                settings=self.settings,
                database=self.database,
                network_manager=self.network_manager
            )
            
            # Initialize Telegram bot
            bot_token = self.settings.get('telegram.bot_token')
            if not bot_token or bot_token == 'your_bot_token_here':
                logging.error("❌ Telegram bot token not configured. Please update .env file.")
                return False
            
            self.telegram_bot = AdvancedTelegramBot(
                token=bot_token,
                backup_manager=self.backup_manager,
                settings=self.settings,
                database=self.database
            )
            
            await self.telegram_bot.initialize()
            
            # Log system startup
            self.database.log_system_event(
                'system_startup',
                {
                    'timestamp': datetime.now().isoformat(),
                    'version': '1.0',
                    'python_version': sys.version
                },
                'info'
            )
            
            logging.info("✅ System initialization completed successfully")
            return True
            
        except Exception as e:
            logging.error(f"❌ Failed to initialize system: {e}")
            return False
    
    async def start(self):
        """Start the backup system"""
        try:
            if not await self.initialize():
                return False
            
            logging.info("🏁 Starting backup system...")
            self.running = True
            
            # Start the Telegram bot
            bot_task = asyncio.create_task(self.telegram_bot.start())
            
            # Start background tasks
            scheduler_task = asyncio.create_task(self._run_scheduler())
            monitor_task = asyncio.create_task(self._monitor_system())
            
            # Wait for all tasks
            try:
                await asyncio.gather(bot_task, scheduler_task, monitor_task)
            except asyncio.CancelledError:
                logging.info("📴 Tasks cancelled, shutting down...")
            
            return True
            
        except Exception as e:
            logging.error(f"❌ Failed to start system: {e}")
            return False
    
    async def _run_scheduler(self):
        """Run scheduled backup tasks"""
        while self.running:
            try:
                # Check if auto backup is enabled
                if self.settings.get('backup.auto_schedule'):
                    schedule_time = self.settings.get('backup.schedule_time', '00:00')
                    current_time = datetime.now().strftime('%H:%M')
                    
                    if current_time == schedule_time:
                        logging.info("⏰ Starting scheduled backup...")
                        await self.backup_manager.run_backup_with_progress()
                        
                        # Wait until next minute to avoid running multiple times
                        await asyncio.sleep(60)
                
                # Check for retry queue
                failed_files = self.database.get_failed_files_for_retry()
                if failed_files:
                    logging.info(f"🔄 Retrying {len(failed_files)} failed files...")
                    await self.backup_manager.retry_failed_files(failed_files)
                
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logging.error(f"Error in scheduler: {e}")
                await asyncio.sleep(60)  # Wait longer on error
    
    async def _monitor_system(self):
        """Monitor system health and performance"""
        while self.running:
            try:
                # Check network connectivity
                network_ok = await self.network_manager.check_connectivity()
                
                # Log system metrics
                self.database.log_system_event(
                    'system_health_check',
                    {
                        'network_connectivity': network_ok,
                        'timestamp': datetime.now().isoformat()
                    },
                    'info'
                )
                
                # Clean up old logs periodically
                if datetime.now().hour == 2:  # Run at 2 AM
                    self.database.cleanup_old_logs(90)  # Keep 90 days
                
                await asyncio.sleep(300)  # Check every 5 minutes
                
            except Exception as e:
                logging.error(f"Error in system monitor: {e}")
                await asyncio.sleep(300)
    
    async def shutdown(self):
        """Gracefully shutdown the system"""
        logging.info("🛑 Shutting down backup system...")
        self.running = False
        
        try:
            if self.telegram_bot:
                await self.telegram_bot.stop()
            
            if self.backup_manager:
                await self.backup_manager.stop_backup()
            
            # Log shutdown
            self.database.log_system_event(
                'system_shutdown',
                {'timestamp': datetime.now().isoformat()},
                'info'
            )
            
            logging.info("✅ System shutdown completed")
            
        except Exception as e:
            logging.error(f"Error during shutdown: {e}")

async def main():
    """Main entry point"""
    try:
        # Set up logging
        setup_logging()
        
        # Print startup banner
        print("=" * 50)
        print("🤖 Advanced Backup System for Termux")
        print("📱 Telegram Bot Controlled")
        print("☁️ Google Drive Integration")
        print("=" * 50)
        
        # Check environment
        env_file = Path(__file__).parent.parent / ".env"
        if not env_file.exists():
            print("❌ Error: .env file not found!")
            print("📝 Please copy .env.example to .env and configure it")
            print("🔧 Edit with: nano .env")
            return 1
        
        # Load environment variables
        try:
            from dotenv import load_dotenv
            load_dotenv(env_file)
        except ImportError:
            logging.warning("python-dotenv not installed, using OS environment")
        
        # Create and start the system
        system = BackupSystemManager()
        
        try:
            success = await system.start()
            return 0 if success else 1
        except KeyboardInterrupt:
            logging.info("🔌 Received keyboard interrupt")
            return 0
        finally:
            await system.shutdown()
            
    except Exception as e:
        logging.error(f"❌ Fatal error: {e}")
        return 1

if __name__ == "__main__":
    # Ensure proper event loop handling
    if sys.platform == "win32":
        # Use ProactorEventLoop on Windows
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n🔌 Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
