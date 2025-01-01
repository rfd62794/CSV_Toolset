from .base_processor import BaseProcessor
from ..utils.data_merger import DataMerger

class AppenderProcessor(BaseProcessor):
    def __init__(self):
        super().__init__()
        self.merger = DataMerger()
    
    def get_columns(self, file_path):
        """Gets list of columns from CSV file"""
        return self.reader.get_columns(file_path)
    
    def _process_data(self, primary_df, secondary_df, primary_key, secondary_key, columns_to_add):
        """
        Merges columns from secondary DataFrame.
        Implements abstract method from BaseProcessor.
        """
        return self.merger.merge_dataframes(
            primary_df,
            secondary_df,
            primary_key,
            secondary_key,
            columns_to_add
        )
    
    def process_file(self, primary_file, secondary_file, primary_key, secondary_key, 
                    columns_to_add, progress_callback=None):
        """Appends columns from secondary file to primary file"""
        self.set_progress_callback(progress_callback)
        
        try:
            # Read primary file
            self.update_progress(0, "Reading primary file...")
            primary_df = self.reader.read_csv(primary_file)
            
            # Read secondary file
            self.update_progress(33, "Reading secondary file...")
            secondary_df = self.reader.read_csv(secondary_file)
            
            # Process the merge
            self.update_progress(66, "Merging files...")
            result, stats = self._process_data(
                primary_df,
                secondary_df,
                primary_key,
                secondary_key,
                columns_to_add
            )
            
            if not isinstance(result, pd.DataFrame):
                return False, stats  # stats contains error message
            
            return result, stats
            
        except Exception as e:
            return False, str(e) 