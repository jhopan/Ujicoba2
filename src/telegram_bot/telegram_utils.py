"""
Telegram Utilities for enhanced bot functionality
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Callable, Any
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

logger = logging.getLogger(__name__)

class TelegramUtils:
    def __init__(self):
        self.progress_messages = {}  # Store progress message IDs for updates
        self.user_sessions = {}  # Store user session data
    
    @staticmethod
    def create_inline_keyboard(buttons: List[List[Dict[str, str]]]) -> InlineKeyboardMarkup:
        """
        Create an inline keyboard from button data
        
        Args:
            buttons: List of button rows, each containing dicts with 'text' and 'callback_data'
            
        Returns:
            InlineKeyboardMarkup: Telegram inline keyboard
        """
        keyboard = []
        for row in buttons:
            keyboard_row = []
            for button in row:
                keyboard_row.append(
                    InlineKeyboardButton(
                        text=button['text'],
                        callback_data=button.get('callback_data'),
                        url=button.get('url')
                    )
                )
            keyboard.append(keyboard_row)
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def create_reply_keyboard(buttons: List[List[str]], 
                            one_time: bool = False,
                            resize: bool = True) -> ReplyKeyboardMarkup:
        """
        Create a reply keyboard from button texts
        
        Args:
            buttons: List of button rows
            one_time: Whether keyboard should hide after use
            resize: Whether to resize keyboard
            
        Returns:
            ReplyKeyboardMarkup: Telegram reply keyboard
        """
        keyboard = []
        for row in buttons:
            keyboard_row = []
            for button_text in row:
                keyboard_row.append(KeyboardButton(button_text))
            keyboard.append(keyboard_row)
        
        return ReplyKeyboardMarkup(
            keyboard,
            one_time_keyboard=one_time,
            resize_keyboard=resize
        )
    
    def get_main_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get the main menu inline keyboard"""
        buttons = [
            [
                {'text': '📱 Start Backup', 'callback_data': 'backup_start'},
                {'text': '⏸️ Stop Backup', 'callback_data': 'backup_stop'}
            ],
            [
                {'text': '👥 Manage Accounts', 'callback_data': 'accounts_menu'},
                {'text': '📁 Manage Folders', 'callback_data': 'folders_menu'}
            ],
            [
                {'text': '⚙️ Settings', 'callback_data': 'settings_menu'},
                {'text': '📊 Status', 'callback_data': 'show_status'}
            ],
            [
                {'text': '📋 View Logs', 'callback_data': 'view_logs'},
                {'text': '❓ Help', 'callback_data': 'show_help'}
            ]
        ]
        return self.create_inline_keyboard(buttons)
    
    def get_backup_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get backup management keyboard"""
        buttons = [
            [
                {'text': '🚀 Quick Backup', 'callback_data': 'backup_quick'},
                {'text': '📋 Custom Backup', 'callback_data': 'backup_custom'}
            ],
            [
                {'text': '⏰ Schedule Backup', 'callback_data': 'backup_schedule'},
                {'text': '🔄 Auto Backup On/Off', 'callback_data': 'backup_toggle_auto'}
            ],
            [
                {'text': '📊 Backup History', 'callback_data': 'backup_history'},
                {'text': '🔙 Back to Main', 'callback_data': 'main_menu'}
            ]
        ]
        return self.create_inline_keyboard(buttons)
    
    def get_accounts_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get accounts management keyboard"""
        buttons = [
            [
                {'text': '➕ Add Account', 'callback_data': 'account_add'},
                {'text': '📝 List Accounts', 'callback_data': 'account_list'}
            ],
            [
                {'text': '🔧 Configure Account', 'callback_data': 'account_configure'},
                {'text': '🗑️ Remove Account', 'callback_data': 'account_remove'}
            ],
            [
                {'text': '📊 Storage Usage', 'callback_data': 'account_usage'},
                {'text': '🔙 Back to Main', 'callback_data': 'main_menu'}
            ]
        ]
        return self.create_inline_keyboard(buttons)
    
    def get_settings_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Get settings management keyboard"""
        buttons = [
            [
                {'text': '📱 Backup Settings', 'callback_data': 'settings_backup'},
                {'text': '📁 Folder Settings', 'callback_data': 'settings_folders'}
            ],
            [
                {'text': '🌐 Network Settings', 'callback_data': 'settings_network'},
                {'text': '🔔 Notification Settings', 'callback_data': 'settings_notifications'}
            ],
            [
                {'text': '📊 View All Settings', 'callback_data': 'settings_view_all'},
                {'text': '↩️ Reset to Defaults', 'callback_data': 'settings_reset'}
            ],
            [
                {'text': '💾 Export Settings', 'callback_data': 'settings_export'},
                {'text': '📥 Import Settings', 'callback_data': 'settings_import'}
            ],
            [
                {'text': '🔙 Back to Main', 'callback_data': 'main_menu'}
            ]
        ]
        return self.create_inline_keyboard(buttons)
    
    async def send_progress_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE,
                                   title: str, progress: int, total: int,
                                   current_file: str = "") -> int:
        """
        Send or update a progress message
        
        Args:
            update: Telegram update object
            context: Bot context
            title: Progress title
            progress: Current progress value
            total: Total progress value
            current_file: Currently processing file
            
        Returns:
            int: Message ID of the progress message
        """
        try:
            percentage = (progress / total * 100) if total > 0 else 0
            progress_bar = self.create_progress_bar(percentage)
            
            message_text = f"🔄 *{title}*\n\n"
            message_text += f"{progress_bar} {percentage:.1f}%\n"
            message_text += f"📊 Progress: {progress}/{total}\n"
            
            if current_file:
                # Truncate long filenames
                if len(current_file) > 30:
                    current_file = current_file[:27] + "..."
                message_text += f"📄 Current: `{current_file}`\n"
            
            user_id = update.effective_user.id
            
            # Check if we have an existing progress message to update
            if user_id in self.progress_messages:
                try:
                    message = await context.bot.edit_message_text(
                        chat_id=update.effective_chat.id,
                        message_id=self.progress_messages[user_id],
                        text=message_text,
                        parse_mode=ParseMode.MARKDOWN
                    )
                    return message.message_id
                except Exception:
                    # If edit fails, send new message
                    pass
            
            # Send new progress message
            message = await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message_text,
                parse_mode=ParseMode.MARKDOWN
            )
            
            self.progress_messages[user_id] = message.message_id
            return message.message_id
            
        except Exception as e:
            logger.error(f"Failed to send progress message: {e}")
            return 0
    
    def create_progress_bar(self, percentage: float, length: int = 20) -> str:
        """
        Create a visual progress bar
        
        Args:
            percentage: Progress percentage (0-100)
            length: Length of the progress bar
            
        Returns:
            str: Progress bar string
        """
        filled = int(length * percentage / 100)
        bar = "█" * filled + "░" * (length - filled)
        return f"[{bar}]"
    
    async def send_status_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE,
                                status_data: Dict[str, Any]) -> None:
        """
        Send a formatted status message
        
        Args:
            update: Telegram update object
            context: Bot context
            status_data: Status information dictionary
        """
        try:
            message = "📊 *Backup System Status*\n\n"
            
            # System status
            system_status = status_data.get('system', {})
            message += f"🔋 System: {system_status.get('status', 'Unknown')}\n"
            message += f"🌐 Network: {system_status.get('network', 'Unknown')}\n"
            message += f"⏰ Last Check: {system_status.get('last_check', 'Never')}\n\n"
            
            # Backup status
            backup_status = status_data.get('backup', {})
            message += f"📱 *Backup Status*\n"
            message += f"Status: {backup_status.get('status', 'Idle')}\n"
            message += f"Files Queued: {backup_status.get('queued', 0)}\n"
            message += f"Files Completed: {backup_status.get('completed', 0)}\n"
            message += f"Files Failed: {backup_status.get('failed', 0)}\n\n"
            
            # Storage info
            storage_info = status_data.get('storage', {})
            message += f"💾 *Storage Usage*\n"
            for account in storage_info.get('accounts', []):
                name = account.get('name', 'Unknown')
                usage = account.get('usage_percentage', 0)
                message += f"{name}: {usage:.1f}% used\n"
            
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode=ParseMode.MARKDOWN
            )
            
        except Exception as e:
            logger.error(f"Failed to send status message: {e}")
    
    async def send_completion_notification(self, update: Update, context: ContextTypes.DEFAULT_TYPE,
                                         backup_results: Dict[str, Any]) -> None:
        """
        Send backup completion notification
        
        Args:
            update: Telegram update object
            context: Bot context
            backup_results: Backup results dictionary
        """
        try:
            success_count = backup_results.get('success_count', 0)
            failed_count = backup_results.get('failed_count', 0)
            total_size = backup_results.get('total_size', 0)
            duration = backup_results.get('duration', 0)
            
            if failed_count == 0:
                icon = "✅"
                status = "Completed Successfully"
            elif success_count > 0:
                icon = "⚠️"
                status = "Completed with Errors"
            else:
                icon = "❌"
                status = "Failed"
            
            message = f"{icon} *Backup {status}*\n\n"
            message += f"📊 Files Processed: {success_count + failed_count}\n"
            message += f"✅ Successful: {success_count}\n"
            message += f"❌ Failed: {failed_count}\n"
            message += f"📦 Total Size: {self.format_file_size(total_size)}\n"
            message += f"⏱️ Duration: {self.format_duration(duration)}\n"
            
            # Add failure details if any
            if failed_count > 0 and 'failed_files' in backup_results:
                message += f"\n❌ *Failed Files:*\n"
                for failed_file in backup_results['failed_files'][:5]:  # Show first 5
                    message += f"• {failed_file}\n"
                if len(backup_results['failed_files']) > 5:
                    message += f"• ... and {len(backup_results['failed_files']) - 5} more\n"
            
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode=ParseMode.MARKDOWN
            )
            
        except Exception as e:
            logger.error(f"Failed to send completion notification: {e}")
    
    def format_file_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def format_duration(self, seconds: int) -> str:
        """Format duration in human readable format"""
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            minutes = seconds // 60
            remaining_seconds = seconds % 60
            return f"{minutes}m {remaining_seconds}s"
        else:
            hours = seconds // 3600
            remaining_minutes = (seconds % 3600) // 60
            return f"{hours}h {remaining_minutes}m"
    
    def set_user_session_data(self, user_id: int, key: str, value: Any) -> None:
        """Store data in user session"""
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {}
        self.user_sessions[user_id][key] = value
    
    def get_user_session_data(self, user_id: int, key: str, default: Any = None) -> Any:
        """Get data from user session"""
        return self.user_sessions.get(user_id, {}).get(key, default)
    
    def clear_user_session(self, user_id: int) -> None:
        """Clear user session data"""
        if user_id in self.user_sessions:
            del self.user_sessions[user_id]
    
    async def send_error_notification(self, update: Update, context: ContextTypes.DEFAULT_TYPE,
                                    error_message: str, error_details: str = "") -> None:
        """
        Send error notification to user
        
        Args:
            update: Telegram update object
            context: Bot context
            error_message: Main error message
            error_details: Additional error details
        """
        try:
            message = f"❌ *Error Occurred*\n\n"
            message += f"📋 {error_message}\n"
            
            if error_details:
                message += f"\n🔍 *Details:*\n"
                # Truncate long error details
                if len(error_details) > 200:
                    error_details = error_details[:197] + "..."
                message += f"`{error_details}`\n"
            
            message += f"\n⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                parse_mode=ParseMode.MARKDOWN
            )
            
        except Exception as e:
            logger.error(f"Failed to send error notification: {e}")
    
    def validate_user_permissions(self, user_id: int, allowed_users: List[int]) -> bool:
        """
        Check if user has permission to use the bot
        
        Args:
            user_id: Telegram user ID
            allowed_users: List of allowed user IDs
            
        Returns:
            bool: True if user is allowed
        """
        # If no restrictions, allow all users
        if not allowed_users:
            return True
        
        return user_id in allowed_users
