import tkinter as tk
from tkinter import ttk
from typing import Any, List, Tuple

class OptionsFrame(ttk.LabelFrame):
    """Reusable frame for tool options"""
    
    def __init__(self, master, title="Options"):
        super().__init__(master, text=title)
        self.options = {}
    
    def add_checkbox(self, name: str, text: str, default: bool = False) -> tk.BooleanVar:
        """Adds a checkbox option"""
        var = tk.BooleanVar(value=default)
        self.options[name] = var
        
        ttk.Checkbutton(
            self,
            text=text,
            variable=var
        ).pack(anchor=tk.W, padx=5, pady=2)
        
        return var
    
    def add_radio_group(self, name: str, options: List[Tuple[str, str]], 
                       default: str = None) -> tk.StringVar:
        """Adds a group of radio buttons"""
        var = tk.StringVar(value=default or options[0][1])
        self.options[name] = var
        
        for text, value in options:
            ttk.Radiobutton(
                self,
                text=text,
                value=value,
                variable=var
            ).pack(anchor=tk.W, padx=20, pady=2)
        
        return var
    
    def get_option(self, name: str) -> Any:
        """Gets current value of an option"""
        return self.options[name].get() 