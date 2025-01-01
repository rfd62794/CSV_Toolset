import pandas as pd
import os
import chardet

class InspectorProcessor:
    @staticmethod
    def get_basic_info(file_path):
        """
        Gets basic file information.
        
        Returns:
            dict: Contains file size, encoding, etc.
        """
        file_size = os.path.getsize(file_path)
        
        # Detect encoding
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            
        return {
            'file_size': file_size,
            'encoding': encoding
        }
    
    @classmethod
    def analyze_data(cls, file_path, progress_callback=None):
        """
        Performs detailed analysis of CSV data.
        
        Args:
            file_path: Path to CSV file
            progress_callback: Optional callback for progress updates
            
        Returns:
            dict: Contains detailed statistics about the data
        """
        # Get basic info first
        info = cls.get_basic_info(file_path)
        
        if progress_callback:
            progress_callback(20, "Reading data...")
            
        # Read with pandas for detailed analysis
        df = pd.read_csv(file_path, encoding=info['encoding'])
        
        if progress_callback:
            progress_callback(40, "Analyzing columns...")
            
        # Analyze each column
        column_stats = {}
        total_columns = len(df.columns)
        
        for idx, col in enumerate(df.columns):
            column_stats[col] = {
                'type': str(df[col].dtype),
                'unique_values': df[col].nunique(),
                'null_count': df[col].isnull().sum(),
                'sample_values': df[col].head().tolist()
            }
            
            if progress_callback:
                progress = 40 + (idx / total_columns * 40)
                progress_callback(progress, f"Analyzing column: {col}")
        
        # Compile all statistics
        stats = {
            'file_info': {
                'size': info['file_size'],
                'encoding': info['encoding'],
                'total_rows': len(df),
                'total_columns': total_columns
            },
            'column_stats': column_stats
        }
        
        if progress_callback:
            progress_callback(100, "Analysis complete!")
            
        return stats
    
    @staticmethod
    def format_stats(stats):
        """
        Formats statistics into human-readable text.
        
        Returns:
            str: Formatted statistics
        """
        lines = [
            "File Statistics:",
            f"- Size: {stats['file_info']['size']:,} bytes",
            f"- Encoding: {stats['file_info']['encoding']}",
            f"- Rows: {stats['file_info']['total_rows']:,}",
            f"- Columns: {stats['file_info']['total_columns']:,}",
            "\nColumn Information:"
        ]
        
        for col, col_stats in stats['column_stats'].items():
            lines.extend([
                f"\n{col}:",
                f"- Type: {col_stats['type']}",
                f"- Unique Values: {col_stats['unique_values']:,}",
                f"- Null Count: {col_stats['null_count']:,}",
                "- Sample Values: " + ", ".join(str(v) for v in col_stats['sample_values'])
            ])
            
        return '\n'.join(lines) 