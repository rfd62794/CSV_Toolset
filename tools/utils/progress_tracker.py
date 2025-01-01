from typing import Optional, Callable
from dataclasses import dataclass

@dataclass
class ProgressTracker:
    """Handles progress tracking and updates"""
    
    callback: Optional[Callable[[int, str], None]] = None
    current: int = 0
    message: str = ""
    
    def update(self, percent: int, message: str = None) -> None:
        """Updates progress"""
        self.current = max(0, min(100, percent))
        if message:
            self.message = message
            
        if self.callback:
            self.callback(self.current, self.message)
    
    def step(self, amount: int = 10, message: str = None) -> None:
        """Increments progress by step amount"""
        self.update(self.current + amount, message) 