import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.validator_processor import ValidatorProcessor
from ..widgets.config_panel import ConfigPanel
from ..widgets.list_selector import ListSelector

class ValidatorFrame(BaseToolFrame):
    """Tool for validating data quality"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "Data Validator"
    
    def create_tool_widgets(self):
        # Create main container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left panel for configuration
        self.left_panel = ttk.Frame(self.main_container)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Create configuration panel
        self.config_panel = ConfigPanel(self.left_panel, "Validation Settings")
        self.config_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Add validation options
        self.config_panel.add_boolean_option(
            'check_missing',
            'Check Missing Values',
            default=True,
            callback=self._on_option_changed
        )
        
        self.config_panel.add_boolean_option(
            'check_duplicates',
            'Check Duplicates',
            default=True,
            callback=self._on_option_changed
        )
        
        self.config_panel.add_boolean_option(
            'check_datatypes',
            'Check Data Types',
            default=True,
            callback=self._on_option_changed
        )
        
        self.config_panel.add_boolean_option(
            'check_outliers',
            'Check Outliers',
            default=True,
            callback=self._on_option_changed
        )
        
        # Column selector
        self.column_selector = ListSelector(
            self.left_panel,
            title="Columns to Validate",
            multiple=True
        )
        self.column_selector.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Right panel for results
        self.right_panel = ttk.Frame(self.main_container)
        self.right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Results notebook
        self.notebook = ttk.Notebook(self.right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Summary tab
        self.summary_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.summary_frame, text="Summary")
        
        self.summary_tree = ttk.Treeview(
            self.summary_frame,
            columns=('Column', 'Issues', 'Details'),
            show='headings'
        )
        for col in ('Column', 'Issues', 'Details'):
            self.summary_tree.heading(col, text=col)
            self.summary_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(
            self.summary_frame,
            orient="vertical",
            command=self.summary_tree.yview
        )
        self.summary_tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.summary_tree.pack(fill=tk.BOTH, expand=True)
        
        # Details tab
        self.details_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.details_frame, text="Details")
        
        self.details_tree = ttk.Treeview(
            self.details_frame,
            columns=('Row', 'Column', 'Value', 'Issue'),
            show='headings'
        )
        for col in ('Row', 'Column', 'Value', 'Issue'):
            self.details_tree.heading(col, text=col)
            self.details_tree.column(col, width=125)
        
        scrollbar = ttk.Scrollbar(
            self.details_frame,
            orient="vertical",
            command=self.details_tree.yview
        )
        self.details_tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.details_tree.pack(fill=tk.BOTH, expand=True)
        
        # Buttons frame
        self.button_frame = ttk.Frame(self.right_panel)
        self.button_frame.pack(fill=tk.X, pady=10)
        
        # Validate button
        self.validate_btn = ttk.Button(
            self.button_frame,
            text="Validate Data",
            command=self.validate_data
        )
        self.validate_btn.pack(side=tk.LEFT, padx=5)
        
        # Export button
        self.export_btn = ttk.Button(
            self.button_frame,
            text="Export Report",
            command=self.export_report
        )
        self.export_btn.pack(side=tk.LEFT, padx=5)
    
    def _on_option_changed(self, *args):
        """Handles option changes"""
        self.save_config()
        self.update_preview()
    
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
        """Updates the validation preview"""
        try:
            if not hasattr(self, 'processor'):
                self.processor = ValidatorProcessor()
            
            df = self.read_input_file()
            if df is None:
                return
                
            config = self.config_panel.get_config()
            config['columns'] = self.column_selector.get_selected()
            
            results = self.processor.validate_data(df, config)
            self._update_results_display(results)
                
        except Exception as e:
            self.show_error(f"Validation error: {str(e)}")
    
    def _update_results_display(self, results: dict):
        """Updates the results display"""
        # Clear current results
        for tree in (self.summary_tree, self.details_tree):
            for item in tree.get_children():
                tree.delete(item)
        
        # Update summary
        for col, issues in results['summary'].items():
            self.summary_tree.insert('', tk.END, values=(
                col,
                len(issues),
                '; '.join(issues)
            ))
        
        # Update details
        for issue in results['details']:
            self.details_tree.insert('', tk.END, values=(
                issue['row'],
                issue['column'],
                issue['value'],
                issue['issue']
            ))
    
    def validate_data(self):
        """Performs full data validation"""
        try:
            if not hasattr(self, 'processor'):
                self.processor = ValidatorProcessor()
            
            df = self.read_input_file()
            if df is None:
                return
                
            config = self.config_panel.get_config()
            config['columns'] = self.column_selector.get_selected()
            
            results = self.processor.validate_data(df, config)
            self._update_results_display(results)
            
            self.show_success("Validation complete!")
                
        except Exception as e:
            self.show_error(f"Validation error: {str(e)}")
    
    def export_report(self):
        """Exports validation report"""
        try:
            if not hasattr(self, 'processor'):
                self.processor = ValidatorProcessor()
            
            df = self.read_input_file()
            if df is None:
                return
                
            config = self.config_panel.get_config()
            config['columns'] = self.column_selector.get_selected()
            
            result = self.processor.export_report(df, config)
            
            if result['success']:
                self.show_success(
                    f"Successfully exported validation report. "
                    f"Output saved to: {result['output_file']}"
                )
            else:
                self.show_error(result['error'])
                
        except Exception as e:
            self.show_error(f"Export error: {str(e)}") 