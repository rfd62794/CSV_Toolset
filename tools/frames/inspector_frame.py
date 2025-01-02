import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.inspector_processor import InspectorProcessor
from ..widgets.config_panel import ConfigPanel

class InspectorFrame(BaseToolFrame):
    """Tool for inspecting CSV files"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "CSV Inspector"
    
    def create_tool_widgets(self):
        # Create configuration panel
        self.config_panel = ConfigPanel(self, "Inspection Settings")
        self.config_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Add inspection options
        self.config_panel.add_boolean_option(
            'show_datatypes',
            'Show Data Types',
            default=True,
            callback=self._on_option_changed
        )
        
        self.config_panel.add_boolean_option(
            'show_nulls',
            'Show Null Counts',
            default=True,
            callback=self._on_option_changed
        )
        
        self.config_panel.add_boolean_option(
            'show_unique',
            'Show Unique Values',
            default=True,
            callback=self._on_option_changed
        )
        
        # Results display
        self.results_frame = ttk.LabelFrame(self, text="Inspection Results")
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create treeview for results
        self.results_tree = ttk.Treeview(
            self.results_frame,
            columns=('Property', 'Value'),
            show='headings'
        )
        self.results_tree.heading('Property', text='Property')
        self.results_tree.heading('Value', text='Value')
        self.results_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            self.results_frame,
            orient="vertical",
            command=self.results_tree.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
    
    def _on_option_changed(self, *args):
        """Handles option changes"""
        self.save_config()
        self.update_preview()
    
    def _on_file_selected(self, file_path: str):
        """Handles file selection"""
        super()._on_file_selected(file_path)
        self.update_preview()
    
    def update_preview(self):
        """Updates the inspection results"""
        try:
            if not hasattr(self, 'processor'):
                self.processor = InspectorProcessor()
            
            df = self.read_input_file()
            if df is None:
                return
                
            config = self.config_panel.get_config()
            results = self.processor.inspect_data(df, config)
            
            # Clear current results
            for item in self.results_tree.get_children():
                self.results_tree.delete(item)
            
            # Add results to tree
            for category, items in results.items():
                category_id = self.results_tree.insert('', tk.END, values=(category, ''))
                for key, value in items.items():
                    self.results_tree.insert(category_id, tk.END, values=(key, value))
                
        except Exception as e:
            self.show_error(f"Inspection error: {str(e)}") 