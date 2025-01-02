import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.sweeper_processor import SweeperProcessor
from ..widgets.config_panel import ConfigPanel
from ..widgets.list_selector import ListSelector

class SweeperFrame(BaseToolFrame):
    """Tool for cleaning and standardizing data"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "Column Sweeper"
    
    def create_tool_widgets(self):
        # Create main container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left panel for configuration
        self.left_panel = ttk.Frame(self.main_container)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Create configuration panel
        self.config_panel = ConfigPanel(self.left_panel, "Cleaning Settings")
        self.config_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Add cleaning options
        self.config_panel.add_boolean_option(
            'trim_whitespace',
            'Trim Whitespace',
            default=True,
            callback=self._on_option_changed
        )
        
        self.config_panel.add_boolean_option(
            'remove_duplicates',
            'Remove Duplicates',
            default=False,
            callback=self._on_option_changed
        )
        
        self.config_panel.add_boolean_option(
            'drop_empty',
            'Drop Empty Rows',
            default=False,
            callback=self._on_option_changed
        )
        
        self.config_panel.add_choice_option(
            'null_handling',
            'Null Handling',
            choices=['Keep', 'Remove', 'Fill'],
            callback=self._on_null_handling_changed
        )
        
        self.config_panel.add_text_option(
            'fill_value',
            'Fill Value',
            default='',
            callback=self._on_option_changed
        )
        
        # Column selector
        self.column_selector = ListSelector(
            self.left_panel,
            title="Columns to Clean",
            multiple=True
        )
        self.column_selector.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Right panel for preview
        self.right_panel = ttk.Frame(self.main_container)
        self.right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Preview frame
        self.preview_frame = ttk.LabelFrame(self.right_panel, text="Preview")
        self.preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # Preview tree
        self.preview_tree = ttk.Treeview(self.preview_frame)
        self.preview_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar to preview
        scrollbar = ttk.Scrollbar(
            self.preview_frame,
            orient="vertical",
            command=self.preview_tree.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.preview_tree.configure(yscrollcommand=scrollbar.set)
        
        # Process button
        self.process_btn = ttk.Button(
            self.right_panel,
            text="Clean Data",
            command=self.process_file
        )
        self.process_btn.pack(pady=10)
        
        # Initially hide fill value option
        self.config_panel.hide_option('fill_value')
    
    def _on_option_changed(self, *args):
        """Handles option changes"""
        self.save_config()
        self.update_preview()
    
    def _on_null_handling_changed(self, value: str):
        """Handles null handling option change"""
        if value == 'Fill':
            self.config_panel.show_option('fill_value')
        else:
            self.config_panel.hide_option('fill_value')
        self._on_option_changed()
    
    def _on_file_selected(self, file_path: str):
        """Handles file selection"""
        self.input_file = file_path
        super()._on_file_selected(file_path)
        
        # Update column choices
        df = self.read_input_file()
        if df is not None and not df.empty:
            self.column_selector.set_items(df.columns.tolist())
            self.update_preview()
    
    def update_preview(self):
        """Updates the preview display"""
        try:
            if not hasattr(self, 'processor'):
                self.processor = SweeperProcessor()
            
            df = self.read_input_file()
            if df is None:
                return
                
            config = self.config_panel.get_config()
            config['columns'] = self.column_selector.get_selected()
            
            preview_data = self.processor.preview_clean(df, config)
            
            # Clear current preview
            for item in self.preview_tree.get_children():
                self.preview_tree.delete(item)
            
            # Update columns
            self.preview_tree['columns'] = preview_data.columns.tolist()
            for col in preview_data.columns:
                self.preview_tree.heading(col, text=col)
            
            # Add preview rows
            for idx, row in preview_data.iterrows():
                self.preview_tree.insert('', tk.END, values=row.tolist())
                
        except Exception as e:
            self.show_error(f"Preview error: {str(e)}")
    
    def process_file(self):
        """Processes the input file"""
        try:
            if not hasattr(self, 'processor'):
                self.processor = SweeperProcessor()
            
            df = self.read_input_file()
            if df is None:
                return
                
            config = self.config_panel.get_config()
            config['columns'] = self.column_selector.get_selected()
            
            result = self.processor.process_file(df, config)
            
            if result['success']:
                self.show_success(
                    f"Successfully cleaned data. "
                    f"Output saved to: {result['output_file']}"
                )
            else:
                self.show_error(result['error'])
                
        except Exception as e:
            self.show_error(f"Error processing file: {str(e)}") 