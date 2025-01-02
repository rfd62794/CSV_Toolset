from typing import Dict, Any, List, Union
import pandas as pd
import re
from pathlib import Path
from ..base.base_processor import BaseProcessor

class TransformerProcessor(BaseProcessor):
    """Processor for transforming CSV data"""
    
    def transform_text(self, value: str, config: dict) -> str:
        """Applies text transformations"""
        if pd.isna(value):
            return value
            
        result = str(value)
        
        # Apply selected transformations
        if config.get('transform_uppercase'):
            result = result.upper()
            
        if config.get('transform_lowercase'):
            result = result.lower()
            
        if config.get('transform_title_case'):
            result = result.title()
            
        if config.get('transform_strip_whitespace'):
            result = result.strip()
            
        if config.get('transform_remove_special_characters'):
            result = re.sub(r'[^a-zA-Z0-9\s]', '', result)
            
        if config.get('transform_format_numbers'):
            try:
                num = float(result)
                result = f"{num:,.2f}"
            except ValueError:
                pass
                
        if config.get('transform_custom_regex'):
            pattern = config.get('custom_regex', '')
            if pattern:
                try:
                    result = re.sub(pattern, '', result)
                except re.error:
                    pass
                    
        return result
    
    def transform_sample(self, series: pd.Series, config: dict) -> pd.Series:
        """Transforms a sample of data for preview"""
        return series.apply(lambda x: self.transform_text(x, config))
    
    def process_file(self, input_file: str, config: dict) -> Dict[str, Any]:
        """Processes the input file according to configuration"""
        try:
            df = pd.read_csv(input_file)
            column = config.get('column')
            
            if not column:
                raise ValueError("No column selected for transformation")
                
            if column not in df.columns:
                raise ValueError(f"Column '{column}' not found in file")
                
            # Transform the selected column
            df[f"{column}_transformed"] = df[column].apply(
                lambda x: self.transform_text(x, config)
            )
            
            # Save transformed file
            output_file = str(Path(input_file).with_stem(f"{Path(input_file).stem}_transformed"))
            df.to_csv(output_file, index=False)
            
            return {
                'success': True,
                'output_file': output_file,
                'rows_processed': len(df),
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'output_file': None,
                'rows_processed': 0,
                'error': str(e)
            } 