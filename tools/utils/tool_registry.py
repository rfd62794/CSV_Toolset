from typing import Dict, Type, List, Set, Tuple, Optional
from ..base.tool_frame import BaseToolFrame
import json
from pathlib import Path

class ToolRegistry:
    """Registry for available tools"""
    
    CATEGORIES = {
        "Analysis": "Tools for analyzing CSV data",
        "Data Cleaning": "Tools for cleaning and validating data",
        "Data Manipulation": "Tools for manipulating data structure",
        "Data Transformation": "Tools for transforming data content",
        "Data Validation": "Tools for validating data quality",
        "Data Export": "Tools for exporting to different formats",
        "Data Import": "Tools for importing from different sources",
        "Data Visualization": "Tools for visualizing data",
        "Text Processing": "Tools for text manipulation",
        "Statistical Analysis": "Tools for statistical calculations",
        "Data Quality": "Tools for assessing data quality",
        "Data Integration": "Tools for combining data sources",
        "Data Extraction": "Tools for extracting specific data",
        "Data Formatting": "Tools for formatting data",
        "Utilities": "General utility tools"
    }
    
    def __init__(self):
        self._tools = {
            category: [] for category in self.CATEGORIES
        }
        self._dependencies = {}  # Tool -> Required tools
        self._configurations = {}  # Tool -> Config
        self.config_file = Path(__file__).parent.parent / 'config' / 'tool_config.json'
        self.load_configurations()
    
    def register_tool(self, tool_class: Type[BaseToolFrame], category: str, 
                     dependencies: List[str] = None):
        """Registers a tool in a category with optional dependencies"""
        if category not in self.CATEGORIES:
            raise ValueError(f"Invalid category: {category}")
        
        tool_name = tool_class.get_tool_name()
        if tool_class not in self._tools[category]:
            self._tools[category].append(tool_class)
            
        if dependencies:
            self._dependencies[tool_name] = set(dependencies)
    
    def get_tools(self, category: str = None) -> list:
        """Gets registered tools, optionally filtered by category"""
        if category:
            if category not in self.CATEGORIES:
                raise ValueError(f"Invalid category: {category}")
            return self._tools[category]
        
        all_tools = []
        for tools in self._tools.values():
            all_tools.extend(tools)
        return all_tools
    
    def check_dependencies(self, tool_name: str) -> Tuple[bool, Optional[str]]:
        """Checks if tool dependencies are satisfied"""
        if tool_name not in self._dependencies:
            return True, None
            
        missing = []
        for dep in self._dependencies[tool_name]:
            if not any(t.get_tool_name() == dep for t in self.get_tools()):
                missing.append(dep)
        
        if missing:
            return False, f"Required tools not available: {', '.join(missing)}"
        return True, None
    
    def get_dependent_tools(self, tool_name: str) -> List[str]:
        """Gets tools that depend on the given tool"""
        dependent = []
        for tool, deps in self._dependencies.items():
            if tool_name in deps:
                dependent.append(tool)
        return dependent
    
    def save_tool_config(self, tool_name: str, config: dict):
        """Saves tool configuration"""
        self._configurations[tool_name] = config
        self.save_configurations()
    
    def get_tool_config(self, tool_name: str) -> dict:
        """Gets tool configuration"""
        return self._configurations.get(tool_name, {})
    
    def load_configurations(self):
        """Loads tool configurations from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    self._configurations = json.load(f)
        except Exception as e:
            print(f"Error loading tool configurations: {e}")
            self._configurations = {}
    
    def save_configurations(self):
        """Saves tool configurations to file"""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self._configurations, f, indent=4)
        except Exception as e:
            print(f"Error saving tool configurations: {e}") 