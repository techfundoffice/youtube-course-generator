"""
AI-Powered Self-Healing Monitor
Monitors the autonomous test fixer and provides intelligent analysis of its performance
"""

import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from openai import OpenAI
import os

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user

logger = logging.getLogger(__name__)

class SelfHealingMonitor:
    """AI-powered monitor for the autonomous test fixing system"""
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        self.monitoring_history = []
        self.performance_metrics = {
            'total_cycles': 0,
            'successful_cycles': 0,
            'total_fixes_applied': 0,
            'average_cycle_time': 0.0,
            'fix_success_rate': 0.0,
            'ai_confidence_avg': 0.0
        }
        
    def start_monitoring(self, fixer_instance):
        """Start monitoring an autonomous fixer instance"""
        logger.info("Starting AI-powered monitoring of self-healing system")
        
        monitoring_session = {
            'session_id': f"monitor_{int(time.time())}",
            'start_time': datetime.now(),
            'fixer_status': fixer_instance.get_status(),
            'initial_test_count': self._count_failing_tests(fixer_instance),
            'cycles': []
        }
        
        self.monitoring_history.append(monitoring_session)
        return monitoring_session['session_id']
        
    def monitor_cycle(self, fixer_instance, cycle_data: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor a single fixing cycle and analyze performance"""
        cycle_start = time.time()
        
        # Capture cycle metrics
        cycle_metrics = {
            'cycle_number': cycle_data.get('iteration', 0),
            'start_time': datetime.now(),
            'tests_analyzed': len(cycle_data.get('failed_tests', [])),
            'fixes_generated': len(cycle_data.get('fixes', [])),
            'fixes_applied': 0,
            'ai_responses': [],
            'success_rate': 0.0
        }
        
        # Monitor fix application
        if 'fixes' in cycle_data:
            for fix in cycle_data['fixes']:
                fix_result = self._monitor_fix_application(fix)
                cycle_metrics['ai_responses'].append(fix_result)
                if fix_result.get('applied_successfully', False):
                    cycle_metrics['fixes_applied'] += 1
                    
        cycle_metrics['success_rate'] = (
            cycle_metrics['fixes_applied'] / max(1, cycle_metrics['fixes_generated'])
        )
        
        cycle_metrics['duration'] = time.time() - cycle_start
        
        # AI analysis of cycle performance
        ai_analysis = self._analyze_cycle_with_ai(cycle_metrics, fixer_instance.get_status())
        cycle_metrics['ai_analysis'] = ai_analysis
        
        # Update performance metrics
        self._update_performance_metrics(cycle_metrics)
        
        return cycle_metrics
        
    def _monitor_fix_application(self, fix: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor the application of a single fix"""
        fix_result = {
            'file_path': fix.get('file_path', 'unknown'),
            'confidence': fix.get('confidence', 0.0),
            'fix_description': fix.get('fix_description', ''),
            'applied_successfully': False,
            'error_message': None,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # In a real implementation, this would monitor actual file changes
            # For now, we simulate based on confidence threshold
            if fix.get('confidence', 0) > 0.7:
                fix_result['applied_successfully'] = True
            else:
                fix_result['error_message'] = "Low confidence fix rejected"
                
        except Exception as e:
            fix_result['error_message'] = str(e)
            logger.error(f"Error monitoring fix application: {e}")
            
        return fix_result
        
    def _analyze_cycle_with_ai(self, cycle_metrics: Dict[str, Any], fixer_status: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to analyze cycle performance and provide recommendations"""
        try:
            analysis_prompt = f"""
            Analyze this autonomous test fixing cycle and provide insights:
            
            Cycle Metrics:
            - Cycle Number: {cycle_metrics['cycle_number']}
            - Tests Analyzed: {cycle_metrics['tests_analyzed']}
            - Fixes Generated: {cycle_metrics['fixes_generated']} 
            - Fixes Applied: {cycle_metrics['fixes_applied']}
            - Success Rate: {cycle_metrics['success_rate']:.2%}
            - Duration: {cycle_metrics['duration']:.2f} seconds
            
            Fixer Status:
            - Total Iterations: {fixer_status.get('iteration', 0)}
            - Running: {fixer_status.get('running', False)}
            - All Tests Passing: {fixer_status.get('all_tests_passing', False)}
            
            Provide analysis in JSON format:
            {{
                "performance_assessment": "excellent|good|fair|poor",
                "key_insights": ["insight1", "insight2"],
                "recommendations": ["recommendation1", "recommendation2"],
                "predicted_completion": "estimated_cycles_remaining",
                "risk_factors": ["risk1", "risk2"],
                "confidence_in_success": 0.85
            }}
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": analysis_prompt}],
                response_format={"type": "json_object"},
                max_tokens=800,
                temperature=0.1
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return {
                "performance_assessment": "unknown",
                "key_insights": ["AI analysis unavailable"],
                "recommendations": ["Continue monitoring"],
                "predicted_completion": "unknown",
                "risk_factors": ["Analysis system error"],
                "confidence_in_success": 0.5
            }
            
    def _count_failing_tests(self, fixer_instance) -> int:
        """Count current failing tests"""
        try:
            test_results = fixer_instance.run_tests()
            return len(test_results.get('failed_tests', []))
        except:
            return 0
            
    def _update_performance_metrics(self, cycle_metrics: Dict[str, Any]):
        """Update overall performance metrics"""
        self.performance_metrics['total_cycles'] += 1
        
        if cycle_metrics['success_rate'] > 0.5:
            self.performance_metrics['successful_cycles'] += 1
            
        self.performance_metrics['total_fixes_applied'] += cycle_metrics['fixes_applied']
        
        # Update averages
        total_cycles = self.performance_metrics['total_cycles']
        
        # Running average of cycle time
        current_avg = self.performance_metrics['average_cycle_time']
        new_duration = cycle_metrics['duration']
        self.performance_metrics['average_cycle_time'] = (
            (current_avg * (total_cycles - 1) + new_duration) / total_cycles
        )
        
        # Overall fix success rate
        self.performance_metrics['fix_success_rate'] = (
            self.performance_metrics['successful_cycles'] / total_cycles
        )
        
        # Average AI confidence
        if cycle_metrics['ai_responses']:
            avg_confidence = sum(
                resp.get('confidence', 0) for resp in cycle_metrics['ai_responses']
            ) / len(cycle_metrics['ai_responses'])
            
            current_ai_avg = self.performance_metrics['ai_confidence_avg']
            self.performance_metrics['ai_confidence_avg'] = (
                (current_ai_avg * (total_cycles - 1) + avg_confidence) / total_cycles
            )
            
    def generate_health_report(self, fixer_instance) -> Dict[str, Any]:
        """Generate comprehensive health report of the self-healing system"""
        current_status = fixer_instance.get_status()
        
        # AI-powered system health analysis
        health_analysis = self._analyze_system_health(current_status)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'system_status': current_status,
            'performance_metrics': self.performance_metrics,
            'health_analysis': health_analysis,
            'monitoring_sessions': len(self.monitoring_history),
            'recommendations': self._generate_recommendations(current_status)
        }
        
        return report
        
    def _analyze_system_health(self, status: Dict[str, Any]) -> Dict[str, Any]:
        """AI analysis of overall system health"""
        try:
            health_prompt = f"""
            Analyze the health of this autonomous test fixing system:
            
            Current Status:
            - Running: {status.get('running', False)}
            - Iteration: {status.get('iteration', 0)}
            - Total Fixes Applied: {status.get('total_fixes_applied', 0)}
            - All Tests Passing: {status.get('all_tests_passing', False)}
            
            Performance Metrics:
            - Total Cycles: {self.performance_metrics['total_cycles']}
            - Success Rate: {self.performance_metrics['fix_success_rate']:.2%}
            - Average Cycle Time: {self.performance_metrics['average_cycle_time']:.2f}s
            - Average AI Confidence: {self.performance_metrics['ai_confidence_avg']:.2f}
            
            Provide health assessment in JSON:
            {{
                "overall_health": "excellent|good|fair|poor|critical",
                "health_score": 0.85,
                "system_stability": "stable|unstable|declining",
                "performance_trend": "improving|stable|declining", 
                "critical_issues": ["issue1", "issue2"],
                "strengths": ["strength1", "strength2"],
                "maintenance_required": false
            }}
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": health_prompt}],
                response_format={"type": "json_object"},
                max_tokens=600,
                temperature=0.1
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Health analysis failed: {e}")
            return {
                "overall_health": "unknown",
                "health_score": 0.5,
                "system_stability": "unknown",
                "performance_trend": "unknown",
                "critical_issues": ["Health analysis unavailable"],
                "strengths": [],
                "maintenance_required": True
            }
            
    def _generate_recommendations(self, status: Dict[str, Any]) -> List[str]:
        """Generate AI-powered recommendations for system improvement"""
        recommendations = []
        
        # Performance-based recommendations
        if self.performance_metrics['fix_success_rate'] < 0.7:
            recommendations.append("Consider lowering AI confidence threshold for fixes")
            
        if self.performance_metrics['average_cycle_time'] > 60:
            recommendations.append("Optimize test execution for faster cycles")
            
        if status.get('iteration', 0) > 30 and not status.get('all_tests_passing', False):
            recommendations.append("Manual intervention may be required for complex failures")
            
        if self.performance_metrics['ai_confidence_avg'] < 0.6:
            recommendations.append("Review AI prompts and failure analysis quality")
            
        return recommendations
        
    def predict_completion_time(self, fixer_instance) -> Dict[str, Any]:
        """AI-powered prediction of when all tests will pass"""
        current_status = fixer_instance.get_status()
        
        if current_status.get('all_tests_passing', False):
            return {
                'completion_status': 'completed',
                'estimated_time': 0,
                'confidence': 1.0
            }
            
        # Simple prediction based on current metrics
        avg_cycle_time = self.performance_metrics['average_cycle_time']
        success_rate = self.performance_metrics['fix_success_rate']
        
        if success_rate > 0:
            # Estimate remaining cycles needed
            estimated_cycles = min(10, max(1, int(1 / success_rate)))
            estimated_time = estimated_cycles * avg_cycle_time
            confidence = min(0.9, success_rate)
        else:
            estimated_cycles = 10
            estimated_time = 600  # 10 minutes fallback
            confidence = 0.3
            
        return {
            'completion_status': 'in_progress',
            'estimated_cycles_remaining': estimated_cycles,
            'estimated_time_seconds': estimated_time,
            'confidence': confidence
        }
        
    def export_monitoring_data(self) -> Dict[str, Any]:
        """Export all monitoring data for analysis"""
        return {
            'performance_metrics': self.performance_metrics,
            'monitoring_history': self.monitoring_history,
            'export_timestamp': datetime.now().isoformat()
        }