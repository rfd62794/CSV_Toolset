from ..utils.data_reader import DataReader
from ..utils.data_analyzer import DataAnalyzer
import os

class InspectorProcessor:
    def __init__(self):
        self.reader = DataReader()
        self.analyzer = DataAnalyzer()
    
    def get_basic_info(self, file_path):
        """Gets basic file information"""
        return {
            'file_size': os.path.getsize(file_path),
            'encoding': self.reader.detect_encoding(file_path)
        }
    
    def analyze_data(self, file_path, progress_callback=None):
        """Performs detailed analysis of CSV data"""
        # Get basic info
        info = self.get_basic_info(file_path)
        
        if progress_callback:
            progress_callback(20, "Reading data...")
        
        # Read data
        df = self.reader.read_csv(file_path, encoding=info['encoding'])
        
        if progress_callback:
            progress_callback(40, "Analyzing columns...")
        
        # Analyze columns
        column_stats = self.analyzer.analyze_dataframe(df)
        
        # Compile statistics
        stats = {
            'file_info': {
                'size': info['file_size'],
                'encoding': info['encoding'],
                'total_rows': len(df),
                'total_columns': len(df.columns)
            },
            'column_stats': column_stats
        }
        
        if progress_callback:
            progress_callback(100, "Analysis complete!")
        
        return stats 