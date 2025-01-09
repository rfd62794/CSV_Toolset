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
import tkinter.messagebox as messagebox

class CSVToolkit(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("CSV Toolkit")
        self.geometry("800x600")
        
        # Initialize tool manager
        self.tool_manager = ToolManager()
        self.register_tools()
        
        # Category descriptions and icons
        self.categories = {
            "Analysis": {
                "desc": "Tools for analyzing and understanding CSV data structure and content",
                "icon": "📊",
                "tools": {
                    "CSV Inspector": "Examine CSV file structure and contents",
                    "Data Profiler": "Generate statistical profiles of your data"
                }
            },
            "Data Cleaning": {
                "desc": "Tools for cleaning and standardizing data",
                "icon": "🧹",
                "tools": {
                    "Column Sweeper": "Clean and standardize column data",
                    "Phone Formatter": "Format and validate phone numbers",
                    "Data Validator": "Validate data quality and consistency"
                }
            },
            "Data Manipulation": {
                "desc": "Tools for modifying and transforming data",
                "icon": "🔧",
                "tools": {
                    "Sample Maker": "Create data samples",
                    "Order Reverser": "Reverse row order",
                    "Column Appender": "Add columns to CSV files",
                    "CSV Merger": "Combine multiple CSV files",
                    "CSV Splitter": "Split CSV into multiple files",
                    "Data Transformer": "Transform column values",
                    "Data Filter": "Filter rows based on conditions",
                    "Column Manager": "Manage and organize columns"
                }
            },
            "Data Formatting": {
                "desc": "Tools for formatting and exporting data",
                "icon": "📝",
                "tools": {
                    "Data Reformatter": "Reformat CSV files with different options"
                }
            }
        }
        
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
    
    def _update_tool_buttons(self):
        """Updates tool buttons based on registered tools"""
        categories = self.tool_manager.get_categories()
        for category, tools in categories.items():
            if category in self.category_frames:
                frame = self.category_frames[category]
                for tool_name in tools:
                    if tool_name not in self.tool_buttons:
                        btn = ttk.Button(
                            frame,
                            text=tool_name,
                            command=lambda t=tool_name: self.show_tool(t)
                        )
                        btn.pack(padx=5, pady=2, fill=tk.X)
                        self.tool_buttons[tool_name] = {
                            'button': btn,
                            'category': category,
                            'tooltip': self.categories[category]['tools'].get(tool_name, '')
                        }
    
    def create_widgets(self):
        """Creates main application widgets"""
        try:
            # Create main container with padding
            self.main_container = ttk.Frame(self)
            self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Initialize dictionaries
            self.tool_buttons = {}
            self.category_frames = {}
            self.test_results = []
            
            # Create tool selection frame
            self.tool_frame = ttk.Frame(self.main_container)
            self.tool_frame.pack(fill=tk.BOTH, expand=True)
            
            # Add search frame
            self.search_frame = ttk.Frame(self.tool_frame)
            self.search_frame.pack(fill=tk.X, pady=(0, 15))
            
            self.search_var = tk.StringVar()
            self.search_var.trace('w', self._filter_tools)
            
            search_label = ttk.Label(
                self.search_frame,
                text="🔍 Search Tools:",
                font=('Helvetica', 10)
            )
            search_label.pack(side=tk.LEFT, padx=(0, 5))
            
            self.search_entry = ttk.Entry(
                self.search_frame,
                textvariable=self.search_var,
                width=40
            )
            self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Create category frames
            for category, info in self.categories.items():
                # Create frame for this category
                category_frame = ttk.LabelFrame(
                    self.tool_frame,
                    text=f"{info['icon']} {category}",
                    padding=10
                )
                category_frame.pack(fill=tk.X, pady=(0, 15))
                
                # Add category description
                desc_label = ttk.Label(
                    category_frame,
                    text=info['desc'],
                    wraplength=600,
                    justify=tk.LEFT,
                    font=('Helvetica', 9, 'italic')
                )
                desc_label.pack(fill=tk.X, pady=(0, 10))
                
                # Create tool buttons frame
                tools_frame = ttk.Frame(category_frame)
                tools_frame.pack(fill=tk.X)
                
                # Create grid for tool buttons
                row = 0
                col = 0
                max_cols = 2
                
                for tool_name, description in info['tools'].items():
                    # Create tool button frame
                    tool_frame = ttk.Frame(tools_frame, padding=5)
                    tool_frame.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)
                    
                    # Configure grid weights
                    tools_frame.grid_columnconfigure(col, weight=1)
                    
                    # Create tool button with icon and name
                    btn = ttk.Button(
                        tool_frame,
                        text=f"{tool_name}",
                        command=lambda t=tool_name: self.show_tool(t),
                        style='Tool.TButton'
                    )
                    btn.pack(fill=tk.X)
                    
                    # Add tool description
                    desc_label = ttk.Label(
                        tool_frame,
                        text=description,
                        wraplength=280,
                        justify=tk.LEFT,
                        font=('Helvetica', 8)
                    )
                    desc_label.pack(fill=tk.X, pady=(5, 0))
                    
                    # Store button reference
                    self.tool_buttons[tool_name] = {
                        'button': btn,
                        'category': category,
                        'tooltip': description
                    }
                    
                    # Update grid position
                    col += 1
                    if col >= max_cols:
                        col = 0
                        row += 1
                
                self.category_frames[category] = category_frame
            
            # Configure style for tool buttons
            style = ttk.Style()
            style.configure(
                'Tool.TButton',
                padding=10,
                font=('Helvetica', 10, 'bold')
            )
            
        except Exception as e:
            messagebox.showerror(
                "Initialization Error",
                f"Error creating application: {str(e)}"
            )
    
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
            # Make tool_manager accessible to the tool
            tool.tool_manager = self.tool_manager
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
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        
        # File menu
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.quit)
        
        # Tools menu
        tools_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Tools", menu=tools_menu)
        
        # Add test runner to tools menu
        tools_menu.add_command(
            label="Run Tests",
            command=self.run_tests,
            accelerator="Ctrl+T"
        )
        
        # Bind keyboard shortcut
        self.bind_all("<Control-t>", lambda e: self.run_tests())
        
        # Help menu
        help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=help_menu)
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

    def _create_tooltip(self, widget, text):
        """Creates a tooltip for a widget"""
        widget.bind('<Enter>', lambda e: self._show_tooltip(e, text))
        widget.bind('<Leave>', lambda e: self._hide_tooltip())

    def _show_tooltip(self, event, text):
        """Shows tooltip"""
        x, y, _, _ = event.widget.bbox("insert")
        x += event.widget.winfo_rootx() + 25
        y += event.widget.winfo_rooty() + 20
        
        # Creates a toplevel window
        self.tooltip = tk.Toplevel(self)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = ttk.Label(
            self.tooltip,
            text=text,
            justify=tk.LEFT,
            background="#ffffe0",
            relief='solid',
            borderwidth=1
        )
        label.pack()

    def _hide_tooltip(self):
        """Hides tooltip"""
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()

    def _filter_tools(self, *args):
        """Filters tools based on search text"""
        search_text = self.search_var.get().lower()
        
        for tool_name, info in self.tool_buttons.items():
            button = info['button']
            tooltip = info['tooltip']
            
            # Check if search matches tool name or tooltip
            if (search_text in tool_name.lower() or 
                search_text in tooltip.lower()):
                button.pack(padx=5, pady=2, fill=tk.X)
            else:
                button.pack_forget()

    def show_about(self):
        """Shows about dialog"""
        about_window = tk.Toplevel(self)
        about_window.title("About CSV Toolkit")
        about_window.geometry("400x300")
        about_window.resizable(False, False)
        
        # Center window
        about_window.transient(self)
        about_window.grab_set()
        
        # Add content
        content_frame = ttk.Frame(about_window, padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(
            content_frame,
            text="CSV Toolkit",
            font=('Helvetica', 16, 'bold')
        )
        title.pack(pady=(0, 10))
        
        # Version
        version = ttk.Label(
            content_frame,
            text="Version 1.0.0"
        )
        version.pack()
        
        # Description
        description = ttk.Label(
            content_frame,
            text=(
                "A collection of tools for working with CSV files.\n\n"
                "Features:\n"
                "• Data Analysis\n"
                "• Data Cleaning\n"
                "• Data Manipulation\n"
                "• Data Formatting"
            ),
            justify=tk.LEFT,
            wraplength=350
        )
        description.pack(pady=20)
        
        # Copyright
        copyright = ttk.Label(
            content_frame,
            text="© 2024 CSV Toolkit"
        )
        copyright.pack(pady=(20, 0))
        
        # Close button
        ttk.Button(
            content_frame,
            text="Close",
            command=about_window.destroy
        ).pack(pady=20)
        
        # Center the window on screen
        about_window.update_idletasks()
        width = about_window.winfo_width()
        height = about_window.winfo_height()
        x = (about_window.winfo_screenwidth() // 2) - (width // 2)
        y = (about_window.winfo_screenheight() // 2) - (height // 2)
        about_window.geometry(f'+{x}+{y}')

if __name__ == "__main__":
    app = CSVToolkit()
    app.mainloop() 