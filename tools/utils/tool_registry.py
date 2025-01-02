from typing import Dict, Type, List, Optional
from ..base.tool_frame import BaseToolFrame

class ToolRegistry:
    """Registry for tool classes and their categories"""
    
    CATEGORIES = {
        "Analysis": "Tools for analyzing data",
        "Data Cleaning": "Tools for cleaning and standardizing data",
        "Data Manipulation": "Tools for modifying data",
        "Data Formatting": "Tools for formatting output"
    }
    
    def __init__(self):
        self._tools: Dict[str, Dict] = {}  # Store tools by name
        self._categories: Dict[str, List[Type[BaseToolFrame]]] = {
            category: [] for category in self.CATEGORIES
        }
    
    def register_tool(self, tool_class: Type[BaseToolFrame], category: str, dependencies: List[str] = None):
        """Registers a tool class"""
        if category not in self.CATEGORIES:
            raise ValueError(f"Invalid category: {category}")
            
        tool_name = tool_class.get_tool_name()
        
        # Store tool info
        self._tools[tool_name] = {
            'class': tool_class,
            'category': category,
            'dependencies': dependencies or []
        }
        
        # Add to category
        self._categories[category].append(tool_class)
    
    def get_tool_class(self, tool_name: str) -> Optional[Type[BaseToolFrame]]:
        """Gets tool class by name"""
        tool_info = self._tools.get(tool_name)
        return tool_info['class'] if tool_info else None
    
    def get_tools(self, category: str) -> List[Type[BaseToolFrame]]:
        """Gets all tools in a category"""
        if category not in self.CATEGORIES:
            raise ValueError(f"Invalid category: {category}")
        return self._categories[category]
    
    def get_tool_category(self, tool_name: str) -> Optional[str]:
        """Gets category for a tool"""
        tool_info = self._tools.get(tool_name)
        return tool_info['category'] if tool_info else None
    
    def get_tool_dependencies(self, tool_name: str) -> List[str]:
        """Gets dependencies for a tool"""
        tool_info = self._tools.get(tool_name)
        return tool_info['dependencies'] if tool_info else []
    
    def check_dependencies(self, tool_name: str) -> tuple[bool, Optional[str]]:
        """Checks if tool dependencies are met"""
        tool_info = self._tools.get(tool_name)
        if not tool_info:
            return False, f"Tool not found: {tool_name}"
            
        dependencies = tool_info['dependencies']
        if not dependencies:
            return True, None
            
        # Check each dependency
        missing = []
        try:
            for dep in dependencies:
                try:
                    __import__(dep)
                except ImportError:
                    missing.append(dep)
                    
            if missing:
                return False, f"Missing dependencies: {', '.join(missing)}"
            return True, None
            
        except Exception as e:
            return False, f"Error checking dependencies: {str(e)}" 