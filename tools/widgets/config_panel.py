import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Callable

class ConfigPanel(ttk.LabelFrame):
    """Panel for tool configuration options"""
    
    def __init__(self, parent, title="Configuration"):
        super().__init__(parent, text=title)
        self.options = {}
        self.variables = {}
        self.frames = {}
    
    def add_choice_option(self, name: str, label: str, choices: list, callback=None):
        """Adds a dropdown selection option"""
        frame = ttk.Frame(self)
        frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(frame, text=label).pack(side=tk.LEFT)
        
        var = tk.StringVar(value=choices[0] if choices else '')
        if callback:
            var.trace_add('write', lambda *args: callback(var.get()))
        
        dropdown = ttk.Combobox(
            frame,
            textvariable=var,
            values=choices,
            state='readonly'
        )
        dropdown.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        self.options[name] = dropdown
        self.variables[name] = var
        self.frames[name] = frame
    
    def add_numeric_option(self, name: str, label: str, default=0, min_val=None, max_val=None, callback=None):
        """Adds a numeric entry option"""
        frame = ttk.Frame(self)
        frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(frame, text=label).pack(side=tk.LEFT)
        
        var = tk.IntVar(value=default)
        if callback:
            var.trace_add('write', lambda *args: callback(var.get()))
        
        vcmd = (self.register(lambda P: self._validate_number(P, min_val, max_val)), '%P')
        entry = ttk.Entry(
            frame,
            textvariable=var,
            validate='key',
            validatecommand=vcmd
        )
        entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        self.options[name] = entry
        self.variables[name] = var
        self.frames[name] = frame
    
    def add_boolean_option(self, name: str, label: str, default=False, callback=None):
        """Adds a checkbox option"""
        frame = ttk.Frame(self)
        frame.pack(fill=tk.X, padx=5, pady=2)
        
        var = tk.BooleanVar(value=default)
        if callback:
            var.trace_add('write', lambda *args: callback(var.get()))
        
        checkbox = ttk.Checkbutton(
            frame,
            text=label,
            variable=var
        )
        checkbox.pack(fill=tk.X)
        
        self.options[name] = checkbox
        self.variables[name] = var
        self.frames[name] = frame
    
    def add_text_option(self, name: str, label: str, default="", callback=None):
        """Adds a text entry option"""
        frame = ttk.Frame(self)
        frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(frame, text=label).pack(side=tk.LEFT)
        
        var = tk.StringVar(value=default)
        if callback:
            var.trace_add('write', lambda *args: callback(var.get()))
        
        entry = ttk.Entry(
            frame,
            textvariable=var
        )
        entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        self.options[name] = entry
        self.variables[name] = var
        self.frames[name] = frame
    
    def add_number_option(self, name: str, label: str, min_val: float = None, 
                         max_val: float = None, default: float = None, callback=None):
        """Adds a numeric entry option"""
        frame = ttk.Frame(self)
        frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(frame, text=label).pack(side=tk.LEFT)
        
        vcmd = (self.register(lambda P: self._validate_number(P, min_val, max_val)), '%P')
        var = tk.StringVar(value=str(default) if default is not None else '')
        
        entry = ttk.Entry(
            frame,
            textvariable=var,
            validate='key',
            validatecommand=vcmd,
            width=10
        )
        entry.pack(side=tk.LEFT, padx=(5, 0))
        
        if min_val is not None or max_val is not None:
            range_text = f"({min_val if min_val is not None else '-∞'}"
            range_text += f" to {max_val if max_val is not None else '∞'})"
            ttk.Label(frame, text=range_text).pack(side=tk.LEFT, padx=(5, 0))
        
        self.variables[name] = var
        self.frames[name] = frame
        
        if callback:
            var.trace_add('write', lambda *args: callback(var.get()))
    
    def get_config(self) -> dict:
        """Gets current configuration values"""
        return {
            name: var.get()
            for name, var in self.variables.items()
        }
    
    def update_choices(self, name: str, choices: list):
        """Updates choices for a dropdown option"""
        if name in self.options:
            self.options[name]['values'] = choices
            if choices:
                self.variables[name].set(choices[0])
    
    def hide_option(self, name: str):
        """Hides a configuration option"""
        if name in self.frames:
            self.frames[name].pack_forget()
    
    def show_option(self, name: str):
        """Shows a configuration option"""
        if name in self.frames:
            self.frames[name].pack(fill=tk.X, padx=5, pady=2)
    
    def _validate_number(self, value: str, min_val: float = None, max_val: float = None) -> bool:
        """Validates numeric input"""
        if not value:  # Allow empty value
            return True
            
        try:
            num = float(value)
            if min_val is not None and num < min_val:
                return False
            if max_val is not None and num > max_val:
                return False
            return True
        except ValueError:
            return False 
    
    def set_config(self, config: dict):
        """Restores saved configuration"""
        if not config:
            return
        
        for name, value in config.items():
            if name in self.variables:
                try:
                    self.variables[name].set(value)
                except Exception as e:
                    print(f"Error setting {name}: {str(e)}")
    
    def add_separator(self):
        """Adds a visual separator"""
        ttk.Separator(self, orient='horizontal').pack(
            fill=tk.X, padx=5, pady=5
        ) 