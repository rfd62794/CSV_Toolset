import math
from typing import List, Tuple, Dict, Any
import pandas as pd
from pathlib import Path
from ..base.base_processor import BaseProcessor

class SplitterProcessor(BaseProcessor):
    """Processor for splitting CSV files"""
    
    def __init__(self):
        super().__init__()
        self.reader = self.get_reader()
        self.writer = self.get_writer()
    
    def split_file(self, file_path: str, split_type: str, size: int) -> List[str]:
        """Splits a CSV file into multiple files"""
        try:
            df = self.reader.read_csv(file_path)
            
            if split_type == "rows":
                return self._split_by_rows(df, file_path, size)
            elif split_type == "size":
                return self._split_by_size(df, file_path, size)
            else:
                raise ValueError(f"Invalid split type: {split_type}")
                
        except Exception as e:
            raise RuntimeError(f"Error splitting file: {str(e)}")
    
    def _split_by_rows(self, df: pd.DataFrame, file_path: str, rows_per_file: int) -> List[str]:
        """Splits DataFrame by number of rows"""
        total_rows = len(df)
        num_files = math.ceil(total_rows / rows_per_file)
        output_files = []
        
        for i in range(num_files):
            if self.progress:
                self.update_progress(
                    (i / num_files) * 100,
                    f"Creating split {i+1} of {num_files}..."
                )
            
            start_idx = i * rows_per_file
            end_idx = min((i + 1) * rows_per_file, total_rows)
            
            split_df = df.iloc[start_idx:end_idx]
            
            # Generate output filename
            base_path = Path(file_path)
            output_file = base_path.parent / f"{base_path.stem}_split{i+1}{base_path.suffix}"
            
            self.writer.write_csv(split_df, str(output_file))
            output_files.append(str(output_file))
        
        return output_files
    
    def _split_by_size(self, df: pd.DataFrame, file_path: str, max_size_mb: int) -> List[str]:
        """Splits DataFrame by file size"""
        max_size_bytes = max_size_mb * 1024 * 1024
        output_files = []
        
        # Calculate approximate rows per file based on memory usage
        memory_usage = df.memory_usage(deep=True).sum()
        rows_per_file = int((max_size_bytes / memory_usage) * len(df))
        
        return self._split_by_rows(df, file_path, rows_per_file) 