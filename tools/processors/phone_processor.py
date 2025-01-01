import re
import pandas as pd
from .base_processor import BaseProcessor
from ..utils.pattern_processor import PatternProcessor

class PhoneProcessor(BaseProcessor):
    # Common phone patterns
    PATTERNS = {
        'us': r'\b(?:\+?1[-.]?)?\s*\(?([0-9]{3})\)?[-.\s]*([0-9]{3})[-.\s]*([0-9]{4})\b',
        'international': r'\+?[0-9]{1,4}[-.\s]*\(?[0-9]{1,4}\)?[-.\s0-9]{6,}'
    }
    
    def __init__(self):
        super().__init__()
        self.pattern_processor = PatternProcessor()
        
    def _compile_pattern(self, pattern_type='us'):
        """Gets the appropriate regex pattern"""
        pattern = self.PATTERNS.get(pattern_type, self.PATTERNS['us'])
        return self.pattern_processor.compile_pattern(pattern, re.IGNORECASE)
    
    def _format_number(self, match, format_type='(XXX) XXX-XXXX'):
        """Formats a phone number match"""
        if not match or len(match.groups()) != 3:
            return match.group(0) if match else ''
            
        area, prefix, number = match.groups()
        formatted = format_type
        formatted = formatted.replace('XXX', area, 1)
        formatted = formatted.replace('XXX', prefix, 1)
        formatted = formatted.replace('XXXX', number)
        return formatted
    
    def _process_data(self, df, source_column, pattern_type='us', format_type='(XXX) XXX-XXXX'):
        """
        Extracts phone numbers from text.
        Implements abstract method from BaseProcessor.
        """
        # Validate source column exists
        valid, error = self.validator.validate_columns_exist(df, [source_column])
        if not valid:
            raise ValueError(error)
        
        # Compile regex pattern
        pattern = self._compile_pattern(pattern_type)
        
        # Extract and format phone numbers
        phone_numbers = []
        for text in df[source_column]:
            if pd.isna(text):
                phone_numbers.append('')
                continue
                
            matches = list(pattern.finditer(str(text)))
            if matches:
                formatted = self._format_number(matches[0], format_type)
                phone_numbers.append(formatted)
            else:
                phone_numbers.append('')
        
        # Create result DataFrame
        result = df.copy()
        result['extracted_phone'] = phone_numbers
        
        return result
    
    def process_file(self, input_file, source_column, pattern_type='us', format_type='(XXX) XXX-XXXX', progress_callback=None):
        """Extracts phone numbers from CSV file"""
        self.set_progress_callback(progress_callback)
        
        try:
            # Read and process data
            df = self.reader.read_csv(input_file)
            result = self._process_data(df, source_column, pattern_type, format_type)
            
            # Calculate statistics
            total_found = sum(result['extracted_phone'].astype(bool))
            stats = {
                'total_rows': len(result),
                'numbers_found': total_found,
                'success_rate': f"{(total_found / len(result) * 100):.1f}%"
            }
            
            return result, stats
            
        except Exception as e:
            return False, str(e) 