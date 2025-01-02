class MergerFrame(BaseToolFrame):
    """Tool for merging multiple CSV files"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "CSV Merger"
    
    def create_tool_specific_widgets(self):
        # File selection for multiple files
        self.files = []
        self.file_list = tk.Listbox(self, height=5)
        self.file_list.pack(fill=tk.X, padx=5, pady=5)
        
        # Add/Remove file buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Add Files",
            command=self.add_files
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            btn_frame,
            text="Remove Selected",
            command=self.remove_file
        ).pack(side=tk.LEFT, padx=2)
        
        # Merge options
        self.merge_type = tk.StringVar(value="append")
        options = ttk.LabelFrame(self, text="Merge Options")
        options.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Radiobutton(
            options,
            text="Append (Stack vertically)",
            value="append",
            variable=self.merge_type
        ).pack(anchor=tk.W, padx=5)
        
        ttk.Radiobutton(
            options,
            text="Join (Merge on key)",
            value="join",
            variable=self.merge_type
        ).pack(anchor=tk.W, padx=5) 