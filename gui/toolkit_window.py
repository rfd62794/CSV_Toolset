import tkinter as tk
from tkinter import ttk
from functools import partial
from tools.frames import (
    InspectorFrame,
    SweeperFrame,
    PhoneFrame,
    SampleFrame,
    ReverserFrame,
    AppenderFrame
)

class CSVToolkitWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("CSV Toolkit")
        self.geometry("800x600")
        
        # Tool registry - maps tool names to their frame classes
        self.tools = {
            "CSV Inspector": InspectorFrame,
            "Column Sweeper": SweeperFrame,
            "Order Reverser": ReverserFrame,
            "Sample Maker": SampleFrame,
            "Phone Extractor": PhoneFrame,
            "Column Appender": AppenderFrame
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        """Creates the main UI layout"""
        # Create main container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create sidebar and content area
        self.create_sidebar()
        self.create_content_area()
        self.show_welcome_screen()
        
    def create_sidebar(self):
        """Creates the tool selection sidebar"""
        self.sidebar = ttk.Frame(self.main_container, width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        ttk.Label(
            self.sidebar,
            text="Available Tools",
            font=('Helvetica', 12, 'bold')
        ).pack(pady=(0, 10))
        
        for tool_name, tool_class in self.tools.items():
            btn = ttk.Button(
                self.sidebar,
                text=tool_name,
                command=partial(self.show_tool, tool_class)
            )
            btn.pack(fill=tk.X, pady=2)
            
    def create_content_area(self):
        """Creates the main content area"""
        self.content = ttk.Frame(self.main_container)
        self.content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
    def show_welcome_screen(self):
        """Shows the welcome screen"""
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
        
    def show_tool(self, tool_class):
        """Displays the selected tool"""
        # Clear current content
        for widget in self.content.winfo_children():
            widget.destroy()
            
        # Create and show new tool
        tool = tool_class(self.content)
        tool.pack(fill=tk.BOTH, expand=True) 