from typing import Dict, Type, List, Set, Tuple, Optional
from ..base.tool_frame import BaseToolFrame

class ToolRegistry:
    """Registry for available tools"""
    
    CATEGORIES = {
        "Analysis": "Tools for analyzing CSV data",
        "Data Cleaning": "Tools for cleaning and validating data",
        "Data Manipulation": "Tools for manipulating data structure",
        "Data Transformation": "Tools for transforming data content"
    }
    
    def __init__(self):
        self._tools = {
            category: [] for category in self.CATEGORIES
        }
    
    def register_tool(self, tool_class, category: str):
        """Registers a tool in a category"""
        if category not in self.CATEGORIES:
            raise ValueError(f"Invalid category: {category}")
        
        if tool_class not in self._tools[category]:
            self._tools[category].append(tool_class)
    
    def get_tools(self, category: str = None) -> list:
        """Gets registered tools, optionally filtered by category"""
        if category:
            if category not in self.CATEGORIES:
                raise ValueError(f"Invalid category: {category}")
            return self._tools[category]
        
        # Return all tools if no category specified
        all_tools = []
        for tools in self._tools.values():
            all_tools.extend(tools)
        return all_tools 