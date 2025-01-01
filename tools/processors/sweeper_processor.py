from .base_processor import BaseProcessor

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