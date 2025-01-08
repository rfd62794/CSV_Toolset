#!/usr/bin/env python3
"""Development environment setup script for CSV Toolset."""

import os
import platform
import subprocess
import sys
from pathlib import Path

def check_python_version():
    """Check if Python version meets requirements."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)

def create_virtual_env():
    """Create and activate virtual environment."""
    venv_path = Path("venv")
    if not venv_path.exists():
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
    
    if platform.system() == "Windows":
        activate_script = venv_path / "Scripts" / "activate.bat"
        pip_path = venv_path / "Scripts" / "pip.exe"
    else:
        activate_script = venv_path / "bin" / "activate"
        pip_path = venv_path / "bin" / "pip"
    
    return str(activate_script), str(pip_path)

def install_dependencies(pip_path):
    """Install project dependencies."""
    subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)
    subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
    subprocess.run([pip_path, "install", "-r", "requirements-dev.txt"], check=True)

def setup_pre_commit():
    """Initialize pre-commit hooks."""
    subprocess.run(["pre-commit", "install"], check=True)
    subprocess.run(["pre-commit", "autoupdate"], check=True)

def create_git_hooks():
    """Create custom git hooks."""
    hooks_dir = Path(".git") / "hooks"
    hooks_dir.mkdir(exist_ok=True)
    
    # Create pre-push hook for running tests
    pre_push = hooks_dir / "pre-push"
    with open(pre_push, "w") as f:
        f.write("""#!/bin/sh
echo "Running tests before push..."
python -m pytest
""")
    
    # Make hook executable on Unix systems
    if platform.system() != "Windows":
        os.chmod(pre_push, 0o755)

def main():
    """Main setup function."""
    try:
        print("Setting up development environment...")
        
        # Check Python version
        check_python_version()
        print("✓ Python version check passed")
        
        # Create virtual environment
        activate_script, pip_path = create_virtual_env()
        print("✓ Virtual environment created")
        
        # Install dependencies
        install_dependencies(pip_path)
        print("✓ Dependencies installed")
        
        # Set up pre-commit
        setup_pre_commit()
        print("✓ Pre-commit hooks installed")
        
        # Create git hooks
        create_git_hooks()
        print("✓ Git hooks created")
        
        print("\nSetup complete! To activate the virtual environment:")
        if platform.system() == "Windows":
            print(f"    {activate_script}")
        else:
            print(f"    source {activate_script}")
            
    except subprocess.CalledProcessError as e:
        print(f"Error during setup: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 