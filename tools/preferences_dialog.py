import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

class ToolPreferencesDialog(tk.Toplevel):
    def __init__(self, parent, categories, current_preferences=None):
        super().__init__(parent)
        self.title("Tool Preferences")
        self.categories = categories
        self.preferences = current_preferences or self._load_defaults()
        self.result = None
        self.tool_vars = {}
        
        self._create_widgets()
        self._center_window()
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Search frame
        search_frame = ttk.Frame(main_frame)
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        ttk.Label(search_frame, text="🔍").grid(row=0, column=0, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._filter_tools)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=1, sticky="ew")
        search_frame.columnconfigure(1, weight=1)
        
        # Select All/None frame
        select_frame = ttk.Frame(main_frame)
        select_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        ttk.Button(select_frame, text="Select All", command=self._select_all).grid(row=0, column=0, padx=5)
        ttk.Button(select_frame, text="Select None", command=self._select_none).grid(row=0, column=1, padx=5)
        
        # Tools frame with scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        tools_frame = ttk.Frame(canvas)
        
        tools_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=tools_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=2, column=0, sticky="nsew")
        scrollbar.grid(row=2, column=1, sticky="ns")
        
        # Create tool checkboxes by category
        row = 0
        for category, info in self.categories.items():
            ttk.Label(tools_frame, text=f"{info['icon']} {category}", font=("", 10, "bold")).grid(
                row=row, column=0, sticky="w", pady=(10, 5))
            ttk.Label(tools_frame, text=info["desc"], font=("", 8)).grid(
                row=row+1, column=0, sticky="w", padx=(20, 0))
            row += 2
            
            for tool_name, tool_desc in info["tools"].items():
                var = tk.BooleanVar(value=self.preferences.get(tool_name, True))
                self.tool_vars[tool_name] = var
                cb = ttk.Checkbutton(tools_frame, text=tool_name, variable=var)
                cb.grid(row=row, column=0, sticky="w", padx=(20, 0))
                
                desc_label = ttk.Label(tools_frame, text=tool_desc, font=("", 8))
                desc_label.grid(row=row+1, column=0, sticky="w", padx=(40, 0))
                row += 2
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        ttk.Button(button_frame, text="Save", command=self._save).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._cancel).grid(row=0, column=1, padx=5)
        
        # Configure grid weights
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
    def _center_window(self):
        self.update_idletasks()
        width = min(600, self.winfo_screenwidth() - 100)
        height = min(800, self.winfo_screenheight() - 100)
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
    def _filter_tools(self, *args):
        search_text = self.search_var.get().lower()
        for category, info in self.categories.items():
            for tool_name in info["tools"]:
                if search_text in tool_name.lower():
                    self.tool_vars[tool_name].trace_vdelete("w", self.tool_vars[tool_name].trace_id)
                else:
                    if not hasattr(self.tool_vars[tool_name], "trace_id"):
                        self.tool_vars[tool_name].trace_id = self.tool_vars[tool_name].trace("w", lambda *args: None)
    
    def _select_all(self):
        for var in self.tool_vars.values():
            var.set(True)
            
    def _select_none(self):
        for var in self.tool_vars.values():
            var.set(False)
            
    def _save(self):
        self.preferences = {name: var.get() for name, var in self.tool_vars.items()}
        try:
            self.save_preferences(self.preferences)
            self.result = self.preferences
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save preferences: {str(e)}")
            
    def _cancel(self):
        self.destroy()
        
    def _load_defaults(self):
        return {tool_name: True 
                for category in self.categories.values() 
                for tool_name in category["tools"]}
    
    @staticmethod
    def get_preferences_path():
        return Path.home() / ".csv_toolkit" / "preferences.json"
        
    @classmethod
    def load_preferences(cls):
        try:
            path = cls.get_preferences_path()
            if not path.exists():
                return None
            with open(path) as f:
                return json.load(f)
        except Exception:
            return None
            
    @classmethod
    def save_preferences(cls, preferences):
        path = cls.get_preferences_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(preferences, f, indent=2) 