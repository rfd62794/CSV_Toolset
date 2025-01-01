import pandas as pd
import chardet

class DataReformatter:
    @staticmethod
    def detect_encoding(file_path):
        """Detects the encoding of a file"""
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            return result['encoding']
    
    @staticmethod
    def clean_text(text, options):
        """Cleans text based on provided options"""
        if not text:
            return text
            
        result = str(text)
        
        if options.get('remove_null'):
            result = result.replace('\x00', '')
            
        if options.get('remove_nonprint'):
            result = ''.join(c for c in result if c.isprintable())
            
        if options.get('convert_ascii'):
            result = result.encode('ascii', errors='ignore').decode('ascii')
            
        return result
    
    @classmethod
    def process_file(cls, file_path, options, encoding=None, progress_callback=None):
        """Processes the file and returns cleaned data"""
        if not encoding:
            encoding = cls.detect_encoding(file_path)
            
        df = pd.read_csv(file_path, encoding=encoding)
        total_cells = df.size
        processed_cells = 0
        
        # Clean each cell in the dataframe
        for col in df.columns:
            df[col] = df[col].apply(lambda x: cls.clean_text(x, options))
            processed_cells += len(df)
            
            if progress_callback:
                progress = (processed_cells / total_cells) * 100
                progress_callback(progress, f"Cleaning column: {col}")
                
        return df
    
    @classmethod
    def preview_data(cls, file_path, options, encoding=None, nrows=5):
        """Generates a preview of the cleaning process"""
        if not encoding:
            encoding = cls.detect_encoding(file_path)
            
        df = pd.read_csv(file_path, nrows=nrows, encoding=encoding)
        original = df.to_string()
        cleaned = cls.clean_text(original, options)
        
        return original, cleaned 