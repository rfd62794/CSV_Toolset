import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ..utils.file_manager import FileManager
from ..utils.progress_tracker import ProgressTracker

class BaseToolFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.file_manager = FileManager()
        self.progress_tracker = ProgressTracker(self.update_progress)
        self.input_file = None
        self.create_base_widgets() 