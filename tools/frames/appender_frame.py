import tkinter as tk
from tkinter import ttk
from ..base.tool_frame import BaseToolFrame
from ..processors.appender_processor import AppenderProcessor
from ..widgets.config_panel import ConfigPanel
from ..widgets.file_selector import FileSelector

class AppenderFrame(BaseToolFrame):
    """Tool for appending CSV files"""
    
    @classmethod
    def get_tool_name(cls) -> str:
        return "CSV Appender"
    
    def create_widgets(self):
        # Create configuration panel
        self.config_panel = ConfigPanel(self, "Append Settings")
        self.config_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Add file selector for additional files
        self.file_selector = FileSelector(
            self,
            label_text="Additional Files",
            multiple=True
        )
        self.file_selector.pack(fill=tk.X, padx=5, pady=5)
        
        # Add configuration options
        self.config_panel.add_boolean_option(
            'match_columns',
            'Match Column Names',
            default=True,
            callback=self._on_match_columns_changed
        )
        
        self.config_panel.add_boolean_option(
            'ignore_extra',
            'Ignore Extra Columns',
            default=False,
            callback=self._on_ignore_extra_changed
        )
        
        self.config_panel.add_choice_option(
            'join_type',
            'Join Type',
            choices=['Inner', 'Outer', 'Left', 'Right'],
            callback=self._on_join_type_changed
        )
        
        # Preview frame
        self.preview_frame = ttk.LabelFrame(self, text="Preview")
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.preview_tree = ttk.Treeview(self.preview_frame)
        self.preview_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add process button
        self.process_btn = ttk.Button(
            self,
            text="Append Files",
            command=self.process_files
        )
        self.process_btn.pack(pady=10)
    
    def _on_match_columns_changed(self, value: bool):
        """Handles match columns option change"""
        self.save_config()
        self.update_preview()
    
    def _on_ignore_extra_changed(self, value: bool):
        """Handles ignore extra columns option change"""
        self.save_config()
        self.update_preview()
    
    def _on_join_type_changed(self, value: str):
        """Handles join type change"""
        self.save_config()
        self.update_preview()
    
    def update_preview(self):
        """Updates the preview display"""
        try:
            if not hasattr(self, 'processor'):
                self.processor = AppenderProcessor()
            
            files = self.file_selector.get_files()
            if not files:
                return
                
            config = self.config_panel.get_config()
            preview_data = self.processor.preview_append(files[0], files[1:], config)
            
            # Clear current preview
            for item in self.preview_tree.get_children():
                self.preview_tree.delete(item)
            
            # Update columns
            self.preview_tree['columns'] = preview_data.columns.tolist()
            for col in preview_data.columns:
                self.preview_tree.heading(col, text=col)
            
            # Add sample rows
            for idx, row in preview_data.iterrows():
                self.preview_tree.insert('', tk.END, values=row.tolist())
                
        except Exception as e:
            self.show_error(f"Preview error: {str(e)}")
    
    def process_files(self):
        """Processes the selected files"""
        try:
            files = self.file_selector.get_files()
            if not files:
                self.show_error("No files selected")
                return
                
            config = self.config_panel.get_config()
            result = self.processor.process_files(files, config)
            
            if result['success']:
                self.show_success(
                    f"Successfully appended {len(files)} files. "
                    f"Output saved to: {result['output_file']}"
                )
            else:
                self.show_error(result['error'])
                
        except Exception as e:
            self.show_error(f"Error processing files: {str(e)}") 