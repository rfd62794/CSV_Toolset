class ProgressTracker:
    def __init__(self, callback=None):
        self.callback = callback
        
    def update(self, progress, message=None):
        """Updates progress with optional message"""
        if self.callback:
            self.callback(progress, message) 