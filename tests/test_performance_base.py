import pytest
import time
import psutil
import threading
from typing import Callable, Any
from .config import TestConfig

class BasePerformanceTest:
    """Base class for performance testing"""
    
    config = TestConfig()
    
    def measure_execution_time(self, func: Callable, *args, **kwargs) -> float:
        """Measures execution time of a function"""
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        return end_time - start_time, result
    
    def measure_memory_usage(self, func: Callable, *args, **kwargs) -> int:
        """Measures peak memory usage of a function"""
        process = psutil.Process()
        initial_memory = process.memory_info().rss
        peak_memory = initial_memory
        stop_monitoring = False
        
        def monitor_memory():
            nonlocal peak_memory
            while not stop_monitoring:
                current_memory = process.memory_info().rss
                peak_memory = max(peak_memory, current_memory)
                time.sleep(self.config.PERFORMANCE_SETTINGS['memory_check_interval'])
        
        # Start memory monitoring in separate thread
        monitor_thread = threading.Thread(target=monitor_memory)
        monitor_thread.start()
        
        try:
            result = func(*args, **kwargs)
        finally:
            stop_monitoring = True
            monitor_thread.join()
        
        memory_used = peak_memory - initial_memory
        return memory_used, result
    
    def benchmark_operation(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """Runs complete benchmark of an operation"""
        rounds = self.config.PERFORMANCE_SETTINGS['benchmark_rounds']
        times = []
        memory_usage = []
        cpu_usage = []
        
        for _ in range(rounds):
            # Measure execution time
            execution_time, _ = self.measure_execution_time(func, *args, **kwargs)
            times.append(execution_time)
            
            # Measure memory usage
            mem_used, _ = self.measure_memory_usage(func, *args, **kwargs)
            memory_usage.append(mem_used)
            
            # Measure CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_usage.append(cpu_percent)
        
        return {
            'avg_time': sum(times) / rounds,
            'max_time': max(times),
            'min_time': min(times),
            'avg_memory': sum(memory_usage) / rounds,
            'peak_memory': max(memory_usage),
            'avg_cpu': sum(cpu_usage) / rounds,
            'max_cpu': max(cpu_usage)
        }
    
    def verify_performance_metrics(self, metrics: Dict[str, Any]):
        """Verifies performance metrics against thresholds"""
        thresholds = self.config.PERFORMANCE_SETTINGS['performance_thresholds']
        
        assert metrics['avg_time'] <= thresholds['load_time'], \
            f"Average execution time ({metrics['avg_time']:.2f}s) exceeds threshold ({thresholds['load_time']}s)"
        
        assert metrics['peak_memory'] <= thresholds['memory_usage'], \
            f"Peak memory usage ({metrics['peak_memory']/1024/1024:.1f}MB) exceeds threshold ({thresholds['memory_usage']/1024/1024:.1f}MB)"
        
        assert metrics['max_cpu'] <= thresholds['cpu_usage'], \
            f"Maximum CPU usage ({metrics['max_cpu']:.1f}%) exceeds threshold ({thresholds['cpu_usage']}%)" 