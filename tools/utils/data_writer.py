class DataWriter:
    """Handles all CSV file writing operations"""
    
    @staticmethod
    def write_csv(df, output_path, **options):
        """Writes DataFrame to CSV with error handling"""
        try:
            encoding = options.pop('encoding', 'utf-8')
            df.to_csv(output_path, encoding=encoding, index=False, **options)
            return True, None
        except Exception as e:
            return False, str(e) 