import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.validator_processor import ValidatorProcessor
from ..widgets.config_panel import ConfigPanel

class ValidatorFrame(BaseToolFrame):
    """Tool for validating CSV data"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "Data Validator"
    
    def create_widgets(self):
        # Create configuration panel
        self.config_panel = ConfigPanel(self, "Validation Settings")
        self.config_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Add validation rules
        self.config_panel.add_boolean_option(
            'check_datatypes',
            'Check Data Types',
            default=True
        )
        
        self.config_panel.add_boolean_option(
            'check_nulls',
            'Check for Null Values',
            default=True
        )
        
        self.config_panel.add_boolean_option(
            'check_duplicates',
            'Check for Duplicates',
            default=True
        )
        
        self.config_panel.add_boolean_option(
            'check_ranges',
            'Check Value Ranges',
            default=False,
            callback=self._on_range_check_changed
        )
        
        # Range settings
        self.range_frame = ttk.LabelFrame(self, text="Range Settings")
        self.ranges = {}  # Column -> {min, max}
        
        # Range configuration
        self.range_config = ttk.Frame(self.range_frame)
        self.range_config.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(self.range_config, text="Column:").pack(side=tk.LEFT)
        self.range_column = ttk.Combobox(self.range_config, state='readonly')
        self.range_column.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.range_config, text="Min:").pack(side=tk.LEFT)
        self.range_min = ttk.Entry(self.range_config, width=10)
        self.range_min.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.range_config, text="Max:").pack(side=tk.LEFT)
        self.range_max = ttk.Entry(self.range_config, width=10)
        self.range_max.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            self.range_config,
            text="Add Range",
            command=self._add_range
        ).pack(side=tk.LEFT, padx=5)
        
        # Range list
        self.range_list = ttk.Treeview(
            self.range_frame,
            columns=('Column', 'Min', 'Max'),
            show='headings',
            height=3
        )
        for col in ('Column', 'Min', 'Max'):
            self.range_list.heading(col, text=col)
        self.range_list.pack(fill=tk.X, padx=5, pady=5)
        
        # Add validate button
        self.validate_btn = ttk.Button(
            self,
            text="Validate Data",
            command=self.process_file
        )
        self.validate_btn.pack(pady=10)
        
        # Results display
        self.results_frame = ttk.LabelFrame(self, text="Validation Results")
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.results_tree = ttk.Treeview(
            self.results_frame,
            columns=('Column', 'Rule', 'Status', 'Details'),
            show='headings'
        )
        
        for col in ('Column', 'Rule', 'Status', 'Details'):
            self.results_tree.heading(col, text=col)
        
        self.results_tree.pack(fill=tk.BOTH, expand=True)

    def _on_range_check_changed(self, value: bool):
        """Handles range check option change"""
        if value:
            self.range_frame.pack(fill=tk.X, padx=5, pady=5)
        else:
            self.range_frame.pack_forget()
        self.save_config()

    def update_results(self, validation_results: dict):
        """Updates the validation results display"""
        # Clear previous results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Add new results
        for rule, result in validation_results.items():
            status = "✓ Pass" if result['passed'] else "❌ Fail"
            details = result.get('details', '')
            self.results_tree.insert('', tk.END, values=(rule, status, details)) 

    def _add_range(self):
        """Adds a range check for a column"""
        column = self.range_column.get()
        try:
            min_val = float(self.range_min.get())
            max_val = float(self.range_max.get())
            
            self.ranges[column] = {'min': min_val, 'max': max_val}
            
            # Update range list
            self.range_list.insert('', tk.END, values=(
                column, min_val, max_val
            ))
            
            # Clear inputs
            self.range_min.delete(0, tk.END)
            self.range_max.delete(0, tk.END)
            
        except ValueError:
            self.show_error("Please enter valid numeric values for min and max")

    def process_file(self):
        """Validates the input file"""
        if not hasattr(self, 'processor'):
            self.processor = ValidatorProcessor()
            
        try:
            config = self.config_panel.get_config()
            config['ranges'] = self.ranges
            
            result = self.processor.process_file(self.input_file, config)
            
            if result['success']:
                self.update_results(result['validation_results'])
            else:
                self.show_error(result['error'])
                
        except Exception as e:
            self.show_error(f"Error validating file: {str(e)}") 