import tkinter as tk
from tkinter import ttk
from tools.utils.tool_manager import ToolManager
from tools.frames import (
    InspectorFrame, SweeperFrame, PhoneFrame, 
    SampleFrame, ReverserFrame, AppenderFrame
)

class CSVToolkit(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("CSV Toolkit")
        self.geometry("800x600")
        
        # Initialize tool manager
        self.tool_manager = ToolManager()
        self.register_tools()
        
        self.create_widgets()
        
    def register_tools(self):
        """Registers available tools with categories"""
        # Analysis tools
        self.tool_manager.register_tool(InspectorFrame, "Analysis")
        
        # Data cleaning tools
        self.tool_manager.register_tool(SweeperFrame, "Data Cleaning")
        self.tool_manager.register_tool(PhoneFrame, "Data Cleaning")
        
        # Data manipulation tools
        self.tool_manager.register_tool(SampleFrame, "Data Manipulation")
        self.tool_manager.register_tool(ReverserFrame, "Data Manipulation")
        self.tool_manager.register_tool(AppenderFrame, "Data Manipulation")
    
    def create_widgets(self):
        """Creates main application widgets"""
        # Create main container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create tool selection frame
        self.tool_frame = ttk.LabelFrame(self.main_container, text="Tools")
        self.tool_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Create notebook for categorized tools
        self.tool_notebook = ttk.Notebook(self.tool_frame)
        self.tool_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Add tool categories
        self.category_frames = {}
        for category, tools in self.tool_manager.get_categories().items():
            frame = ttk.Frame(self.tool_notebook)
            self.tool_notebook.add(frame, text=category)
            
            for tool_name in tools:
                btn = ttk.Button(
                    frame,
                    text=tool_name,
                    command=lambda t=tool_name: self.show_tool(t)
                )
                btn.pack(padx=5, pady=2, fill=tk.X)
            
            self.category_frames[category] = frame
        
        # Create tool display area
        self.tool_display = ttk.Frame(self.main_container)
        self.tool_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Show welcome message
        self.show_welcome()
    
    def show_welcome(self):
        """Shows welcome message"""
        for widget in self.tool_display.winfo_children():
            widget.destroy()
            
        welcome = ttk.Label(
            self.tool_display,
            text="Welcome to CSV Toolkit!\n\nSelect a tool to begin.",
            justify=tk.CENTER
        )
        welcome.pack(expand=True)
    
    def show_tool(self, tool_name):
        """Shows selected tool"""
        # Clear current tool
        for widget in self.tool_display.winfo_children():
            widget.destroy()
        
        try:
            # Create and show new tool
            tool = self.tool_manager.create_tool(tool_name, self.tool_display)
            tool.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
        except Exception as e:
            # Show error if tool creation fails
            error = ttk.Label(
                self.tool_display,
                text=f"Error loading tool: {str(e)}",
                foreground='red'
            )
            error.pack(expand=True)

if __name__ == "__main__":
    app = CSVToolkit()
    app.mainloop() 