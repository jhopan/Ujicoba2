"""
Folder Manager for organizing backup files and managing folder structures
"""

import os
import shutil
import asyncio
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class FolderManager:
    def __init__(self, base_backup_dir: str = "~/Backups"):
        self.base_backup_dir = Path(base_backup_dir).expanduser()
        self.supported_extensions = {
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg'],
            'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
            'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
            'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.pages'],
            'spreadsheets': ['.xls', '.xlsx', '.csv', '.ods', '.numbers'],
            'presentations': ['.ppt', '.pptx', '.odp', '.key'],
            'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
            'code': ['.py', '.js', '.html', '.css', '.cpp', '.java', '.php', '.rb'],
            'configs': ['.json', '.xml', '.yaml', '.yml', '.ini', '.cfg', '.conf'],
            'databases': ['.db', '.sqlite', '.sql', '.mdb']
        }
    
    def get_file_category(self, file_path: Path) -> str:
        """
        Determine the category of a file based on its extension
        
        Args:
            file_path: Path to the file
            
        Returns:
            str: Category name or 'other' if not found
        """
        file_extension = file_path.suffix.lower()
        
        for category, extensions in self.supported_extensions.items():
            if file_extension in extensions:
                return category
        
        return 'other'
    
    def create_date_folder_structure(self, date: datetime = None) -> Path:
        """
        Create folder structure based on date (YYYY-MM-DD format)
        
        Args:
            date: Date for folder creation (defaults to today)
            
        Returns:
            Path: Path to the created date folder
        """
        if date is None:
            date = datetime.now()
        
        date_folder = date.strftime("%Y-%m-%d")
        folder_path = self.base_backup_dir / date_folder
        
        try:
            folder_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created/verified date folder: {folder_path}")
            return folder_path
        except Exception as e:
            logger.error(f"Failed to create date folder {folder_path}: {e}")
            raise
    
    def create_category_folders(self, base_path: Path) -> Dict[str, Path]:
        """
        Create category subfolders within a base path
        
        Args:
            base_path: Base directory to create subfolders in
            
        Returns:
            dict: Mapping of category names to their paths
        """
        category_paths = {}
        
        for category in list(self.supported_extensions.keys()) + ['other']:
            category_path = base_path / category
            try:
                category_path.mkdir(parents=True, exist_ok=True)
                category_paths[category] = category_path
                logger.debug(f"Created/verified category folder: {category_path}")
            except Exception as e:
                logger.error(f"Failed to create category folder {category_path}: {e}")
                continue
        
        return category_paths
    
    def organize_file(self, source_file: Path, target_date: datetime = None) -> Path:
        """
        Organize a file into the appropriate folder structure
        
        Args:
            source_file: Path to the source file
            target_date: Date for organization (defaults to today)
            
        Returns:
            Path: Path where the file was organized
        """
        if not source_file.exists():
            raise FileNotFoundError(f"Source file not found: {source_file}")
        
        # Create date folder
        date_folder = self.create_date_folder_structure(target_date)
        
        # Create category folders
        category_folders = self.create_category_folders(date_folder)
        
        # Determine file category
        category = self.get_file_category(source_file)
        target_folder = category_folders[category]
        
        # Create target file path
        target_file = target_folder / source_file.name
        
        # Handle file name conflicts
        counter = 1
        original_target = target_file
        while target_file.exists():
            stem = original_target.stem
            suffix = original_target.suffix
            target_file = target_folder / f"{stem}_{counter}{suffix}"
            counter += 1
        
        try:
            # Copy the file
            shutil.copy2(source_file, target_file)
            logger.info(f"Organized file: {source_file} -> {target_file}")
            return target_file
        except Exception as e:
            logger.error(f"Failed to organize file {source_file}: {e}")
            raise
    
    async def organize_files_batch(self, file_list: List[Path], 
                                  target_date: datetime = None) -> Dict[str, List[Path]]:
        """
        Organize multiple files in batch
        
        Args:
            file_list: List of files to organize
            target_date: Date for organization (defaults to today)
            
        Returns:
            dict: Results with 'success' and 'failed' lists
        """
        results = {'success': [], 'failed': []}
        
        for file_path in file_list:
            try:
                organized_path = self.organize_file(file_path, target_date)
                results['success'].append(organized_path)
            except Exception as e:
                logger.error(f"Failed to organize {file_path}: {e}")
                results['failed'].append(file_path)
        
        return results
    
    def get_folder_structure(self, path: Path = None) -> Dict:
        """
        Get the current folder structure
        
        Args:
            path: Path to analyze (defaults to base backup dir)
            
        Returns:
            dict: Folder structure information
        """
        if path is None:
            path = self.base_backup_dir
        
        structure = {
            'path': str(path),
            'exists': path.exists(),
            'folders': [],
            'files': [],
            'total_size': 0
        }
        
        if not path.exists():
            return structure
        
        try:
            for item in path.iterdir():
                if item.is_dir():
                    structure['folders'].append({
                        'name': item.name,
                        'path': str(item),
                        'file_count': len(list(item.rglob('*'))) if item.exists() else 0
                    })
                else:
                    file_size = item.stat().st_size
                    structure['files'].append({
                        'name': item.name,
                        'path': str(item),
                        'size': file_size,
                        'modified': datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                    })
                    structure['total_size'] += file_size
        except Exception as e:
            logger.error(f"Failed to get folder structure for {path}: {e}")
        
        return structure
    
    def clean_empty_folders(self, path: Path = None) -> int:
        """
        Remove empty folders recursively
        
        Args:
            path: Path to clean (defaults to base backup dir)
            
        Returns:
            int: Number of folders removed
        """
        if path is None:
            path = self.base_backup_dir
        
        removed_count = 0
        
        if not path.exists():
            return removed_count
        
        try:
            # Process subfolders first (bottom-up)
            for item in path.iterdir():
                if item.is_dir():
                    removed_count += self.clean_empty_folders(item)
            
            # Check if current folder is empty and remove if so
            if path.exists() and not any(path.iterdir()):
                path.rmdir()
                removed_count += 1
                logger.info(f"Removed empty folder: {path}")
        
        except Exception as e:
            logger.error(f"Failed to clean folder {path}: {e}")
        
        return removed_count
    
    def get_category_stats(self, date_folder: Path = None) -> Dict[str, Dict]:
        """
        Get statistics for each file category
        
        Args:
            date_folder: Specific date folder to analyze
            
        Returns:
            dict: Statistics for each category
        """
        if date_folder is None:
            date_folder = self.create_date_folder_structure()
        
        stats = {}
        
        for category in list(self.supported_extensions.keys()) + ['other']:
            category_path = date_folder / category
            category_stats = {
                'file_count': 0,
                'total_size': 0,
                'file_types': {}
            }
            
            if category_path.exists():
                for file_path in category_path.rglob('*'):
                    if file_path.is_file():
                        file_size = file_path.stat().st_size
                        file_extension = file_path.suffix.lower()
                        
                        category_stats['file_count'] += 1
                        category_stats['total_size'] += file_size
                        
                        if file_extension in category_stats['file_types']:
                            category_stats['file_types'][file_extension]['count'] += 1
                            category_stats['file_types'][file_extension]['size'] += file_size
                        else:
                            category_stats['file_types'][file_extension] = {
                                'count': 1,
                                'size': file_size
                            }
            
            stats[category] = category_stats
        
        return stats
    
    def create_backup_manifest(self, date_folder: Path = None) -> Path:
        """
        Create a manifest file listing all files in the backup
        
        Args:
            date_folder: Date folder to create manifest for
            
        Returns:
            Path: Path to the created manifest file
        """
        if date_folder is None:
            date_folder = self.create_date_folder_structure()
        
        manifest_file = date_folder / "backup_manifest.json"
        manifest_data = {
            'created': datetime.now().isoformat(),
            'backup_date': date_folder.name,
            'categories': self.get_category_stats(date_folder),
            'file_list': []
        }
        
        # Add detailed file list
        for file_path in date_folder.rglob('*'):
            if file_path.is_file() and file_path.name != "backup_manifest.json":
                relative_path = file_path.relative_to(date_folder)
                manifest_data['file_list'].append({
                    'path': str(relative_path),
                    'size': file_path.stat().st_size,
                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    'category': self.get_file_category(file_path)
                })
        
        try:
            import json
            with open(manifest_file, 'w') as f:
                json.dump(manifest_data, f, indent=2)
            
            logger.info(f"Created backup manifest: {manifest_file}")
            return manifest_file
        except Exception as e:
            logger.error(f"Failed to create backup manifest: {e}")
            raise
