import pandas as pd
import chardet

class DataReader:
    """Handles all CSV file reading operations"""
    
    @staticmethod
    def detect_encoding(file_path):
        """Detects file encoding"""
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            return result['encoding']
    
    @classmethod
    def read_csv(cls, file_path, **options):
        """Reads CSV with automatic encoding detection"""
        encoding = options.pop('encoding', None)
        if not encoding:
            encoding = cls.detect_encoding(file_path)
        
        return pd.read_csv(file_path, encoding=encoding, **options)
    
    @classmethod
    def read_preview(cls, file_path, nrows=5):
        """Reads first few rows for preview"""
        return cls.read_csv(file_path, nrows=nrows)
    
    @classmethod
    def get_columns(cls, file_path):
        """Gets column names without reading entire file"""
        return cls.read_csv(file_path, nrows=0).columns.tolist() 