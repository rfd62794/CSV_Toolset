import pytest
import sys
import argparse
from pathlib import Path
from typing import List, Optional

def parse_args():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Run CSV Toolkit tests')
    
    parser.add_argument(
        '-t', '--test-path',
        help='Path to specific test file or directory'
    )
    
    parser.add_argument(
        '-k', '--keyword',
        help='Only run tests matching given keyword expression'
    )
    
    parser.add_argument(
        '-m', '--marker',
        help='Only run tests matching given marker expression'
    )
    
    parser.add_argument(
        '--unit',
        action='store_true',
        help='Run only unit tests'
    )
    
    parser.add_argument(
        '--integration',
        action='store_true',
        help='Run only integration tests'
    )
    
    parser.add_argument(
        '--performance',
        action='store_true',
        help='Run only performance tests'
    )
    
    return parser.parse_args()

def run_tests(
    test_path: Optional[str] = None,
    keyword: Optional[str] = None,
    marker: Optional[str] = None,
    test_types: List[str] = None
) -> int:
    """
    Runs the test suite
    
    Args:
        test_path: Optional path to specific test file or directory
        keyword: Optional keyword expression to filter tests
        marker: Optional marker expression to filter tests
        test_types: Optional list of test types to run
    """
    args = [
        '-v',  # verbose output
        '--tb=short',  # shorter traceback format
        '--capture=no'  # show print statements
    ]
    
    if keyword:
        args.extend(['-k', keyword])
    
    if marker:
        args.extend(['-m', marker])
    
    if test_types:
        markers = ' or '.join(test_types)
        args.extend(['-m', markers])
    
    if test_path:
        args.append(test_path)
    else:
        args.append(str(Path(__file__).parent))
    
    return pytest.main(args)

if __name__ == '__main__':
    args = parse_args()
    
    test_types = []
    if args.unit:
        test_types.append('unit')
    if args.integration:
        test_types.append('integration')
    if args.performance:
        test_types.append('performance')
    
    sys.exit(run_tests(
        test_path=args.test_path,
        keyword=args.keyword,
        marker=args.marker,
        test_types=test_types
    )) 