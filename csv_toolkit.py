import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from functools import partial

class CSVToolkit(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("CSV Toolkit")
        self.geometry("800x600")
        
        # Create main container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create sidebar for tool selection
        self.sidebar = ttk.Frame(self.main_container, width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Create main content area
        self.content = ttk.Frame(self.main_container)
        self.content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Tool registry - maps tool names to their functions
        self.tools = {
            "CSV Inspector": self.show_inspector,
            "Column Sweeper": self.show_column_sweeper,
            "Order Reverser": self.show_order_reverser,
            "Sample Maker": self.show_sample_maker,
            "Phone Extractor": self.show_phone_extractor,
            "Column Appender": self.show_column_appender,
            "Data Reformatter": self.show_reformatter
        }
        
        self.create_sidebar()
        self.create_welcome_screen()
        
    def create_sidebar(self):
        # Create tool selection buttons
        ttk.Label(self.sidebar, text="Available Tools", font=('Helvetica', 12, 'bold')).pack(pady=(0, 10))
        
        for tool_name in self.tools.keys():
            btn = ttk.Button(
                self.sidebar,
                text=tool_name,
                command=partial(self.tools[tool_name])
            )
            btn.pack(fill=tk.X, pady=2)
    
    def create_welcome_screen(self):
        welcome = ttk.Frame(self.content)
        welcome.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(
            welcome,
            text="Welcome to CSV Toolkit",
            font=('Helvetica', 16, 'bold')
        ).pack(pady=20)
        
        ttk.Label(
            welcome,
            text="Select a tool from the sidebar to begin.",
            font=('Helvetica', 12)
        ).pack()
    
    def clear_content(self):
        """Clear all widgets from the content frame"""
        for widget in self.content.winfo_children():
            widget.destroy()
    
    # Tool display methods
    def show_inspector(self):
        self.clear_content()
        from tools.inspector_frame import InspectorFrame
        inspector = InspectorFrame(self.content)
        inspector.pack(fill=tk.BOTH, expand=True)
    
    def show_column_sweeper(self):
        self.clear_content()
        from tools.column_sweeper_frame import ColumnSweeperFrame
        sweeper = ColumnSweeperFrame(self.content)
        sweeper.pack(fill=tk.BOTH, expand=True)
    
    # ... Additional tool methods ...

if __name__ == "__main__":
    app = CSVToolkit()
    app.mainloop() 