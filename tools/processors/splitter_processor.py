import pandas as pd
from pathlib import Path
from typing import Dict, List, Any
from ..base.base_processor import BaseProcessor

class SplitterProcessor(BaseProcessor):
    """Processor for splitting CSV files"""
    
    def split_by_rows(self, df: pd.DataFrame, row_count: int, 
                     keep_headers: bool = True) -> List[pd.DataFrame]:
        """Splits dataframe by row count"""
        chunks = []
        for i in range(0, len(df), row_count):
            chunk = df.iloc[i:i + row_count].copy()
            chunks.append(chunk)
        return chunks
    
    def split_by_percentage(self, df: pd.DataFrame, percentage: float,
                          keep_headers: bool = True) -> List[pd.DataFrame]:
        """Splits dataframe by percentage"""
        row_count = int(len(df) * (percentage / 100))
        return [
            df.iloc[:row_count].copy(),
            df.iloc[row_count:].copy()
        ]
    
    def split_by_column(self, df: pd.DataFrame, column: str,
                       keep_headers: bool = True) -> Dict[Any, pd.DataFrame]:
        """Splits dataframe by unique column values"""
        return {
            value: group.copy()
            for value, group in df.groupby(column)
        }
    
    def process_file(self, input_file: str, config: dict) -> Dict[str, Any]:
        """Processes the input file according to configuration"""
        df = pd.read_csv(input_file)
        output_dir = Path(input_file).parent
        pattern = config.get('output_pattern', 'split_{n}')
        keep_headers = config.get('keep_headers', True)
        
        split_type = config.get('split_type')
        result = {
            'success': True,
            'files_created': [],
            'error': None
        }
        
        try:
            if split_type == 'Row Count':
                row_count = config.get('row_count', 1000)
                chunks = self.split_by_rows(df, row_count, keep_headers)
                
                for i, chunk in enumerate(chunks, 1):
                    output_file = output_dir / f"{pattern.format(n=i)}.csv"
                    chunk.to_csv(output_file, index=False)
                    result['files_created'].append(str(output_file))
                    
            elif split_type == 'Percentage':
                percentage = config.get('percentage', 50)
                chunks = self.split_by_percentage(df, percentage, keep_headers)
                
                for i, chunk in enumerate(['first', 'second']):
                    output_file = output_dir / f"{pattern.format(n=chunk)}.csv"
                    chunks[i].to_csv(output_file, index=False)
                    result['files_created'].append(str(output_file))
                    
            elif split_type == 'Column Value':
                column = config.get('split_column')
                if not column:
                    raise ValueError("No split column specified")
                    
                chunks = self.split_by_column(df, column, keep_headers)
                
                for value, chunk in chunks.items():
                    output_file = output_dir / f"{pattern.format(n=value)}.csv"
                    chunk.to_csv(output_file, index=False)
                    result['files_created'].append(str(output_file))
            
            return result
            
        except Exception as e:
            result['success'] = False
            result['error'] = str(e)
            return result 