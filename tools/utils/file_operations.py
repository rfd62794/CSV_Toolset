import os
from typing import Dict, Any, List

class FileOperations:
    """Handles common file operations"""
    
    @staticmethod
    def get_file_info(file_path: str) -> Dict[str, Any]:
        """Gets file information"""
        return {
            'size': os.path.getsize(file_path),
            'modified': os.path.getmtime(file_path),
            'created': os.path.getctime(file_path),
            'extension': os.path.splitext(file_path)[1].lower()
        }
    
    @staticmethod
    def ensure_directory(file_path: str) -> None:
        """Ensures directory exists for file path"""
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
    
    @staticmethod
    def generate_unique_path(base_path: str) -> str:
        """Generates unique file path by adding number if needed"""
        if not os.path.exists(base_path):
            return base_path
            
        name, ext = os.path.splitext(base_path)
        counter = 1
        while True:
            new_path = f"{name}_{counter}{ext}"
            if not os.path.exists(new_path):
                return new_path
            counter += 1 