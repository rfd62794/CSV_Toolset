import pandas as pd

class ColumnAppenderProcessor:
    @staticmethod
    def validate_column_name(df, column_name):
        """
        Validates if a column name can be added to the dataframe.
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not column_name:
            return False, "Column name cannot be empty"
            
        if column_name in df.columns:
            return False, f"Column '{column_name}' already exists"
            
        return True, None
    
    @classmethod
    def add_column(cls, df, column_name, default_value="", position="end"):
        """
        Adds a new column to the dataframe.
        
        Args:
            df: Input DataFrame
            column_name: Name of the new column
            default_value: Default value for the new column
            position: "start" or "end"
            
        Returns:
            DataFrame with new column added
        """
        df_copy = df.copy()
        
        if position == "start":
            # Insert at start
            df_copy.insert(0, column_name, default_value)
        else:
            # Add at end
            df_copy[column_name] = default_value
            
        return df_copy
    
    @classmethod
    def preview_data(cls, df, column_name, default_value="", position="end", nrows=5):
        """
        Generates a preview of the data with new column.
        
        Returns:
            DataFrame with preview rows
        """
        preview_df = df.head(nrows).copy()
        return cls.add_column(preview_df, column_name, default_value, position) 