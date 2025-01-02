import tkinter as tk
from tkinter import ttk
from tools.utils.tool_manager import ToolManager
# Import individual frames if needed
from tools.frames.inspector_frame import InspectorFrame
from tools.frames.sweeper_frame import SweeperFrame
from tools.frames.phone_frame import PhoneFrame
from tools.frames.sample_frame import SampleFrame
from tools.frames.reverser_frame import ReverserFrame
from tools.frames.appender_frame import AppenderFrame
from pathlib import Path
from tools.test_runner import TestRunnerTool
from datetime import datetime
from tools.frames.merger_frame import MergerFrame
from tools.frames.splitter_frame import SplitterFrame
from tools.frames.transformer_frame import TransformerFrame
from tools.frames.filter_frame import FilterFrame
from tools.frames.validator_frame import ValidatorFrame
from tools.frames.profiler_frame import ProfilerFrame
from tools.frames.column_manager_frame import ColumnManagerFrame
from tools.frames.reformatter_frame import ReformatterFrame

class CSVToolkit(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("CSV Toolkit")
        self.geometry("800x600")
        
        # Initialize tool manager
        self.tool_manager = ToolManager()
        self.register_tools()
        
        self.create_menu()
        self.create_widgets()
        
        self.test_results = []
        
    def register_tools(self):
        """Registers available tools with categories"""
        # Analysis tools
        self.tool_manager.register_tool(InspectorFrame, "Analysis")
        self.tool_manager.register_tool(ProfilerFrame, "Analysis")
        
        # Data cleaning tools
        self.tool_manager.register_tool(SweeperFrame, "Data Cleaning")
        self.tool_manager.register_tool(PhoneFrame, "Data Cleaning")
        self.tool_manager.register_tool(ValidatorFrame, "Data Cleaning")
        
        # Data manipulation tools
        self.tool_manager.register_tool(SampleFrame, "Data Manipulation")
        self.tool_manager.register_tool(ReverserFrame, "Data Manipulation")
        self.tool_manager.register_tool(AppenderFrame, "Data Manipulation")
        self.tool_manager.register_tool(MergerFrame, "Data Manipulation")
        self.tool_manager.register_tool(SplitterFrame, "Data Manipulation")
        self.tool_manager.register_tool(TransformerFrame, "Data Manipulation")
        self.tool_manager.register_tool(FilterFrame, "Data Manipulation")
        self.tool_manager.register_tool(ColumnManagerFrame, "Data Manipulation")
        
        # Data formatting tools
        self.tool_manager.register_tool(ReformatterFrame, "Data Formatting")
    
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
        
        # Create toolbar
        toolbar = ttk.Frame(self)
        toolbar.pack(fill=tk.X, padx=5, pady=2)
        
        # Add test runner button to toolbar
        test_btn = ttk.Button(
            toolbar,
            text="Run Tests",
            command=self.run_tests
        )
        test_btn.pack(side=tk.LEFT, padx=2)
        
        # Add tooltip
        if hasattr(self, 'tooltip'):
            self.tooltip.bind_widget(
                test_btn,
                "Run test suite (Ctrl+T)"
            )
        
        # Add test results frame
        self.results_frame = ttk.LabelFrame(self, text="Test Results")
        self.results_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # Results tree
        self.results_tree = ttk.Treeview(
            self.results_frame,
            columns=('timestamp', 'result', 'categories'),
            show='headings',
            height=3
        )
        
        # Configure columns
        self.results_tree.heading('timestamp', text='Time')
        self.results_tree.heading('result', text='Result')
        self.results_tree.heading('categories', text='Categories')
        
        self.results_tree.column('timestamp', width=150)
        self.results_tree.column('result', width=100)
        self.results_tree.column('categories', width=200)
        
        self.results_tree.pack(fill=tk.X, padx=5, pady=2)
        
        # Add clear results button
        ttk.Button(
            self.results_frame,
            text="Clear History",
            command=self.clear_test_results
        ).pack(side=tk.RIGHT, padx=5, pady=2)
    
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
    
    def create_menu(self):
        """Creates the menu bar"""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        
        # Add test runner to tools menu
        tools_menu.add_command(
            label="Run Tests",
            command=self.run_tests,
            accelerator="Ctrl+T"
        )
        
        # Bind keyboard shortcut
        self.bind_all("<Control-t>", lambda e: self.run_tests())
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Add shortcuts for new tools
        tools_menu.add_command(
            label="Data Profiler",
            command=lambda: self.open_tool(ProfilerFrame),
            accelerator="Ctrl+P"
        )
        tools_menu.add_command(
            label="Data Validator",
            command=lambda: self.open_tool(ValidatorFrame),
            accelerator="Ctrl+V"
        )
        tools_menu.add_command(
            label="Column Manager",
            command=lambda: self.open_tool(ColumnManagerFrame),
            accelerator="Ctrl+M"
        )
        
        # Bind keyboard shortcuts
        self.bind_all("<Control-p>", lambda e: self.open_tool(ProfilerFrame))
        self.bind_all("<Control-v>", lambda e: self.open_tool(ValidatorFrame))
        self.bind_all("<Control-m>", lambda e: self.open_tool(ColumnManagerFrame))
    
    def run_tests(self):
        """Opens the test runner tool"""
        test_runner = TestRunnerTool(
            parent=self,
            callback=self.update_test_results
        )
    
    def update_test_results(self, result_data: dict):
        """Updates test results display"""
        # Add to results list
        self.test_results.append(result_data)
        
        # Format timestamp
        timestamp = datetime.fromisoformat(result_data['timestamp'])
        formatted_time = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        
        # Format result
        result_text = "✓ Passed" if result_data['success'] else "❌ Failed"
        
        # Format categories
        categories = ', '.join(result_data['categories'])
        
        # Add to tree
        self.results_tree.insert(
            '',
            0,  # Insert at top
            values=(formatted_time, result_text, categories)
        )
        
        # Keep only last 10 results
        if len(self.test_results) > 10:
            self.test_results.pop(0)  # Remove oldest
            self.results_tree.delete(self.results_tree.get_children()[-1])
    
    def clear_test_results(self):
        """Clears test results history"""
        self.test_results.clear()
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

if __name__ == "__main__":
    app = CSVToolkit()
    app.mainloop() 