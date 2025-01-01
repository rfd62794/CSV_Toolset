import pandas as pd

class DataValidator:
    """Common data validation functions"""
    
    @staticmethod
    def validate_columns_exist(df, required_columns):
        """Validates that required columns exist in DataFrame"""
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            return False, f"Missing columns: {', '.join(missing)}"
        return True, None
    
    @staticmethod
    def validate_data_types(df, column_types):
        """Validates column data types"""
        invalid = []
        for col, expected_type in column_types.items():
            if col in df and not pd.api.types.is_dtype_equal(df[col].dtype, expected_type):
                invalid.append(f"{col} (expected {expected_type}, got {df[col].dtype})")
        
        if invalid:
            return False, f"Invalid column types: {', '.join(invalid)}"
        return True, None
    
    @staticmethod
    def validate_sample_size(total_rows, sample_size):
        """Validates sample size"""
        try:
            sample_size = int(sample_size)
            if sample_size < 1:
                return False, "Sample size must be at least 1"
            if sample_size > total_rows:
                return False, f"Sample size ({sample_size:,}) is larger than total rows ({total_rows:,})"
            return True, None
        except ValueError:
            return False, "Sample size must be a valid number" 