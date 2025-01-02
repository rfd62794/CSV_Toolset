import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.profiler_processor import ProfilerProcessor
from ..widgets.config_panel import ConfigPanel

class ProfilerFrame(BaseToolFrame):
    """Tool for generating data profiles"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "Data Profiler"
    
    def create_tool_widgets(self):
        # Create configuration panel
        self.config_panel = ConfigPanel(self, "Profile Settings")
        self.config_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Add profiling options
        self.config_panel.add_boolean_option(
            'show_stats',
            'Show Statistics',
            default=True,
            callback=self._on_option_changed
        )
        
        self.config_panel.add_boolean_option(
            'show_distribution',
            'Show Distribution',
            default=True,
            callback=self._on_option_changed
        )
        
        self.config_panel.add_boolean_option(
            'show_correlations',
            'Show Correlations',
            default=True,
            callback=self._on_option_changed
        )
        
        self.config_panel.add_numeric_option(
            'sample_size',
            'Sample Size',
            default=1000,
            min_val=100,
            callback=self._on_option_changed
        )
        
        # Results display
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Statistics tab
        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text="Statistics")
        
        self.stats_tree = ttk.Treeview(
            self.stats_frame,
            columns=('Column', 'Type', 'Count', 'Mean', 'Std', 'Min', 'Max'),
            show='headings'
        )
        for col in ('Column', 'Type', 'Count', 'Mean', 'Std', 'Min', 'Max'):
            self.stats_tree.heading(col, text=col)
            self.stats_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(
            self.stats_frame,
            orient="vertical",
            command=self.stats_tree.yview
        )
        self.stats_tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.stats_tree.pack(fill=tk.BOTH, expand=True)
        
        # Distribution tab
        self.dist_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dist_frame, text="Distribution")
        
        self.dist_tree = ttk.Treeview(
            self.dist_frame,
            columns=('Column', 'Unique', 'Missing', 'Top Values'),
            show='headings'
        )
        for col in ('Column', 'Unique', 'Missing', 'Top Values'):
            self.dist_tree.heading(col, text=col)
            self.dist_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(
            self.dist_frame,
            orient="vertical",
            command=self.dist_tree.yview
        )
        self.dist_tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.dist_tree.pack(fill=tk.BOTH, expand=True)
        
        # Correlations tab
        self.corr_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.corr_frame, text="Correlations")
        
        self.corr_tree = ttk.Treeview(
            self.corr_frame,
            columns=('Column 1', 'Column 2', 'Correlation'),
            show='headings'
        )
        for col in ('Column 1', 'Column 2', 'Correlation'):
            self.corr_tree.heading(col, text=col)
            self.corr_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(
            self.corr_frame,
            orient="vertical",
            command=self.corr_tree.yview
        )
        self.corr_tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.corr_tree.pack(fill=tk.BOTH, expand=True)
    
    def _on_option_changed(self, *args):
        """Handles option changes"""
        self.save_config()
        self.update_preview()
    
    def _on_file_selected(self, file_path: str):
        """Handles file selection"""
        self.input_file = file_path
        super()._on_file_selected(file_path)
        self.update_preview()
    
    def update_preview(self):
        """Updates the profile results"""
        try:
            if not hasattr(self, 'processor'):
                self.processor = ProfilerProcessor()
            
            df = self.read_input_file()
            if df is None:
                return
                
            config = self.config_panel.get_config()
            results = self.processor.profile_data(df, config)
            
            # Update statistics
            for item in self.stats_tree.get_children():
                self.stats_tree.delete(item)
            
            if results.get('statistics'):
                for col, stats in results['statistics'].items():
                    self.stats_tree.insert('', tk.END, values=(
                        col,
                        stats['type'],
                        stats['count'],
                        stats.get('mean', 'N/A'),
                        stats.get('std', 'N/A'),
                        stats.get('min', 'N/A'),
                        stats.get('max', 'N/A')
                    ))
            
            # Update distributions
            for item in self.dist_tree.get_children():
                self.dist_tree.delete(item)
            
            if results.get('distribution'):
                for col, dist in results['distribution'].items():
                    self.dist_tree.insert('', tk.END, values=(
                        col,
                        dist['unique'],
                        dist['missing'],
                        str(dist['top_values'])
                    ))
            
            # Update correlations
            for item in self.corr_tree.get_children():
                self.corr_tree.delete(item)
            
            if results.get('correlations'):
                for corr in results['correlations']:
                    self.corr_tree.insert('', tk.END, values=(
                        corr['col1'],
                        corr['col2'],
                        f"{corr['value']:.3f}"
                    ))
                
        except Exception as e:
            self.show_error(f"Profiling error: {str(e)}") 