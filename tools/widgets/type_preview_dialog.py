import tkinter as tk
from tkinter import ttk
from typing import Dict, Callable
import pandas as pd

class TypePreviewDialog(tk.Toplevel):
    """Dialog for previewing and selecting column types"""
    
    def __init__(self, parent, df: pd.DataFrame, detected_types: Dict[str, str]):
        super().__init__(parent)
        self.title("Column Type Preview")
        self.df = df
        self.detected_types = detected_types
        self.selected_types = detected_types.copy()
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
        
        # Center dialog
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')

    # ... (rest of the code remains the same) 