import chardet
import csv
import os
from typing import Optional, Dict, Any

class CSVHandler:
    @staticmethod
    def detect_encoding(file_path: str) -> str:
        """Detect the encoding of a CSV file."""
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            return result['encoding']
    
    @staticmethod
    def safe_read_csv(file_path: str, encoding: Optional[str] = None) -> tuple[list, list]:
        """Safely read a CSV file with encoding detection."""
        if not encoding:
            encoding = CSVHandler.detect_encoding(file_path)
            
        with open(file_path, 'r', encoding=encoding) as f:
            reader = csv.reader(f)
            header = next(reader)
            data = list(reader)
        return header, data
    
    @staticmethod
    def safe_write_csv(file_path: str, header: list, data: list, encoding: str = 'utf-8'):
        """Safely write data to a CSV file."""
        with open(file_path, 'w', newline='', encoding=encoding) as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data)

class FileManager:
    @staticmethod
    def generate_output_path(input_path: str, suffix: str) -> str:
        """Generate an output file path with a suffix."""
        base, ext = os.path.splitext(input_path)
        return f"{base}_{suffix}{ext}" 