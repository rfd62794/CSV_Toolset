import pytest
import sys
from pathlib import Path

def run_tests(test_path: str = None):
    """
    Runs the test suite
    
    Args:
        test_path: Optional path to specific test file or directory
    """
    args = [
        '-v',  # verbose output
        '--tb=short',  # shorter traceback format
        '--capture=no'  # show print statements
    ]
    
    if test_path:
        args.append(test_path)
    else:
        # Run all tests in the tests directory
        args.append(str(Path(__file__).parent))
    
    return pytest.main(args)

if __name__ == '__main__':
    test_path = sys.argv[1] if len(sys.argv) > 1 else None
    sys.exit(run_tests(test_path)) 