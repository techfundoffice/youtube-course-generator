#!/usr/bin/env python3
"""
Test Runner Service for YouTube Course Generator
Provides a web interface to run and monitor pytest tests
"""

import subprocess
import json
import os
import time
from datetime import datetime
from flask import Flask, render_template, jsonify, request
import threading
import queue

app = Flask(__name__)

class TestRunner:
    def __init__(self):
        self.test_queue = queue.Queue()
        self.results = {}
        self.running = False
        
    def run_tests(self, test_path=None, coverage=True, verbose=True):
        """Run pytest tests with specified options"""
        cmd = ['python', '-m', 'pytest']
        
        if test_path:
            cmd.append(test_path)
        
        if coverage:
            cmd.extend(['--cov=.', '--cov-report=json', '--cov-report=term'])
        
        if verbose:
            cmd.append('-v')
        
        cmd.extend(['--json-report', '--json-report-file=test_results.json'])
        
        try:
            self.running = True
            start_time = time.time()
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Parse test results
            test_results = self._parse_results(result, duration)
            
            self.running = False
            return test_results
            
        except Exception as e:
            self.running = False
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _parse_results(self, result, duration):
        """Parse pytest results"""
        try:
            # Try to read JSON report
            if os.path.exists('test_results.json'):
                with open('test_results.json', 'r') as f:
                    json_data = json.load(f)
                
                return {
                    'success': result.returncode == 0,
                    'exit_code': result.returncode,
                    'duration': duration,
                    'summary': json_data.get('summary', {}),
                    'tests': json_data.get('tests', []),
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'timestamp': datetime.now().isoformat(),
                    'coverage': self._get_coverage_data()
                }
        except Exception as e:
            pass
        
        # Fallback to basic parsing
        return {
            'success': result.returncode == 0,
            'exit_code': result.returncode,
            'duration': duration,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'timestamp': datetime.now().isoformat(),
            'summary': self._parse_text_output(result.stdout)
        }
    
    def _get_coverage_data(self):
        """Get coverage data from JSON report"""
        try:
            if os.path.exists('coverage.json'):
                with open('coverage.json', 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return None
    
    def _parse_text_output(self, stdout):
        """Parse text output for basic summary"""
        lines = stdout.split('\n')
        summary = {'passed': 0, 'failed': 0, 'total': 0}
        
        for line in lines:
            if 'failed' in line and 'passed' in line:
                # Parse line like "17 failed, 29 passed in 4.71s"
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == 'failed' and i > 0:
                        try:
                            summary['failed'] = int(parts[i-1])
                        except (ValueError, IndexError):
                            pass
                    elif part == 'passed' and i > 0:
                        try:
                            summary['passed'] = int(parts[i-1])
                        except (ValueError, IndexError):
                            pass
                summary['total'] = summary['passed'] + summary['failed']
                break
            elif '== FAILURES ==' in line:
                # Tests have failures
                summary['failed'] = summary.get('failed', 1)
            elif 'passed' in line and 'in' in line and 's' in line:
                # Parse line like "29 passed in 4.71s"
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == 'passed' and i > 0:
                        try:
                            summary['passed'] = int(parts[i-1])
                            summary['total'] = summary['passed'] + summary['failed']
                        except (IndexError, ValueError):
                            pass
                        break
        
        return summary
    
    def get_test_files(self):
        """Get list of available test files including organized subdirectories"""
        test_files = []
        test_dir = 'tests'
        
        if os.path.exists(test_dir):
            # Get files in root tests directory
            for file in os.listdir(test_dir):
                if file.startswith('test_') and file.endswith('.py'):
                    test_files.append({'name': file, 'path': file, 'category': 'legacy'})
            
            # Get files in organized subdirectories
            for subdir in ['unit', 'integration', 'functional']:
                subdir_path = os.path.join(test_dir, subdir)
                if os.path.exists(subdir_path):
                    for file in os.listdir(subdir_path):
                        if file.startswith('test_') and file.endswith('.py'):
                            relative_path = f"{subdir}/{file}"
                            test_files.append({
                                'name': file,
                                'path': relative_path,
                                'category': subdir,
                                'display_name': f"{subdir.title()}: {file.replace('test_', '').replace('.py', '').replace('_', ' ').title()}"
                            })
        
        return sorted(test_files, key=lambda x: (x['category'], x['name']))
    
    def run_async(self, test_path=None, coverage=True, verbose=True):
        """Run tests asynchronously"""
        def run_in_thread():
            result = self.run_tests(test_path, coverage, verbose)
            self.test_queue.put(result)
        
        thread = threading.Thread(target=run_in_thread)
        thread.daemon = True
        thread.start()

# Global test runner instance
test_runner = TestRunner()

@app.route('/tests')
def test_dashboard():
    """Test dashboard page"""
    test_files = test_runner.get_test_files()
    return render_template('test_dashboard.html', test_files=test_files)

@app.route('/api/tests/run', methods=['POST'])
def run_tests_api():
    """Run tests via API"""
    data = request.get_json() or {}
    test_path = data.get('test_path')
    coverage = data.get('coverage', True)
    verbose = data.get('verbose', True)
    
    if test_runner.running:
        return jsonify({
            'success': False,
            'error': 'Tests are already running'
        }), 400
    
    # Run tests asynchronously
    test_runner.run_async(test_path, coverage, verbose)
    
    return jsonify({
        'success': True,
        'message': 'Tests started',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/tests/status')
def test_status():
    """Get test execution status"""
    try:
        # Check if tests completed
        if not test_runner.running and not test_runner.test_queue.empty():
            result = test_runner.test_queue.get_nowait()
            return jsonify(result)
        
        return jsonify({
            'running': test_runner.running,
            'timestamp': datetime.now().isoformat()
        })
        
    except queue.Empty:
        return jsonify({
            'running': test_runner.running,
            'timestamp': datetime.now().isoformat()
        })

@app.route('/api/tests/files')
def get_test_files():
    """Get available test files"""
    return jsonify({
        'test_files': test_runner.get_test_files()
    })

@app.route('/api/tests/files/detailed')
def get_detailed_test_files():
    """Get detailed test files information with enhanced metadata"""
    test_files = test_runner.get_test_files()
    
    # Enhance with additional metadata
    enhanced_files = []
    for file in test_files:
        enhanced_file = {
            **file,
            'description': get_test_description(file['name']),
            'estimated_duration': get_estimated_duration(file['name']),
            'dependencies': get_test_dependencies(file['name']),
            'last_run': get_last_run_status(file['name'])
        }
        enhanced_files.append(enhanced_file)
    
    return jsonify({
        'success': True,
        'test_files': enhanced_files,
        'categories': {
            'unit': [f for f in enhanced_files if f['category'] == 'unit'],
            'integration': [f for f in enhanced_files if f['category'] == 'integration'],
            'functional': [f for f in enhanced_files if f['category'] == 'functional'],
            'legacy': [f for f in enhanced_files if f['category'] == 'legacy']
        },
        'summary': {
            'total_files': len(enhanced_files),
            'by_category': {
                'unit': len([f for f in enhanced_files if f['category'] == 'unit']),
                'integration': len([f for f in enhanced_files if f['category'] == 'integration']),
                'functional': len([f for f in enhanced_files if f['category'] == 'functional']),
                'legacy': len([f for f in enhanced_files if f['category'] == 'legacy'])
            }
        }
    })

def get_test_description(filename):
    """Get human-readable description for test file"""
    descriptions = {
        'test_app.py': 'Core application routes and API endpoints',
        'test_services.py': 'Service layer components and integrations',
        'test_utils.py': 'Utility functions and helper methods',
        'test_validators.py': 'Input validation and sanitization functions',
        'test_app_routes.py': 'HTTP routes and endpoint testing',
        'test_course_generation.py': 'End-to-end course generation workflow',
        'test_autonomous_fixer.py': 'Self-healing test automation system'
    }
    return descriptions.get(filename, 'Test suite for application components')

def get_estimated_duration(filename):
    """Get estimated test duration in seconds"""
    durations = {
        'test_app.py': 15,
        'test_services.py': 25,
        'test_utils.py': 10,
        'test_validators.py': 5,
        'test_app_routes.py': 12,
        'test_course_generation.py': 30,
        'test_autonomous_fixer.py': 20
    }
    return durations.get(filename, 10)

def get_test_dependencies(filename):
    """Get test dependencies"""
    dependencies = {
        'test_app.py': ['database', 'flask_app'],
        'test_services.py': ['database', 'external_apis'],
        'test_utils.py': [],
        'test_validators.py': [],
        'test_app_routes.py': ['database', 'flask_app'],
        'test_course_generation.py': ['database', 'external_apis', 'ai_services'],
        'test_autonomous_fixer.py': ['database', 'ai_services']
    }
    return dependencies.get(filename, [])

def get_last_run_status(filename):
    """Get last run status for test file"""
    # This would typically come from a database or cache
    # For now, return a default structure
    return {
        'timestamp': None,
        'status': 'unknown',
        'duration': None,
        'passed': None,
        'failed': None
    }

@app.route('/api/tests/coverage')
def get_coverage():
    """Get latest coverage report"""
    coverage_data = test_runner._get_coverage_data()
    if coverage_data:
        return jsonify(coverage_data)
    else:
        return jsonify({'error': 'No coverage data available'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)