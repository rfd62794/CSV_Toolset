import pandas as pd

class OrderProcessor:
    @classmethod
    def reverse_order(cls, df, preserve_header=True):
        """
        Reverses the order of rows in a DataFrame.
        
        Args:
            df: Input DataFrame
            preserve_header: If True, keep header row at top
            
        Returns:
            DataFrame with reversed rows
        """
        if preserve_header:
            # Preserve header by excluding it from the reversal
            return pd.concat([
                df.iloc[:1],  # Keep header row
                df.iloc[1:].iloc[::-1]  # Reverse all other rows
            ])
        else:
            # Reverse all rows including header
            return df.iloc[::-1]
    
    @classmethod
    def preview_data(cls, file_path, preserve_header=True, nrows=5):
        """
        Generates a preview of the reversal.
        
        Returns:
            tuple: (first_rows, last_rows) - DataFrames containing preview rows
        """
        df = pd.read_csv(file_path)
        
        # Get original first and last rows
        first_rows = df.head(nrows)
        last_rows = df.tail(nrows)
        
        # Get reversed first and last rows
        df_reversed = cls.reverse_order(df, preserve_header)
        reversed_first = df_reversed.head(nrows)
        reversed_last = df_reversed.tail(nrows)
        
        return {
            'original': {
                'first': first_rows,
                'last': last_rows
            },
            'reversed': {
                'first': reversed_first,
                'last': reversed_last
            }
        } 