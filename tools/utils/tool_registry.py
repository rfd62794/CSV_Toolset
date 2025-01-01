from typing import Dict, Type, List, Set, Tuple, Optional
from ..base.tool_frame import BaseToolFrame

class ToolRegistry:
    """Manages tool registration and dependencies"""
    
    def __init__(self):
        self._tools: Dict[str, Type[BaseToolFrame]] = {}
        self._categories: Dict[str, List[str]] = {}
        self._dependencies: Dict[str, Set[str]] = {}
    
    def register_tool(self, tool_class: Type[BaseToolFrame], 
                     category: str = "General",
                     dependencies: List[str] = None) -> None:
        """
        Registers a tool with category and dependencies
        
        Args:
            tool_class: Tool frame class
            category: Tool category
            dependencies: List of required module names
        """
        tool_name = tool_class.get_tool_name(None)
        self._tools[tool_name] = tool_class
        
        # Add to category
        if category not in self._categories:
            self._categories[category] = []
        self._categories[category].append(tool_name)
        
        # Store dependencies
        if dependencies:
            self._dependencies[tool_name] = set(dependencies)
    
    def get_tool_class(self, tool_name: str) -> Type[BaseToolFrame]:
        """Gets tool class by name"""
        return self._tools.get(tool_name)
    
    def get_categories(self) -> Dict[str, List[str]]:
        """Gets all categories and their tools"""
        return self._categories
    
    def check_dependencies(self, tool_name: str) -> Tuple[bool, Optional[str]]:
        """
        Checks if tool dependencies are available
        
        Returns:
            tuple: (dependencies_met, error_message)
        """
        if tool_name not in self._dependencies:
            return True, None
            
        missing = []
        for module in self._dependencies[tool_name]:
            try:
                __import__(module)
            except ImportError:
                missing.append(module)
        
        if missing:
            return False, f"Missing dependencies: {', '.join(missing)}"
        return True, None 