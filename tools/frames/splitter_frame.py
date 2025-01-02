class SplitterFrame(BaseToolFrame):
    """Tool for splitting CSV files into smaller files"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "CSV Splitter"
    
    def create_tool_specific_widgets(self):
        # Split options
        options = ttk.LabelFrame(self, text="Split Options")
        options.pack(fill=tk.X, padx=5, pady=5)
        
        # Split type
        self.split_type = tk.StringVar(value="rows")
        ttk.Radiobutton(
            options,
            text="Split by number of rows",
            value="rows",
            variable=self.split_type,
            command=self._update_options
        ).pack(anchor=tk.W, padx=5)
        
        ttk.Radiobutton(
            options,
            text="Split by file size",
            value="size",
            variable=self.split_type,
            command=self._update_options
        ).pack(anchor=tk.W, padx=5)
        
        # Size/rows entry
        size_frame = ttk.Frame(options)
        size_frame.pack(fill=tk.X, padx=5, pady=5)
        self.size_var = tk.StringVar(value="1000")
        ttk.Entry(
            size_frame,
            textvariable=self.size_var,
            width=10
        ).pack(side=tk.LEFT)
        
        self.size_label = ttk.Label(size_frame, text="rows")
        self.size_label.pack(side=tk.LEFT, padx=5) 