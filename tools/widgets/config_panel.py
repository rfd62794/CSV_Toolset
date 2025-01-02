import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Callable

class ConfigPanel(ttk.LabelFrame):
    """Reusable configuration panel widget"""
    
    def __init__(self, parent, title="Configuration", **kwargs):
        super().__init__(parent, text=title, **kwargs)
        self.config_vars = {}
        self.callbacks = {}
        
    def add_text_option(self, key: str, label: str, default: str = "", 
                       callback: Callable = None) -> tk.StringVar:
        """Adds a text configuration option"""
        frame = ttk.Frame(self)
        frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(frame, text=label).pack(side=tk.LEFT)
        var = tk.StringVar(value=default)
        
        if callback:
            var.trace_add('write', lambda *args: callback(var.get()))
            self.callbacks[key] = callback
            
        self.config_vars[key] = var
        ttk.Entry(frame, textvariable=var).pack(side=tk.RIGHT, expand=True, fill=tk.X)
        return var
        
    def add_boolean_option(self, key: str, label: str, default: bool = False,
                          callback: Callable = None) -> tk.BooleanVar:
        """Adds a boolean configuration option"""
        var = tk.BooleanVar(value=default)
        
        if callback:
            var.trace_add('write', lambda *args: callback(var.get()))
            self.callbacks[key] = callback
            
        self.config_vars[key] = var
        ttk.Checkbutton(
            self, text=label, variable=var
        ).pack(anchor=tk.W, padx=5, pady=2)
        return var
        
    def add_choice_option(self, key: str, label: str, choices: list, 
                         default: str = None, callback: Callable = None) -> tk.StringVar:
        """Adds a choice configuration option"""
        frame = ttk.Frame(self)
        frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(frame, text=label).pack(side=tk.LEFT)
        var = tk.StringVar(value=default or choices[0])
        
        if callback:
            var.trace_add('write', lambda *args: callback(var.get()))
            self.callbacks[key] = callback
            
        self.config_vars[key] = var
        ttk.OptionMenu(frame, var, var.get(), *choices).pack(side=tk.RIGHT)
        return var
        
    def add_numeric_option(self, key: str, label: str, default: float = 0,
                          min_val: float = None, max_val: float = None,
                          callback: Callable = None) -> tk.DoubleVar:
        """Adds a numeric configuration option"""
        frame = ttk.Frame(self)
        frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(frame, text=label).pack(side=tk.LEFT)
        var = tk.DoubleVar(value=default)
        
        if callback:
            var.trace_add('write', lambda *args: callback(var.get()))
            self.callbacks[key] = callback
            
        self.config_vars[key] = var
        spinbox = ttk.Spinbox(
            frame, 
            from_=min_val if min_val is not None else float('-inf'),
            to=max_val if max_val is not None else float('inf'),
            textvariable=var
        )
        spinbox.pack(side=tk.RIGHT)
        return var
    
    def get_config(self) -> Dict[str, Any]:
        """Gets current configuration values"""
        return {
            key: var.get()
            for key, var in self.config_vars.items()
        }
    
    def set_config(self, config: Dict[str, Any]):
        """Sets configuration values"""
        for key, value in config.items():
            if key in self.config_vars:
                self.config_vars[key].set(value)
                if key in self.callbacks:
                    self.callbacks[key](value)
    
    def add_separator(self):
        """Adds a separator line"""
        ttk.Separator(self, orient='horizontal').pack(
            fill=tk.X, padx=5, pady=5
        ) 