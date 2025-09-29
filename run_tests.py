#!/usr/bin/env python3
"""
Quick test runner script for YouTube Course Generator
Provides command-line access to run tests with various options
"""

import subprocess
import sys
import os
import json
from datetime import datetime

def run_tests(coverage=True, verbose=True, specific_test=None):
    """Run pytest tests with specified options"""
    cmd = ['python', '-m', 'pytest']
    
    if specific_test:
        cmd.append(specific_test)
    else:
        cmd.append('tests/')
    
    if verbose:
        cmd.append('-v')
    
    if coverage:
        cmd.extend(['--cov=.', '--cov-report=term-missing', '--cov-report=html'])
    
    # Add other useful options
    cmd.extend(['--tb=short', '--durations=10'])
    
    print(f"Running command: {' '.join(cmd)}")
    print("-" * 60)
    
    start_time = datetime.now()
    result = subprocess.run(cmd, cwd=os.getcwd())
    end_time = datetime.now()
    
    duration = (end_time - start_time).total_seconds()
    
    print("-" * 60)
    print(f"Tests completed in {duration:.2f} seconds")
    print(f"Exit code: {result.returncode}")
    
    if result.returncode == 0:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    
    return result.returncode

def main():
    """Main function with command line argument parsing"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run tests for YouTube Course Generator')
    parser.add_argument('--no-coverage', action='store_true', help='Skip coverage report')
    parser.add_argument('--quiet', action='store_true', help='Reduce verbosity')
    parser.add_argument('--test', type=str, help='Run specific test file or function')
    parser.add_argument('--unit', action='store_true', help='Run only unit tests')
    parser.add_argument('--integration', action='store_true', help='Run only integration tests')
    
    args = parser.parse_args()
    
    coverage = not args.no_coverage
    verbose = not args.quiet
    
    specific_test = None
    if args.test:
        specific_test = args.test
    elif args.unit:
        specific_test = 'tests/test_utils.py tests/test_services.py'
    elif args.integration:
        specific_test = 'tests/test_app.py'
    
    return run_tests(coverage=coverage, verbose=verbose, specific_test=specific_test)

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)