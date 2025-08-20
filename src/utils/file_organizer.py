"""
File Organizer for advanced file management and organization
"""

import os
import shutil
import hashlib
import mimetypes
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Set, Tuple
import logging

logger = logging.getLogger(__name__)

class FileOrganizer:
    def __init__(self, base_dir: str = "~/Downloads"):
        self.base_dir = Path(base_dir).expanduser()
        self.duplicate_action = "skip"  # skip, overwrite, rename
        self.file_filters = {
            'min_size': 0,  # Minimum file size in bytes
            'max_size': None,  # Maximum file size in bytes (None = no limit)
            'extensions': [],  # Specific extensions to include (empty = all)
            'exclude_extensions': ['.tmp', '.temp', '.log'],  # Extensions to exclude
            'exclude_patterns': ['.*', '__pycache__', 'node_modules']  # Patterns to exclude
        }
    
    def calculate_file_hash(self, file_path: Path, algorithm: str = 'md5') -> str:
        """
        Calculate hash of a file for duplicate detection
        
        Args:
            file_path: Path to the file
            algorithm: Hash algorithm to use
            
        Returns:
            str: File hash
        """
        hash_obj = hashlib.new(algorithm)
        
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        except Exception as e:
            logger.error(f"Failed to calculate hash for {file_path}: {e}")
            return ""
    
    def get_file_metadata(self, file_path: Path) -> Dict:
        """
        Get comprehensive metadata for a file
        
        Args:
            file_path: Path to the file
            
        Returns:
            dict: File metadata
        """
        try:
            stat = file_path.stat()
            mime_type, _ = mimetypes.guess_type(str(file_path))
            
            metadata = {
                'name': file_path.name,
                'stem': file_path.stem,
                'suffix': file_path.suffix,
                'size': stat.st_size,
                'size_human': self.format_file_size(stat.st_size),
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'accessed': datetime.fromtimestamp(stat.st_atime).isoformat(),
                'mime_type': mime_type,
                'is_hidden': file_path.name.startswith('.'),
                'hash': self.calculate_file_hash(file_path)
            }
            
            return metadata
        except Exception as e:
            logger.error(f"Failed to get metadata for {file_path}: {e}")
            return {}
    
    def format_file_size(self, size_bytes: int) -> str:
        """
        Format file size in human-readable format
        
        Args:
            size_bytes: Size in bytes
            
        Returns:
            str: Formatted size
        """
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def should_include_file(self, file_path: Path) -> bool:
        """
        Check if a file should be included based on filters
        
        Args:
            file_path: Path to check
            
        Returns:
            bool: True if file should be included
        """
        try:
            # Check if file exists
            if not file_path.exists() or not file_path.is_file():
                return False
            
            # Check exclude patterns
            for pattern in self.file_filters['exclude_patterns']:
                if pattern in str(file_path):
                    return False
            
            # Check exclude extensions
            if file_path.suffix.lower() in self.file_filters['exclude_extensions']:
                return False
            
            # Check include extensions (if specified)
            if (self.file_filters['extensions'] and 
                file_path.suffix.lower() not in self.file_filters['extensions']):
                return False
            
            # Check file size
            file_size = file_path.stat().st_size
            if file_size < self.file_filters['min_size']:
                return False
            
            if (self.file_filters['max_size'] is not None and 
                file_size > self.file_filters['max_size']):
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error checking file filter for {file_path}: {e}")
            return False
    
    def find_files_to_backup(self, search_paths: List[Path] = None) -> List[Path]:
        """
        Find all files that should be backed up
        
        Args:
            search_paths: Paths to search (defaults to base_dir)
            
        Returns:
            List[Path]: List of files to backup
        """
        if search_paths is None:
            search_paths = [self.base_dir]
        
        files_to_backup = []
        
        for search_path in search_paths:
            if not search_path.exists():
                logger.warning(f"Search path does not exist: {search_path}")
                continue
            
            try:
                if search_path.is_file():
                    if self.should_include_file(search_path):
                        files_to_backup.append(search_path)
                else:
                    # Recursively find files
                    for file_path in search_path.rglob('*'):
                        if self.should_include_file(file_path):
                            files_to_backup.append(file_path)
            
            except Exception as e:
                logger.error(f"Error searching path {search_path}: {e}")
                continue
        
        logger.info(f"Found {len(files_to_backup)} files to backup")
        return files_to_backup
    
    def find_duplicates(self, file_list: List[Path]) -> Dict[str, List[Path]]:
        """
        Find duplicate files based on hash
        
        Args:
            file_list: List of files to check
            
        Returns:
            dict: Hash to file list mapping for duplicates
        """
        hash_to_files = {}
        duplicates = {}
        
        for file_path in file_list:
            try:
                file_hash = self.calculate_file_hash(file_path)
                if not file_hash:
                    continue
                
                if file_hash in hash_to_files:
                    if file_hash not in duplicates:
                        duplicates[file_hash] = [hash_to_files[file_hash]]
                    duplicates[file_hash].append(file_path)
                else:
                    hash_to_files[file_hash] = file_path
            
            except Exception as e:
                logger.error(f"Error processing file for duplicates {file_path}: {e}")
                continue
        
        logger.info(f"Found {len(duplicates)} groups of duplicate files")
        return duplicates
    
    def handle_duplicate_file(self, source_path: Path, target_path: Path) -> Path:
        """
        Handle duplicate file based on configured action
        
        Args:
            source_path: Source file path
            target_path: Target file path
            
        Returns:
            Path: Final target path
        """
        if not target_path.exists():
            return target_path
        
        if self.duplicate_action == "skip":
            logger.info(f"Skipping duplicate file: {source_path}")
            return target_path
        
        elif self.duplicate_action == "overwrite":
            logger.info(f"Overwriting existing file: {target_path}")
            return target_path
        
        elif self.duplicate_action == "rename":
            # Find a unique name
            counter = 1
            original_target = target_path
            while target_path.exists():
                stem = original_target.stem
                suffix = original_target.suffix
                target_path = original_target.parent / f"{stem}_{counter}{suffix}"
                counter += 1
            
            logger.info(f"Renamed to avoid duplicate: {target_path}")
            return target_path
        
        return target_path
    
    def create_backup_catalog(self, files: List[Path], output_path: Path) -> Dict:
        """
        Create a detailed catalog of backup files
        
        Args:
            files: List of files to catalog
            output_path: Path to save catalog
            
        Returns:
            dict: Catalog data
        """
        catalog = {
            'created': datetime.now().isoformat(),
            'total_files': len(files),
            'total_size': 0,
            'files': [],
            'statistics': {
                'by_extension': {},
                'by_size_range': {'<1MB': 0, '1-10MB': 0, '10-100MB': 0, '>100MB': 0},
                'by_date': {}
            }
        }
        
        for file_path in files:
            try:
                metadata = self.get_file_metadata(file_path)
                if not metadata:
                    continue
                
                catalog['files'].append(metadata)
                catalog['total_size'] += metadata['size']
                
                # Update statistics
                ext = metadata['suffix'].lower()
                catalog['statistics']['by_extension'][ext] = \
                    catalog['statistics']['by_extension'].get(ext, 0) + 1
                
                # Size range statistics
                size_mb = metadata['size'] / (1024 * 1024)
                if size_mb < 1:
                    catalog['statistics']['by_size_range']['<1MB'] += 1
                elif size_mb < 10:
                    catalog['statistics']['by_size_range']['1-10MB'] += 1
                elif size_mb < 100:
                    catalog['statistics']['by_size_range']['10-100MB'] += 1
                else:
                    catalog['statistics']['by_size_range']['>100MB'] += 1
                
                # Date statistics
                date_key = metadata['modified'][:10]  # YYYY-MM-DD
                catalog['statistics']['by_date'][date_key] = \
                    catalog['statistics']['by_date'].get(date_key, 0) + 1
            
            except Exception as e:
                logger.error(f"Error cataloging file {file_path}: {e}")
                continue
        
        # Save catalog
        try:
            import json
            with open(output_path, 'w') as f:
                json.dump(catalog, f, indent=2)
            logger.info(f"Created backup catalog: {output_path}")
        except Exception as e:
            logger.error(f"Failed to save catalog: {e}")
        
        return catalog
    
    def cleanup_source_files(self, file_list: List[Path], 
                           backup_successful: List[Path]) -> Dict[str, int]:
        """
        Clean up source files after successful backup
        
        Args:
            file_list: Original file list
            backup_successful: Files that were successfully backed up
            
        Returns:
            dict: Cleanup statistics
        """
        stats = {'deleted': 0, 'failed': 0, 'skipped': 0}
        
        successful_set = set(backup_successful)
        
        for file_path in file_list:
            try:
                if file_path in successful_set:
                    # Only delete if backup was successful
                    file_path.unlink()
                    stats['deleted'] += 1
                    logger.info(f"Deleted source file after backup: {file_path}")
                else:
                    stats['skipped'] += 1
                    logger.warning(f"Skipped deletion (backup failed): {file_path}")
            
            except Exception as e:
                stats['failed'] += 1
                logger.error(f"Failed to delete source file {file_path}: {e}")
        
        logger.info(f"Cleanup completed: {stats}")
        return stats
    
    def set_filter_options(self, **options):
        """
        Set file filter options
        
        Args:
            **options: Filter options to set
        """
        for key, value in options.items():
            if key in self.file_filters:
                self.file_filters[key] = value
                logger.info(f"Updated filter option {key}: {value}")
    
    def get_filter_summary(self) -> str:
        """
        Get a summary of current filter settings
        
        Returns:
            str: Filter summary
        """
        summary = "Current File Filters:\n"
        summary += f"  Min Size: {self.format_file_size(self.file_filters['min_size'])}\n"
        summary += f"  Max Size: {self.format_file_size(self.file_filters['max_size']) if self.file_filters['max_size'] else 'No limit'}\n"
        summary += f"  Include Extensions: {self.file_filters['extensions'] or 'All'}\n"
        summary += f"  Exclude Extensions: {self.file_filters['exclude_extensions']}\n"
        summary += f"  Exclude Patterns: {self.file_filters['exclude_patterns']}\n"
        summary += f"  Duplicate Action: {self.duplicate_action}\n"
        
        return summary
