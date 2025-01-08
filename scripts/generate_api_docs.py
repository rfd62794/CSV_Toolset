#!/usr/bin/env python3
"""Generate API documentation from source code."""

import os
import sys
from pathlib import Path
import inspect
import importlib
import pkgutil
from docstring_parser import parse
import csv_toolset

def get_module_docstring(module):
    """Get module's docstring."""
    return inspect.getdoc(module) or ""

def get_class_docstring(cls):
    """Get class's docstring."""
    return inspect.getdoc(cls) or ""

def get_function_docstring(func):
    """Get function's docstring."""
    return inspect.getdoc(func) or ""

def generate_module_doc(module, level=1):
    """Generate documentation for a module."""
    doc = []
    module_name = module.__name__.split('.')[-1]
    doc.append(f"{'#' * level} {module_name.replace('_', ' ').title()}\n")
    
    # Add module docstring
    docstring = get_module_docstring(module)
    if docstring:
        doc.append(f"{docstring}\n")
    
    # Document classes
    classes = inspect.getmembers(module, inspect.isclass)
    if classes:
        doc.append(f"{'#' * (level + 1)} Classes\n")
        for name, cls in classes:
            if cls.__module__ == module.__name__:
                doc.append(f"### {name}\n")
                doc.append(f"{get_class_docstring(cls)}\n")
                
                # Document methods
                methods = inspect.getmembers(cls, inspect.isfunction)
                if methods:
                    doc.append("#### Methods\n")
                    for method_name, method in methods:
                        if not method_name.startswith('_'):
                            doc.append(f"##### `{method_name}`\n")
                            doc.append(f"{get_function_docstring(method)}\n")
    
    # Document functions
    functions = inspect.getmembers(module, inspect.isfunction)
    if functions:
        doc.append(f"{'#' * (level + 1)} Functions\n")
        for name, func in functions:
            if func.__module__ == module.__name__ and not name.startswith('_'):
                doc.append(f"### {name}\n")
                doc.append(f"{get_function_docstring(func)}\n")
    
    return '\n'.join(doc)

def generate_package_docs(package, output_dir: Path):
    """Generate documentation for a package and its submodules."""
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate main package documentation
    main_doc = generate_module_doc(package)
    with open(output_dir / 'index.md', 'w') as f:
        f.write(main_doc)
    
    # Generate documentation for submodules
    for _, name, ispkg in pkgutil.iter_modules(package.__path__):
        full_name = f"{package.__name__}.{name}"
        try:
            module = importlib.import_module(full_name)
            doc = generate_module_doc(module)
            
            # Create subdirectory for subpackages
            if ispkg:
                subdir = output_dir / name
                subdir.mkdir(exist_ok=True)
                with open(subdir / 'index.md', 'w') as f:
                    f.write(doc)
            else:
                with open(output_dir / f'{name}.md', 'w') as f:
                    f.write(doc)
                    
        except Exception as e:
            print(f"Error processing module {full_name}: {e}", file=sys.stderr)

def main():
    """Main function to generate API documentation."""
    try:
        # Set up paths
        docs_dir = Path('docs/api')
        docs_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate documentation for main package and submodules
        generate_package_docs(csv_toolset, docs_dir)
        
        print("API documentation generated successfully!")
        
    except Exception as e:
        print(f"Error generating API documentation: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 