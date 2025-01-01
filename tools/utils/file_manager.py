import os
import chardet

class FileManager:
    @staticmethod
    def detect_encoding(file_path):
        """Detects the encoding of a file"""
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            return result['encoding']
    
    @staticmethod
    def generate_output_path(input_path, suffix):
        """
        Generates an output file path by adding a suffix.
        
        Args:
            input_path: Original file path
            suffix: Suffix to add before extension
            
        Returns:
            str: New file path with suffix
        """
        base, ext = os.path.splitext(input_path)
        return f"{base}_{suffix}{ext}"
    
    @staticmethod
    def validate_csv_file(file_path):
        """
        Validates that a file exists and has .csv extension.
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not file_path:
            return False, "No file selected"
            
        if not os.path.exists(file_path):
            return False, f"File not found: {file_path}"
            
        if not file_path.lower().endswith('.csv'):
            return False, "Selected file is not a CSV file"
            
        return True, None 