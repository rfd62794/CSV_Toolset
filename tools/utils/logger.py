import logging
from pathlib import Path
from datetime import datetime
from .config import ToolConfig

class Logger:
    """Handles application logging"""
    
    def __init__(self):
        self.config = ToolConfig()
        self._setup_logging()
    
    def _setup_logging(self):
        """Sets up logging configuration"""
        log_dir = Path.home() / 'CSVToolkit' / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"csvtoolkit_{datetime.now():%Y%m%d}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
    
    @staticmethod
    def log_operation(operation: str, details: dict):
        """Logs operation details"""
        logging.info(f"Operation: {operation}")
        for key, value in details.items():
            logging.info(f"  {key}: {value}") 