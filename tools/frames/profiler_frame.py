import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.profiler_processor import ProfilerProcessor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class ProfilerFrame(BaseToolFrame):
    """Tool for generating data profiles and visualizations"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "Data Profiler"
    
    def create_tool_specific_widgets(self):
        # Profile options
        options_frame = ttk.LabelFrame(self, text="Profile Options")
        options_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Analysis types
        self.analysis_vars = {}
        analyses = [
            ("Basic Statistics", "basic_stats"),
            ("Data Types", "data_types"),
            ("Missing Values", "missing_values"),
            ("Value Distribution", "distribution"),
            ("Correlations", "correlations"),
            ("Outliers", "outliers"),
            ("Pattern Analysis", "patterns")
        ]
        
        for label, key in analyses:
            var = tk.BooleanVar(value=True)
            self.analysis_vars[key] = var
            ttk.Checkbutton(
                options_frame,
                text=label,
                variable=var
            ).pack(anchor=tk.W, padx=5)
        
        # Results display
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs for different result types
        self.stats_frame = ttk.Frame(self.notebook)
        self.viz_frame = ttk.Frame(self.notebook)
        self.issues_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.stats_frame, text="Statistics")
        self.notebook.add(self.viz_frame, text="Visualizations")
        self.notebook.add(self.issues_frame, text="Data Issues")
        
        # Statistics display
        self.stats_tree = ttk.Treeview(
            self.stats_frame,
            columns=('metric', 'value'),
            show='headings'
        )
        self.stats_tree.heading('metric', text='Metric')
        self.stats_tree.heading('value', text='Value')
        self.stats_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Visualization canvas
        self.fig = Figure(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, self.viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Issues display
        self.issues_text = tk.Text(self.issues_frame, wrap=tk.WORD)
        self.issues_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def process_file(self):
        """Processes the selected file"""
        if not self.validate_input():
            return
        
        try:
            # Get selected analyses
            analyses = {
                key: var.get()
                for key, var in self.analysis_vars.items()
            }
            
            # Process data
            processor = ProfilerProcessor()
            df = self.read_input_file()
            profile_results = processor.profile_data(df, analyses)
            
            # Display results
            self.display_results(profile_results)
            
        except Exception as e:
            self.show_error(f"Error profiling data: {str(e)}")
    
    def display_results(self, results: dict):
        """Displays profiling results"""
        # Clear previous results
        self.stats_tree.delete(*self.stats_tree.get_children())
        self.issues_text.delete('1.0', tk.END)
        self.fig.clear()
        
        # Display statistics
        if 'basic_stats' in results:
            for metric, value in results['basic_stats'].items():
                self.stats_tree.insert('', tk.END, values=(metric, value))
        
        # Display visualizations
        if 'distribution' in results:
            self.plot_distributions(results['distribution'])
        
        # Display issues
        if 'issues' in results:
            for issue in results['issues']:
                self.issues_text.insert(tk.END, f"• {issue}\n")
        
        self.canvas.draw()
    
    def plot_distributions(self, dist_data: dict):
        """Plots value distributions"""
        ax = self.fig.add_subplot(111)
        ax.clear()
        
        # Plot histogram for numeric columns
        if 'numeric_dist' in dist_data:
            ax.hist(dist_data['numeric_dist'], bins=30)
            ax.set_title('Value Distribution')
            ax.set_xlabel('Value')
            ax.set_ylabel('Frequency') 