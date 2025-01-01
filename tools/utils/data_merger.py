import pandas as pd

class DataMerger:
    """Handles DataFrame merging operations"""
    
    @staticmethod
    def validate_merge_keys(left_df, right_df, left_key, right_key):
        """Validates merge keys exist in both DataFrames"""
        if left_key not in left_df.columns:
            return False, f"Key column '{left_key}' not found in primary file"
        if right_key not in right_df.columns:
            return False, f"Key column '{right_key}' not found in secondary file"
        return True, None
    
    @staticmethod
    def merge_dataframes(left_df, right_df, left_key, right_key, columns_to_add, how='left'):
        """
        Merges two DataFrames on specified keys.
        
        Args:
            left_df: Primary DataFrame
            right_df: Secondary DataFrame to merge
            left_key: Key column in primary DataFrame
            right_key: Key column in secondary DataFrame
            columns_to_add: List of columns to add from secondary DataFrame
            how: Merge type (left, right, inner, outer)
            
        Returns:
            tuple: (merged_df, stats_dict)
        """
        # Validate merge keys
        valid, error = DataMerger.validate_merge_keys(left_df, right_df, left_key, right_key)
        if not valid:
            return None, error
            
        # Validate columns to add exist
        missing_cols = [col for col in columns_to_add if col not in right_df.columns]
        if missing_cols:
            return None, f"Columns not found in secondary file: {', '.join(missing_cols)}"
            
        # Perform merge
        try:
            # Select only needed columns from right DataFrame
            right_df = right_df[[right_key] + columns_to_add]
            
            # Merge DataFrames
            merged = left_df.merge(
                right_df,
                left_on=left_key,
                right_on=right_key,
                how=how
            )
            
            # Calculate statistics
            stats = {
                'rows_before': len(left_df),
                'rows_after': len(merged),
                'columns_added': len(columns_to_add),
                'matched_rows': sum(merged[right_key].notna())
            }
            
            return merged, stats
            
        except Exception as e:
            return None, f"Merge failed: {str(e)}" 