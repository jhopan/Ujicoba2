"""
📂 Popular Folder Handlers - Music, Movies, Games, Camera, etc.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

from ...config.manager import config_manager, STORAGE_PATH

class PopularFolderHandler:
    """📂 Handle popular folder shortcuts (Music, Movies, Games, etc.)"""
    
    @staticmethod
    async def add_folder_music(query):
        """🎵 Add Music folder"""
        music_path = str(STORAGE_PATH / "Music")
        config_manager.save_folder_config("Music", music_path)
        await query.answer("✅ Music folder added")
        await PopularFolderHandler._show_folder_added_success(query, "Music", music_path, "🎵", "MP3, FLAC, M4A, etc.")
    
    @staticmethod
    async def add_folder_movies(query):
        """🎬 Add Movies folder"""
        movies_path = str(STORAGE_PATH / "Movies")
        config_manager.save_folder_config("Movies", movies_path)
        await query.answer("✅ Movies folder added")
        await PopularFolderHandler._show_folder_added_success(query, "Movies", movies_path, "🎬", "MP4, AVI, MKV, etc.")
    
    @staticmethod
    async def add_folder_games(query):
        """🎮 Add Games Data folder"""
        games_path = str(STORAGE_PATH / "Android" / "data")
        config_manager.save_folder_config("Games Data", games_path)
        await query.answer("✅ Games data folder added")
        await PopularFolderHandler._show_folder_added_success(query, "Games Data", games_path, "🎮", "Game saves & data")
    
    @staticmethod
    async def add_folder_camera(query):
        """📷 Add Camera folder"""
        camera_path = str(STORAGE_PATH / "DCIM" / "Camera")
        config_manager.save_folder_config("Camera", camera_path)
        await query.answer("✅ Camera folder added")
        await PopularFolderHandler._show_folder_added_success(query, "Camera", camera_path, "📷", "Photos & Videos")
    
    @staticmethod
    async def add_folder_recordings(query):
        """🎙️ Add Recordings folder"""
        recordings_path = str(STORAGE_PATH / "Recordings")
        config_manager.save_folder_config("Recordings", recordings_path)
        await query.answer("✅ Recordings folder added")
        await PopularFolderHandler._show_folder_added_success(query, "Recordings", recordings_path, "🎙️", "Voice recordings")
    
    @staticmethod
    async def add_folder_backups(query):
        """💾 Add Backups folder"""
        backups_path = str(STORAGE_PATH / "Backups")
        config_manager.save_folder_config("Backups", backups_path)
        await query.answer("✅ Backups folder added")
        await PopularFolderHandler._show_folder_added_success(query, "Backups", backups_path, "💾", "App & system backups")
    
    @staticmethod
    async def add_folder_screenshots(query):
        """📱 Add Screenshots folder"""
        screenshots_path = str(STORAGE_PATH / "Pictures" / "Screenshots")
        config_manager.save_folder_config("Screenshots", screenshots_path)
        await query.answer("✅ Screenshots folder added")
        await PopularFolderHandler._show_folder_added_success(query, "Screenshots", screenshots_path, "📱", "Screen captures")
    
    @staticmethod
    async def _show_folder_added_success(query, folder_name: str, folder_path: str, icon: str, file_types: str):
        """Helper method to show folder added success message"""
        success_text = f"""
✅ *{folder_name.upper()} FOLDER ADDED*

{icon} *Folder:* {folder_name}
📂 *Path:* `{folder_path}`
📊 *Content:* {file_types}

🎯 *Features:*
• Automatic file detection
• Smart organization
• Incremental backup
• Safe file handling

💡 *{folder_name} files will be backed up to Google Drive*
        """
        
        keyboard = [
            [InlineKeyboardButton("📂 Add More Popular", callback_data="add_custom_path")],
            [InlineKeyboardButton("📁 Manage Folders", callback_data="manage_folders")],
            [InlineKeyboardButton("🚀 Start Backup", callback_data="quick_backup")],
            [InlineKeyboardButton("🔙 Main Menu", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            success_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )