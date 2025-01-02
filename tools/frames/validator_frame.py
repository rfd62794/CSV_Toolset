import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.validator_processor import ValidatorProcessor

class ValidatorFrame(BaseToolFrame):
    """Tool for validating data against rules"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "Data Validator"
    
    def create_tool_specific_widgets(self):
        # Rules section
        rules_frame = ttk.LabelFrame(self, text="Validation Rules")
        rules_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Column selection
        col_frame = ttk.Frame(rules_frame)
        col_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(col_frame, text="Column:").pack(side=tk.LEFT)
        self.column_var = tk.StringVar()
        self.column_combo = ttk.Combobox(
            col_frame,
            textvariable=self.column_var,
            state='readonly'
        )
        self.column_combo.pack(side=tk.LEFT, padx=5)
        
        # Rule types
        rules_list = ttk.Frame(rules_frame)
        rules_list.pack(fill=tk.X, padx=5, pady=2)
        
        self.rule_vars = {}
        rules = [
            ("Not Null", "null_check"),
            ("Unique Values", "unique_check"),
            ("Data Type", "type_check"),
            ("Value Range", "range_check"),
            ("Pattern Match", "pattern_check"),
            ("Custom Function", "custom_check")
        ]
        
        for label, key in rules:
            var = tk.BooleanVar()
            self.rule_vars[key] = var
            ttk.Checkbutton(
                rules_list,
                text=label,
                variable=var,
                command=lambda k=key: self._toggle_rule(k)
            ).pack(anchor=tk.W)
        
        # Rule configuration
        self.config_frame = ttk.LabelFrame(self, text="Rule Configuration")
        self.config_frame.pack(fill=tk.X, padx=5, pady=5) 