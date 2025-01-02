class FilterFrame(BaseToolFrame):
    """Tool for filtering CSV data based on conditions"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "Data Filter"
    
    def create_tool_specific_widgets(self):
        # Filter conditions
        conditions_frame = ttk.LabelFrame(self, text="Filter Conditions")
        conditions_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Condition builder
        self.conditions = []
        self.add_condition_row()
        
        # Add/Remove condition buttons
        btn_frame = ttk.Frame(conditions_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(
            btn_frame,
            text="Add Condition",
            command=self.add_condition_row
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            btn_frame,
            text="Remove Last",
            command=self.remove_condition_row
        ).pack(side=tk.LEFT, padx=2) 