import time
from typing import Dict, Any, Optional
from contextlib import contextmanager
from .metrics_collector import MetricsCollector

class PerformanceMonitor:
    """Monitors tool performance and resource usage"""
    
    def __init__(self):
        self.metrics = MetricsCollector()
        self.current_operation: Optional[Dict[str, Any]] = None
    
    @contextmanager
    def monitor_operation(self, tool_name: str, operation_type: str):
        """Context manager for monitoring operation performance"""
        start_time = time.time()
        self.current_operation = {
            'tool': tool_name,
            'type': operation_type,
            'start_time': start_time
        }
        
        try:
            yield
        finally:
            end_time = time.time()
            duration = end_time - start_time
            
            if self.current_operation:
                self.current_operation.update({
                    'duration': duration,
                    'end_time': end_time
                })
                
                # Log performance metrics
                self.metrics.log_operation(tool_name, {
                    'operation_type': operation_type,
                    'duration': duration
                })
            
            self.current_operation = None
    
    def log_resource_usage(self, stats: Dict[str, Any]):
        """Logs resource usage statistics"""
        if self.current_operation:
            self.current_operation.update({
                'memory_usage': stats.get('memory', 0),
                'cpu_usage': stats.get('cpu', 0)
            }) 