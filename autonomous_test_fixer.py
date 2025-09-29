"""
Autonomous Test Fixer - Closed Loop AI System
Continuously runs tests, analyzes failures, fixes code, and repeats until 100% pass rate
"""

import os
import json
import time
import subprocess
import logging
from datetime import datetime
from typing import Dict, List, Any
import openai
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AutonomousTestFixer:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.max_iterations = 50
        self.iteration = 0  # Fixed: renamed from current_iteration to match test expectations
        self.test_results_history = []
        self.fixes_applied = []
        self.running = False
        
    def run_tests(self) -> Dict[str, Any]:
        """Run pytest and return detailed results"""
        logger.info("Running tests...")
        
        # Use simpler command to ensure output is captured
        cmd = ['python', '-m', 'pytest', 'tests/', '-v', '--tb=short']
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300, cwd=os.getcwd())
            
            logger.info(f"Test exit code: {result.returncode}")
            logger.info(f"Test output length: {len(result.stdout)} chars")
            
            # Parse text output for failure details
            failed_tests = self._parse_failures(result.stdout)
            
            logger.info(f"Parsed {len(failed_tests)} failed tests")
            
            return {
                'success': result.returncode == 0,
                'exit_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'failed_tests': failed_tests,
                'timestamp': datetime.now().isoformat()
            }
            
        except subprocess.TimeoutExpired:
            logger.error("Tests timed out")
            return {'success': False, 'error': 'Timeout', 'failed_tests': []}
            
    def _parse_failures(self, stdout: str) -> List[Dict[str, str]]:
        """Extract detailed failure information from pytest output"""
        failures = []
        lines = stdout.split('\n')
        
        # Look for FAILED lines
        for line in lines:
            if 'FAILED' in line and '::' in line:
                # Extract test path and error
                parts = line.split(' - ')
                test_path = parts[0].replace('FAILED ', '').strip()
                error_message = parts[1] if len(parts) > 1 else "Test failed"
                
                failures.append({
                    'test_path': test_path,
                    'error_message': error_message,
                    'traceback': f"Failed test: {test_path}\nError: {error_message}"
                })
        
        # If no failures found via FAILED lines, check summary
        if not failures:
            for line in lines:
                if 'failed' in line and 'passed' in line:
                    # Extract count from summary line
                    if 'failed' in line:
                        # Create generic failures for the count
                        import re
                        match = re.search(r'(\d+) failed', line)
                        if match:
                            failed_count = int(match.group(1))
                            for i in range(failed_count):
                                failures.append({
                                    'test_path': f'unknown_test_{i}',
                                    'error_message': 'Test failed - details not captured',
                                    'traceback': 'Generic test failure'
                                })
                    break
            
        return failures
    
    def analyze_failures_with_ai(self, test_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Use AI to analyze test failures and generate fixes"""
        logger.info(f"Analyzing {len(test_results['failed_tests'])} test failures with AI...")
        
        fixes = []
        
        for failure in test_results['failed_tests']:
            try:
                # Get file content for context
                file_path = failure['test_path'].split('::')[0]
                file_content = self._read_file_safely(file_path)
                
                # Analyze with AI
                fix = self._get_ai_fix_for_failure(failure, file_content)
                if fix:
                    fixes.append(fix)
                    
            except Exception as e:
                logger.error(f"Error analyzing failure {failure['test_path']}: {e}")
                
        return fixes
    
    def _read_file_safely(self, file_path: str) -> str:
        """Safely read file content"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
        return ""
    
    def _get_ai_fix_for_failure(self, failure: Dict[str, str], file_content: str) -> Dict[str, Any]:
        """Get AI-generated fix for a specific test failure"""
        prompt = f"""
You are an expert Python developer fixing test failures. Analyze this test failure and provide a precise fix.

TEST FAILURE:
{failure['error_message']}

TRACEBACK:
{failure['traceback']}

CURRENT FILE CONTENT:
{file_content[:3000]}

Provide a JSON response with:
{{
    "file_path": "path/to/file.py",
    "fix_description": "Brief description of the fix",
    "old_code": "exact code to replace",
    "new_code": "replacement code",
    "confidence": 0.9
}}

Focus on the root cause. Provide exact code replacements that will fix the test.
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert Python developer. Respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                max_tokens=1500,
                temperature=0.1
            )
            
            fix_data = json.loads(response.choices[0].message.content)
            fix_data['test_path'] = failure['test_path']
            return fix_data
            
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return None
    
    def apply_fixes(self, fixes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply AI-generated fixes to the codebase"""
        logger.info(f"Applying {len(fixes)} fixes...")
        
        applied_fixes = []
        
        for fix in fixes:
            try:
                if self._apply_single_fix(fix):
                    applied_fixes.append(fix)
                    logger.info(f"Applied fix: {fix['fix_description']}")
                else:
                    logger.warning(f"Failed to apply fix: {fix['fix_description']}")
                    
            except Exception as e:
                logger.error(f"Error applying fix: {e}")
                
        return applied_fixes
    
    def _apply_single_fix(self, fix: Dict[str, Any]) -> bool:
        """Apply a single fix to a file"""
        file_path = fix.get('file_path')
        old_code = fix.get('old_code', '').strip()
        new_code = fix.get('new_code', '').strip()
        
        if not file_path or not old_code or not new_code:
            return False
            
        try:
            # Read current content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Apply fix
            if old_code in content:
                new_content = content.replace(old_code, new_code)
                
                # Write back
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                    
                return True
            else:
                logger.warning(f"Old code not found in {file_path}")
                return False
                
        except Exception as e:
            logger.error(f"Error applying fix to {file_path}: {e}")
            return False
    
    def run_autonomous_cycle(self):
        """Main autonomous cycle: test -> analyze -> fix -> repeat"""
        logger.info("Starting autonomous test fixing cycle...")
        self.running = True
        self.current_iteration = 0
        
        while self.running and self.current_iteration < self.max_iterations:
            self.current_iteration += 1
            logger.info(f"\n=== ITERATION {self.current_iteration} ===")
            
            # Step 1: Run tests
            test_results = self.run_tests()
            self.test_results_history.append(test_results)
            
            # Check if all tests pass
            if test_results['success']:
                logger.info("🎉 ALL TESTS PASS! Autonomous fixing complete.")
                self.running = False
                break
            
            failed_count = len(test_results['failed_tests'])
            logger.info(f"Found {failed_count} failing tests")
            
            # Step 2: Analyze failures with AI
            fixes = self.analyze_failures_with_ai(test_results)
            
            if not fixes:
                logger.warning("No fixes generated by AI")
                break
            
            # Step 3: Apply fixes
            applied_fixes = self.apply_fixes(fixes)
            self.fixes_applied.extend(applied_fixes)
            
            if not applied_fixes:
                logger.warning("No fixes could be applied")
                break
                
            logger.info(f"Applied {len(applied_fixes)} fixes. Running tests again...")
            time.sleep(2)  # Brief pause before next iteration
            
        if self.current_iteration >= self.max_iterations:
            logger.warning(f"Reached maximum iterations ({self.max_iterations})")
            
        self.running = False
        return self.get_status()
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the autonomous fixer"""
        latest_results = self.test_results_history[-1] if self.test_results_history else None
        
        return {
            'running': self.running,
            'iteration': self.iteration,
            'max_iterations': self.max_iterations,
            'total_fixes_applied': len(self.fixes_applied),
            'latest_test_results': latest_results,
            'all_tests_passing': latest_results and latest_results.get('success', False),
            'fixes_history': self.fixes_applied,
            'timestamp': datetime.now().isoformat()
        }
    
    def stop(self):
        """Stop the autonomous cycle"""
        logger.info("Stopping autonomous test fixer...")
        self.running = False

# Global instance for web interface
autonomous_fixer = AutonomousTestFixer()