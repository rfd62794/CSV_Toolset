from .base_processor import BaseProcessor
import pandas as pd

class SweeperProcessor(BaseProcessor):
    def __init__(self):
        super().__init__()
    
    def get_columns(self, file_path):
        """Gets list of columns from CSV file"""
        return self.reader.get_columns(file_path)
    
    def _process_data(self, df, columns, treat_empty_as_null=True):
        """
        Removes rows with missing data in specified columns.
        Implements abstract method from BaseProcessor.
        """
        df_clean = df.copy()
        
        if treat_empty_as_null:
            # Consider empty strings as missing values
            for col in columns:
                df_clean = df_clean[df_clean[col].astype(str).str.strip() != '']
        
        # Remove rows with NaN values in selected columns
        df_clean = df_clean.dropna(subset=columns)
        
        return df_clean
    
    def process_file(self, input_file, columns, treat_empty_as_null=True, progress_callback=None):
        """Processes the file and removes rows with missing data"""
        self.set_progress_callback(progress_callback)
        
        # Validate columns exist before processing
        df = self.reader.read_csv(input_file)
        valid, error = self.validator.validate_columns_exist(df, columns)
        if not valid:
            return False, error
            
        initial_rows = len(df)
        df_clean = self._process_data(df, columns, treat_empty_as_null)
        
        stats = {
            'initial_rows': initial_rows,
            'final_rows': len(df_clean),
            'rows_removed': initial_rows - len(df_clean)
        }
        
        return df_clean, stats 
    
    def preview_clean(self, df: pd.DataFrame, config: dict) -> pd.DataFrame:
        """Creates a preview of the cleaning operations"""
        try:
            # Get a sample of the data
            preview_df = df.head(5).copy()
            
            # Apply cleaning operations
            if config.get('trim_whitespace'):
                preview_df = preview_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
                
            if config.get('remove_duplicates'):
                preview_df = preview_df.drop_duplicates()
                
            if config.get('drop_empty'):
                preview_df = preview_df.dropna(axis=1, how='all')
                
            null_handling = config.get('null_handling', 'Keep')
            if null_handling == 'Drop':
                preview_df = preview_df.dropna()
            elif null_handling == 'Fill':
                fill_value = config.get('fill_value', '')
                preview_df = preview_df.fillna(fill_value)
                
            return preview_df
            
        except Exception as e:
            raise ValueError(f"Preview error: {str(e)}") 