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
        
        # Add configuration panel
        self.config_panel = ConfigPanel(self, "Transform Settings")
        self.config_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Add configuration options
        self.config_panel.add_boolean_option(
            'preserve_original', 
            'Preserve original column',
            default=True,
            callback=self._on_preserve_changed
        )
        
        self.config_panel.add_choice_option(
            'null_handling',
            'Null Value Handling',
            choices=['Skip', 'Keep', 'Replace'],
            callback=self._on_null_handling_changed
        )
        
        self.config_panel.add_text_option(
            'null_replacement',
            'Null Replacement Value',
            default='',
            callback=self._on_replacement_changed
        )
        
        # Load saved configuration
        saved_config = self.parent.tool_manager.get_tool_config(self.get_tool_name())
        if saved_config:
            self.config_panel.set_config(saved_config)

    def get_config(self) -> dict:
        """Gets current tool configuration"""
        return self.config_panel.get_config()

    def _on_preserve_changed(self, value: bool):
        """Handles preserve original column option change"""
        # Implementation...
        self.save_config()

    def _on_null_handling_changed(self, value: str):
        """Handles null handling option change"""
        # Implementation...
        self.save_config()

    def _on_replacement_changed(self, value: str):
        """Handles null replacement value change"""
        # Implementation...
        self.save_config() 