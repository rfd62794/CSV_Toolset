from typing import List, Tuple, Dict, Any
import pandas as pd
from ..base.base_processor import BaseProcessor

class MergerProcessor(BaseProcessor):
    """Processor for merging CSV files"""
    
    def __init__(self):
        super().__init__()
        self.reader = self.get_reader()
        self.writer = self.get_writer()
    
    def merge_files(self, files: List[str], merge_type: str, **options) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Merges multiple CSV files"""
        if not files:
            raise ValueError("No files provided for merging")
            
        try:
            if merge_type == "append":
                return self._append_files(files, **options)
            elif merge_type == "join":
                return self._join_files(files, **options)
            else:
                raise ValueError(f"Invalid merge type: {merge_type}")
                
        except Exception as e:
            raise RuntimeError(f"Error merging files: {str(e)}")
    
    def _append_files(self, files: List[str], **options) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Vertically stacks files"""
        dfs = []
        total_rows = 0
        
        for file in files:
            if self.progress:
                self.update_progress(
                    (len(dfs) / len(files)) * 100,
                    f"Reading {file}..."
                )
            
            df = self.reader.read_csv(file)
            total_rows += len(df)
            dfs.append(df)
        
        if self.progress:
            self.update_progress(90, "Merging files...")
            
        result = pd.concat(dfs, ignore_index=True)
        
        stats = {
            'input_files': len(files),
            'total_input_rows': total_rows,
            'output_rows': len(result),
            'merge_type': 'append'
        }
        
        return result, stats
    
    def _join_files(self, files: List[str], join_key: str, how: str = 'inner', **options) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Joins files on a key column"""
        if not join_key:
            raise ValueError("Join key must be specified")
            
        dfs = []
        total_rows = 0
        
        for file in files:
            if self.progress:
                self.update_progress(
                    (len(dfs) / len(files)) * 100,
                    f"Reading {file}..."
                )
            
            df = self.reader.read_csv(file)
            if join_key not in df.columns:
                raise ValueError(f"Join key '{join_key}' not found in {file}")
                
            total_rows += len(df)
            dfs.append(df)
        
        if self.progress:
            self.update_progress(90, "Joining files...")
            
        result = dfs[0]
        for df in dfs[1:]:
            result = result.merge(df, on=join_key, how=how)
        
        stats = {
            'input_files': len(files),
            'total_input_rows': total_rows,
            'output_rows': len(result),
            'merge_type': 'join',
            'join_key': join_key,
            'join_type': how
        }
        
        return result, stats 