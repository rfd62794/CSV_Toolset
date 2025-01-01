import pandas as pd

class SweeperProcessor:
    @classmethod
    def get_columns(cls, file_path):
        """
        Gets list of columns from CSV file.
        
        Returns:
            list: Column names
        """
        df = pd.read_csv(file_path, nrows=0)  # Read only header
        return list(df.columns)
    
    @classmethod
    def remove_empty_rows(cls, df, columns, treat_empty_as_null=True):
        """
        Removes rows with missing data in specified columns.
        
        Args:
            df: Input DataFrame
            columns: List of columns to check
            treat_empty_as_null: If True, treat empty strings as missing values
            
        Returns:
            DataFrame with rows removed
        """
        df_clean = df.copy()
        
        if treat_empty_as_null:
            # Consider empty strings as missing values
            for col in columns:
                df_clean = df_clean[df_clean[col].astype(str).str.strip() != '']
        
        # Remove rows with NaN values in selected columns
        df_clean = df_clean.dropna(subset=columns)
        
        return df_clean
    
    @classmethod
    def process_file(cls, file_path, columns, treat_empty_as_null=True, progress_callback=None):
        """
        Processes the file and removes rows with missing data.
        
        Args:
            file_path: Path to CSV file
            columns: List of columns to check
            treat_empty_as_null: If True, treat empty strings as missing values
            progress_callback: Optional callback for progress updates
            
        Returns:
            tuple: (processed_df, stats_dict)
        """
        if progress_callback:
            progress_callback(0, "Reading file...")
            
        df = pd.read_csv(file_path)
        initial_rows = len(df)
        
        if progress_callback:
            progress_callback(33, "Removing empty rows...")
            
        df_clean = cls.remove_empty_rows(df, columns, treat_empty_as_null)
        
        if progress_callback:
            progress_callback(66, "Calculating statistics...")
            
        stats = {
            'initial_rows': initial_rows,
            'final_rows': len(df_clean),
            'rows_removed': initial_rows - len(df_clean)
        }
        
        return df_clean, stats 