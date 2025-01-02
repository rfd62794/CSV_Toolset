import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.reformatter_processor import ReformatterProcessor
from ..widgets.options_frame import OptionsFrame
from ..widgets.list_selector import ListSelector

class ReformatterFrame(BaseToolFrame):
    """Frame for reformatting CSV data"""
    
    def __init__(self, master):
        super().__init__(master)
        self.processor = ReformatterProcessor()
        self.create_tool_specific_widgets()
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "Data Reformatter"
    
    def create_tool_specific_widgets(self):
        # Column selection
        self.column_frame = ttk.LabelFrame(self, text="Column Selection")
        self.column_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.column_selector = ListSelector(
            self.column_frame,
            "Select columns to reformat:"
        )
        self.column_selector.pack(fill=tk.X, padx=5, pady=5)
        
        # Options frame
        self.options = OptionsFrame(self)
        self.options.pack(fill=tk.X, padx=10, pady=5)
        
        # Case options
        self.case_var = tk.StringVar(value='none')
        case_frame = ttk.LabelFrame(self.options, text="Case Transformation")
        case_frame.pack(fill=tk.X, padx=5, pady=5)
        
        for text, value in [
            ("No change", "none"),
            ("UPPERCASE", "upper"),
            ("lowercase", "lower"),
            ("Title Case", "title")
        ]:
            ttk.Radiobutton(
                case_frame,
                text=text,
                value=value,
                variable=self.case_var
            ).pack(anchor=tk.W, padx=5, pady=2)
        
        # Other options
        self.options.add_checkbox(
            'trim',
            "Trim whitespace",
            default=True
        )
        
        self.options.add_checkbox(
            'remove_special',
            "Remove special characters",
            default=False
        )
        
        # Format options
        format_frame = ttk.LabelFrame(self.options, text="Format Options")
        format_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Date format
        date_frame = ttk.Frame(format_frame)
        date_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(date_frame, text="Date format:").pack(side=tk.LEFT)
        self.date_var = tk.StringVar(value="%Y-%m-%d")
        ttk.Entry(
            date_frame,
            textvariable=self.date_var,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        # Number format
        num_frame = ttk.Frame(format_frame)
        num_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(num_frame, text="Number format:").pack(side=tk.LEFT)
        self.number_var = tk.StringVar(value=".2f")
        ttk.Entry(
            num_frame,
            textvariable=self.number_var,
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        # Process button
        self.process_btn = ttk.Button(
            self,
            text="Reformat Data",
            command=self.process_file
        )
        self.process_btn.pack(pady=10)
        
        # Bind file selection to column update
        self.file_path_var.trace_add('write', self.update_columns)
    
    def update_columns(self, *args):
        """Updates available columns when file is selected"""
        if self.input_file:
            try:
                columns = self.processor.get_columns(self.input_file)
                self.column_selector.set_items(columns)
            except Exception as e:
                self.show_error(str(e))
    
    def process_file(self):
        """Processes the selected file"""
        if not self.input_file:
            self.show_warning("Please select a file first")
            return
            
        selected_columns = self.column_selector.get_selected()
        if not selected_columns:
            self.show_warning("Please select at least one column")
            return
            
        try:
            # Get options
            case = self.case_var.get()
            if case == 'none':
                case = None
                
            # Process file
            result_df, stats = self.processor.process_file(
                self.input_file,
                columns=selected_columns,
                case=case,
                trim=self.options.get_option('trim'),
                remove_special=self.options.get_option('remove_special'),
                date_format=self.date_var.get(),
                number_format=self.number_var.get(),
                progress_callback=self.update_progress
            )
            
            # Generate output filename
            output_file = self.file_manager.generate_output_path(
                self.input_file,
                "reformatted"
            )
            
            # Save results
            success, error = self.writer.write_csv(result_df, output_file)
            if not success:
                raise Exception(error)
            
            # Show success message
            message = (
                f"Complete! Processed {stats['columns_processed']} columns "
                f"across {stats['total_rows']:,} rows.\n"
                f"Saved to: {output_file}"
            )
            self.update_progress(100, message)
            
        except Exception as e:
            self.show_error(str(e)) 