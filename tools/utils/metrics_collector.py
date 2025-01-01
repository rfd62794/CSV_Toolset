from datetime import datetime
import json
from pathlib import Path
from typing import Dict, Any
from .logger import Logger

class MetricsCollector:
    """Collects usage metrics for tools"""
    
    def __init__(self):
        self.logger = Logger()
        self.metrics_file = Path.home() / 'CSVToolkit' / 'metrics.json'
        self.metrics: Dict[str, Any] = self._load_metrics()
    
    def _load_metrics(self) -> Dict[str, Any]:
        """Loads existing metrics"""
        if self.metrics_file.exists():
            try:
                return json.loads(self.metrics_file.read_text())
            except Exception:
                return self._get_default_metrics()
        return self._get_default_metrics()
    
    def _get_default_metrics(self) -> Dict[str, Any]:
        """Returns default metrics structure"""
        return {
            'total_operations': 0,
            'tool_usage': {},
            'file_stats': {
                'total_files': 0,
                'total_rows': 0,
                'avg_file_size': 0
            },
            'errors': {
                'total': 0,
                'by_type': {}
            }
        }
    
    def log_operation(self, tool_name: str, details: Dict[str, Any]):
        """Logs tool operation"""
        timestamp = datetime.now().isoformat()
        
        # Update tool usage
        if tool_name not in self.metrics['tool_usage']:
            self.metrics['tool_usage'][tool_name] = {
                'uses': 0,
                'last_used': None,
                'avg_processing_time': 0
            }
            
        tool_stats = self.metrics['tool_usage'][tool_name]
        tool_stats['uses'] += 1
        tool_stats['last_used'] = timestamp
        
        # Update file stats
        if 'rows_processed' in details:
            self.metrics['file_stats']['total_rows'] += details['rows_processed']
        
        self.metrics['total_operations'] += 1
        self._save_metrics()
        
        # Log operation details
        self.logger.log_operation(tool_name, details)
    
    def log_error(self, error_type: str, details: Dict[str, Any]):
        """Logs error occurrence"""
        self.metrics['errors']['total'] += 1
        
        if error_type not in self.metrics['errors']['by_type']:
            self.metrics['errors']['by_type'][error_type] = 0
        self.metrics['errors']['by_type'][error_type] += 1
        
        self._save_metrics()
    
    def _save_metrics(self):
        """Saves metrics to file"""
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
        self.metrics_file.write_text(json.dumps(self.metrics, indent=2))
    
    def get_tool_stats(self, tool_name: str) -> Dict[str, Any]:
        """Gets usage statistics for tool"""
        return self.metrics['tool_usage'].get(tool_name, {
            'uses': 0,
            'last_used': None,
            'avg_processing_time': 0
        }) 