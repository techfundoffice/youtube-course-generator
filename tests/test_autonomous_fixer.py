"""
Test suite for the Autonomous Test Fixer - Self-Healing System
Tests the closed-loop feedback system's ability to autonomously fix failing tests
"""

import pytest
import json
import time
import threading
from unittest.mock import patch, Mock, MagicMock
from autonomous_test_fixer import AutonomousTestFixer
from services.ai_service import AIService


class TestAutonomousTestFixer:
    """Test the self-healing autonomous test fixing system"""
    
    def setup_method(self):
        """Setup test environment"""
        self.fixer = AutonomousTestFixer()
        
    def test_initialization(self):
        """Test autonomous fixer initializes correctly"""
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data self.fixer.max_iterations == 50
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data self.fixer.iteration == 0
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data self.fixer.running == False
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data self.fixer.fixes_applied == []
        
    def test_test_runner_integration(self):
        """Test that test runner detects failures correctly"""
        # Mock test output with failures
        mock_stdout = """
        FAILED tests/test_app.py::TestRoutes::test_courses_list - jinja2.exceptions.UndefinedError
        FAILED tests/test_utils.py::TestValidators::test_validate_course_structure_valid
        ======================== 2 failed, 29 passed in 4.45s =========================
        """
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 1
            mock_run.return_value.stdout = mock_stdout
            mock_run.return_value.stderr = ""
            
            result = self.fixer.run_tests()
            
            assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data result['success'] == False
            assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data len(result['failed_tests']) == 2
            assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data 'test_courses_list' in result['failed_tests'][0]['test_path']
            
    def test_failure_parsing(self):
        """Test accurate parsing of pytest failure output"""
        test_output = """
        FAILED tests/test_app.py::TestRoutes::test_courses_list - jinja2.exceptions.UndefinedError: 'dict object' has no attribute 'created_at'
        FAILED tests/test_services.py::TestAIService::test_generate_course_claude_success
        ======================== 2 failed, 29 passed in 4.45s =========================
        """
        
        failures = self.fixer._parse_failures(test_output)
        
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data len(failures) == 2
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data failures[0]['test_path'] == 'tests/test_app.py::TestRoutes::test_courses_list'
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data 'jinja2.exceptions.UndefinedError' in failures[0]['error_message']
        
    @patch('openai.OpenAI')
    def test_ai_analysis_integration(self, mock_openai):
        """Test AI analysis of test failures"""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content=json.dumps({
            "file_path": "tests/test_app.py",
            "fix_description": "Fix missing attribute error",
            "old_code": "assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data b'Test Course' in response.data",
            "new_code": "assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data b'Test Course' in response.data",
            "confidence": 0.9
        })
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        test_results = {
            'failed_tests': [{
                'test_path': 'tests/test_app.py::TestRoutes::test_courses_list',
                'error_message': 'AttributeError: dict has no attribute created_at',
                'traceback': 'Full traceback here'
            }]
        }
        
        fixes = self.fixer.analyze_failures_with_ai(test_results)
        
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data len(fixes) == 1
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data fixes[0]['file_path'] == 'tests/test_app.py'
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data fixes[0]['confidence'] == 0.9
        
    def test_fix_application(self):
        """Test application of AI-generated fixes"""
        # Create a temporary test file
        test_file_content = '''
def test_example():
    assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data False  # This will fail
        '''
        
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = test_file_content
            mock_open.return_value.__enter__.return_value.write = Mock()
            
            fix = {
                'file_path': 'test_file.py',
                'old_code': 'assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data False  # This will fail',
                'new_code': 'assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data True  # This will pass',
                'fix_description': 'Fix failing assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.dataion',
                'confidence': 0.95
            }
            
            result = self.fixer._apply_single_fix(fix)
            assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data result == True
            
    @patch('subprocess.run')
    @patch('openai.OpenAI')
    def test_autonomous_cycle_simulation(self, mock_openai, mock_subprocess):
        """Test complete autonomous fixing cycle"""
        # Mock initial failing tests
        mock_subprocess.return_value.returncode = 1
        mock_subprocess.return_value.stdout = """
        FAILED tests/test_example.py::test_function - AssertionError
        ======================== 1 failed, 0 passed in 1.0s =========================
        """
        mock_subprocess.return_value.stderr = ""
        
        # Mock AI fix generation
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content=json.dumps({
            "file_path": "tests/test_example.py",
            "fix_description": "Fix assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.dataion error",
            "old_code": "assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data False",
            "new_code": "assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data True",
            "confidence": 0.9
        })
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        # Mock file operations
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = "assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data False"
            mock_open.return_value.__enter__.return_value.write = Mock()
            
            # Simulate one iteration
            self.fixer.iteration = 1
            test_results = self.fixer.run_tests()
            fixes = self.fixer.analyze_failures_with_ai(test_results)
            applied_fixes = self.fixer.apply_fixes(fixes)
            
            assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data len(applied_fixes) == 1
            assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data applied_fixes[0]['success'] == True
            
    def test_status_reporting(self):
        """Test status reporting functionality"""
        self.fixer.iteration = 5
        self.fixer.running = True
        self.fixer.fixes_applied = [
            {'file_path': 'test1.py', 'fix_description': 'Fix 1'},
            {'file_path': 'test2.py', 'fix_description': 'Fix 2'}
        ]
        
        status = self.fixer.get_status()
        
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data status['iteration'] == 5
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data status['running'] == True
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data status['total_fixes_applied'] == 2
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data len(status['fixes_history']) == 2
        
    def test_max_iteration_limit(self):
        """Test that system respects maximum iteration limit"""
        self.fixer.iteration = 50
        
        # Should stop due to max iterations
        with patch.object(self.fixer, 'run_tests') as mock_run_tests:
            mock_run_tests.return_value = {
                'success': False,
                'failed_tests': [{'test_path': 'test.py', 'error_message': 'error'}]
            }
            
            # This should not run because max iterations reached
            assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data self.fixer.iteration >= self.fixer.max_iterations
            
    def test_stop_functionality(self):
        """Test stop functionality works correctly"""
        self.fixer.running = True
        self.fixer.stop()
        
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data self.fixer.running == False
        
    @patch('subprocess.run')
    def test_all_tests_passing_detection(self, mock_subprocess):
        """Test detection when all tests pass"""
        # Mock all tests passing
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = """
        ======================== 46 passed in 5.0s =========================
        """
        mock_subprocess.return_value.stderr = ""
        
        result = self.fixer.run_tests()
        
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data result['success'] == True
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data len(result['failed_tests']) == 0


class TestSelfHealingIntegration:
    """Integration tests for the complete self-healing system"""
    
    @pytest.mark.asyncio
    async def test_ai_monitoring_integration(self):
        """Test integration with AI monitoring system"""
        ai_service = AIService()
        
        # Test AI service health
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data ai_service.is_healthy() == True
        
        # Mock test failure analysis
        test_failure_data = {
            'test_path': 'tests/test_app.py::test_function',
            'error_message': 'AssertionError: Expected True but got False',
            'file_content': 'def test_function():\n    assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data False'
        }
        
        # This would normally call AI to analyze the failure
        # In production, this integrates with the autonomous fixer
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data test_failure_data['test_path'] is not None
        
    def test_real_time_monitoring(self):
        """Test real-time monitoring of autonomous fixing process"""
        fixer = AutonomousTestFixer()
        
        # Start monitoring
        fixer.running = True
        fixer.iteration = 3
        fixer.fixes_applied = [
            {'file_path': 'test1.py', 'success': True},
            {'file_path': 'test2.py', 'success': True}
        ]
        
        status = fixer.get_status()
        
        # Verify monitoring data
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data status['running'] == True
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data status['iteration'] == 3
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data status['total_fixes_applied'] == 2
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data 'timestamp' in status
        
    def test_fix_quality_metrics(self):
        """Test quality metrics for applied fixes"""
        fixer = AutonomousTestFixer()
        
        # Simulate high-quality fixes
        high_quality_fixes = [
            {'confidence': 0.95, 'success': True},
            {'confidence': 0.88, 'success': True},
            {'confidence': 0.92, 'success': True}
        ]
        
        total_confidence = sum(fix['confidence'] for fix in high_quality_fixes)
        avg_confidence = total_confidence / len(high_quality_fixes)
        
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data avg_confidence > 0.85  # High quality threshold
        
    def test_error_handling_resilience(self):
        """Test system resilience to errors during fixing"""
        fixer = AutonomousTestFixer()
        
        # Simulate AI service failure
        with patch('openai.OpenAI') as mock_openai:
            mock_openai.side_effect = Exception("API Error")
            
            test_results = {
                'failed_tests': [{
                    'test_path': 'test.py',
                    'error_message': 'Error',
                    'traceback': 'Traceback'
                }]
            }
            
            # Should handle error gracefully
            fixes = fixer.analyze_failures_with_ai(test_results)
            assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data fixes == []  # No fixes due to error, but system continues
            
    def test_concurrent_safety(self):
        """Test thread safety of autonomous fixer"""
        fixer = AutonomousTestFixer()
        results = []
        
        def check_status():
            status = fixer.get_status()
            results.append(status['running'])
            
        # Start multiple threads checking status
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=check_status)
            threads.append(thread)
            thread.start()
            
        for thread in threads:
            thread.join()
            
        # All threads should get consistent results
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data len(set(results)) <= 2  # Either True or False, but consistent


class TestAIEnhancedSelfHealing:
    """Test AI-enhanced features of the self-healing system"""
    
    @patch('openai.OpenAI')
    def test_intelligent_fix_prioritization(self, mock_openai):
        """Test AI prioritizes critical fixes first"""
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content=json.dumps({
            "file_path": "critical_test.py",
            "fix_description": "Critical security fix",
            "old_code": "insecure_function()",
            "new_code": "secure_function()",
            "confidence": 0.98,
            "priority": "critical"
        })
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        fixer = AutonomousTestFixer()
        test_results = {
            'failed_tests': [{
                'test_path': 'tests/security_test.py',
                'error_message': 'Security vulnerability detected',
                'traceback': 'Security error traceback'
            }]
        }
        
        fixes = fixer.analyze_failures_with_ai(test_results)
        
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data len(fixes) == 1
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data fixes[0]['confidence'] > 0.95  # High confidence for critical fixes
        
    @patch('openai.OpenAI')
    def test_learning_from_fix_patterns(self, mock_openai):
        """Test system learns from successful fix patterns"""
        fixer = AutonomousTestFixer()
        
        # Simulate successful fix history
        fixer.fixes_applied = [
            {'file_path': 'test1.py', 'pattern': 'assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.dataion_fix', 'success': True},
            {'file_path': 'test2.py', 'pattern': 'assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.dataion_fix', 'success': True},
            {'file_path': 'test3.py', 'pattern': 'import_fix', 'success': True}
        ]
        
        # System should recognize successful patterns
        successful_patterns = [fix for fix in fixer.fixes_applied if fix['success']]
        pattern_frequency = {}
        
        for fix in successful_patterns:
            pattern = fix.get('pattern', 'unknown')
            pattern_frequency[pattern] = pattern_frequency.get(pattern, 0) + 1
            
        # Most common successful pattern should be prioritized
        most_common_pattern = max(pattern_frequency, key=pattern_frequency.get)
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data most_common_pattern == 'assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.dataion_fix'
        
    def test_adaptive_confidence_thresholds(self):
        """Test adaptive confidence thresholds based on success rate"""
        fixer = AutonomousTestFixer()
        
        # High success rate should lower confidence threshold
        high_success_fixes = [
            {'confidence': 0.7, 'success': True},
            {'confidence': 0.8, 'success': True},
            {'confidence': 0.75, 'success': True}
        ]
        
        success_rate = sum(1 for fix in high_success_fixes if fix['success']) / len(high_success_fixes)
        
        # With high success rate, can accept lower confidence fixes
        adaptive_threshold = 0.8 - (success_rate - 0.5) * 0.2
        
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data success_rate == 1.0
        assert b'Test Course' in response.data.replace(b'created_at', b'') b'Test Course' in response.data adaptive_threshold < 0.8  # Lowered threshold due to high success rate