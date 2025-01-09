import tkinter as tk
from tkinter import ttk
import json
from pathlib import Path

class ToolPreferencesDialog:
    def __init__(self, parent, categories, current_preferences=None):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Tool Preferences")
        self.dialog.geometry("600x500")
        self.dialog.resizable(True, True)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.categories = categories
        self.tool_vars = {}
        self.result = None
        
        # Create main container
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add header
        header = ttk.Label(
            main_frame,
            text="Select the tools you want to show in the main menu",
            font=('Helvetica', 10, 'bold'),
            wraplength=500,
            justify=tk.LEFT
        )
        header.pack(fill=tk.X, pady=(0, 20))
        
        # Create scrollable frame for categories
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add category sections
        for category, info in self.categories.items():
            # Create category frame
            category_frame = ttk.LabelFrame(
                scrollable_frame,
                text=f"{info['icon']} {category}",
                padding=10
            )
            category_frame.pack(fill=tk.X, pady=(0, 10))
            
            # Add category description
            desc_label = ttk.Label(
                category_frame,
                text=info['desc'],
                wraplength=500,
                justify=tk.LEFT,
                font=('Helvetica', 9, 'italic')
            )
            desc_label.pack(fill=tk.X, pady=(0, 10))
            
            # Add tool checkboxes
            for tool_name, description in info['tools'].items():
                tool_frame = ttk.Frame(category_frame)
                tool_frame.pack(fill=tk.X)
                
                var = tk.BooleanVar(value=True if not current_preferences 
                                  else current_preferences.get(tool_name, True))
                self.tool_vars[tool_name] = var
                
                cb = ttk.Checkbutton(
                    tool_frame,
                    text=tool_name,
                    variable=var
                )
                cb.pack(side=tk.LEFT)
                
                desc_label = ttk.Label(
                    tool_frame,
                    text=f"- {description}",
                    wraplength=400,
                    justify=tk.LEFT,
                    font=('Helvetica', 8)
                )
                desc_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Add select all/none buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            button_frame,
            text="Select All",
            command=self.select_all
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Select None",
            command=self.select_none
        ).pack(side=tk.LEFT)
        
        # Add action buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(
            action_frame,
            text="Save",
            command=self.save
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            action_frame,
            text="Cancel",
            command=self.cancel
        ).pack(side=tk.RIGHT)
        
        # Pack scrollable components
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Center dialog
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'+{x}+{y}')
    
    def select_all(self):
        """Select all tools"""
        for var in self.tool_vars.values():
            var.set(True)
    
    def select_none(self):
        """Deselect all tools"""
        for var in self.tool_vars.values():
            var.set(False)
    
    def save(self):
        """Save preferences and close dialog"""
        self.result = {
            tool: var.get()
            for tool, var in self.tool_vars.items()
        }
        self.dialog.destroy()
    
    def cancel(self):
        """Cancel without saving"""
        self.dialog.destroy()
    
    @staticmethod
    def load_preferences():
        """Load saved preferences"""
        prefs_file = Path.home() / '.csv_toolkit' / 'preferences.json'
        if prefs_file.exists():
            with open(prefs_file) as f:
                return json.load(f)
        return None
    
    @staticmethod
    def save_preferences(preferences):
        """Save preferences to file"""
        prefs_dir = Path.home() / '.csv_toolkit'
        prefs_dir.mkdir(parents=True, exist_ok=True)
        
        prefs_file = prefs_dir / 'preferences.json'
        with open(prefs_file, 'w') as f:
            json.dump(preferences, f, indent=2) 