import re
import pandas as pd

class PhoneProcessor:
    @staticmethod
    def format_number(value, format_style="standard", strict=True):
        """
        Formats a phone number according to specified style.
        
        Args:
            value: The input value to format
            format_style: "standard" (XXX-XXX-XXXX), "plain" (XXXXXXXXXX), 
                         or "parentheses" ((XXX) XXX-XXXX)
            strict: If True, only accept 10-digit numbers
        """
        # Remove all non-numeric characters
        numbers = re.sub(r'\D', '', str(value))
        
        # In strict mode, only accept 10-digit numbers
        if strict and len(numbers) != 10:
            return None
            
        # If not strict, try to extract last 10 digits
        if len(numbers) > 10:
            numbers = numbers[-10:]
        elif len(numbers) < 10:
            return None
            
        # Format according to selected style
        if format_style == "plain":
            return numbers
        elif format_style == "standard":
            return f"{numbers[:3]}-{numbers[3:6]}-{numbers[6:]}"
        else:  # parentheses
            return f"({numbers[:3]}) {numbers[3:6]}-{numbers[6:]}"
    
    @classmethod
    def process_column(cls, df, column, format_style="standard", strict=True):
        """
        Processes phone numbers in a column.
        
        Args:
            df: Input DataFrame
            column: Column name containing phone numbers
            format_style: Desired format style
            strict: Whether to use strict validation
            
        Returns:
            DataFrame with original and formatted columns
        """
        # Create output dataframe
        output_df = pd.DataFrame({
            'Original': df[column],
            'Formatted_Phone': df[column].apply(
                lambda x: cls.format_number(x, format_style, strict)
            )
        })
        
        return output_df
    
    @classmethod
    def preview_data(cls, df, column, format_style="standard", strict=True, nrows=5):
        """Generates a preview of phone number formatting"""
        preview_data = []
        for value in df[column].head(nrows):
            formatted = cls.format_number(value, format_style, strict)
            preview_data.append({
                'Original': value,
                'Formatted': formatted if formatted else 'No valid phone number found'
            })
        return preview_data 