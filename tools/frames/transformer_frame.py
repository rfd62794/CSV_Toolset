class TransformerFrame(BaseToolFrame):
    """Tool for applying transformations to columns"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "Data Transformer"
    
    def create_tool_specific_widgets(self):
        # Column selection
        col_frame = ttk.LabelFrame(self, text="Column Selection")
        col_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.column_var = tk.StringVar()
        self.column_combo = ttk.Combobox(
            col_frame,
            textvariable=self.column_var,
            state='readonly'
        )
        self.column_combo.pack(fill=tk.X, padx=5, pady=5)
        
        # Transformation selection
        trans_frame = ttk.LabelFrame(self, text="Transformations")
        trans_frame.pack(fill=tk.X, padx=5, pady=5)
        
        transformations = [
            "Uppercase",
            "Lowercase",
            "Title Case",
            "Strip Whitespace",
            "Remove Special Characters",
            "Format Numbers",
            "Format Dates",
            "Custom Regex"
        ]
        
        self.trans_vars = {}
        for trans in transformations:
            var = tk.BooleanVar()
            self.trans_vars[trans] = var
            ttk.Checkbutton(
                trans_frame,
                text=trans,
                variable=var
            ).pack(anchor=tk.W, padx=5) 