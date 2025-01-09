"""Test result analysis and reporting utilities."""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from xml.etree import ElementTree as ET

logger = logging.getLogger(__name__)

class TestResultAnalyzer:
    """Analyzes and reports test execution results."""
    
    def __init__(self, junit_path: Path):
        self.junit_path = junit_path
        self.results = {}
        self.summary = {}
        
    def analyze_results(self) -> Tuple[Dict[str, Dict], List[str]]:
        """
        Analyze test results from JUnit XML report.
        Returns (results, insights).
        """
        try:
            tree = ET.parse(self.junit_path)
            root = tree.getroot()
            insights = []
            
            # Collect test suite metrics
            for testsuite in root.findall(".//testsuite"):
                suite_name = testsuite.get("name")
                self.results[suite_name] = {
                    "tests": int(testsuite.get("tests", 0)),
                    "failures": int(testsuite.get("failures", 0)),
                    "errors": int(testsuite.get("errors", 0)),
                    "skipped": int(testsuite.get("skipped", 0)),
                    "time": float(testsuite.get("time", 0)),
                    "timestamp": testsuite.get("timestamp", ""),
                    "test_cases": []
                }
                
                # Analyze test cases
                for testcase in testsuite.findall(".//testcase"):
                    case_data = {
                        "name": testcase.get("name"),
                        "time": float(testcase.get("time", 0)),
                        "status": "passed"
                    }
                    
                    # Check for failures/errors
                    failure = testcase.find("failure")
                    error = testcase.find("error")
                    skipped = testcase.find("skipped")
                    
                    if failure is not None:
                        case_data["status"] = "failed"
                        case_data["message"] = failure.get("message", "")
                        insights.append(f"Test failed: {suite_name}.{case_data['name']} - {case_data['message']}")
                    elif error is not None:
                        case_data["status"] = "error"
                        case_data["message"] = error.get("message", "")
                        insights.append(f"Test error: {suite_name}.{case_data['name']} - {case_data['message']}")
                    elif skipped is not None:
                        case_data["status"] = "skipped"
                        case_data["message"] = skipped.get("message", "")
                        
                    self.results[suite_name]["test_cases"].append(case_data)
                    
                # Generate suite insights
                suite_metrics = self.results[suite_name]
                if suite_metrics["failures"] > 0:
                    insights.append(f"Suite {suite_name} has {suite_metrics['failures']} failures")
                if suite_metrics["errors"] > 0:
                    insights.append(f"Suite {suite_name} has {suite_metrics['errors']} errors")
                if suite_metrics["skipped"] > 0:
                    insights.append(f"Suite {suite_name} has {suite_metrics['skipped']} skipped tests")
                    
            self._generate_summary()
            return self.results, insights
            
        except Exception as e:
            logger.error(f"Failed to analyze test results: {str(e)}")
            return {}, [f"Analysis failed: {str(e)}"]
            
    def _generate_summary(self):
        """Generate overall test execution summary."""
        total_tests = 0
        total_failures = 0
        total_errors = 0
        total_skipped = 0
        total_time = 0.0
        
        for suite_metrics in self.results.values():
            total_tests += suite_metrics["tests"]
            total_failures += suite_metrics["failures"]
            total_errors += suite_metrics["errors"]
            total_skipped += suite_metrics["skipped"]
            total_time += suite_metrics["time"]
            
        self.summary = {
            "total_tests": total_tests,
            "total_failures": total_failures,
            "total_errors": total_errors,
            "total_skipped": total_skipped,
            "total_time": total_time,
            "success_rate": (total_tests - total_failures - total_errors) / total_tests * 100 if total_tests > 0 else 0
        }
        
    def generate_report(self, output_path: Path) -> bool:
        """Generate detailed test analysis report in JSON format."""
        try:
            report = {
                "timestamp": datetime.now().isoformat(),
                "results": self.results,
                "summary": self.summary,
                "insights": self._generate_insights()
            }
            
            with open(output_path, "w") as f:
                json.dump(report, f, indent=2)
                
            return True
            
        except Exception as e:
            logger.error(f"Failed to generate report: {str(e)}")
            return False
            
    def _generate_insights(self) -> List[str]:
        """Generate test execution insights and recommendations."""
        insights = []
        
        # Overall health check
        if self.summary["success_rate"] < 90:
            insights.append(f"Low success rate: {self.summary['success_rate']:.1f}%")
            
        # Performance insights
        slow_tests = []
        for suite_name, suite_data in self.results.items():
            for test_case in suite_data["test_cases"]:
                if test_case["time"] > 1.0:  # Tests taking more than 1 second
                    slow_tests.append(f"{suite_name}.{test_case['name']}")
                    
        if slow_tests:
            insights.append(f"Slow tests detected ({len(slow_tests)}):")
            insights.extend(f"  - {test}" for test in slow_tests)
            
        # Test distribution
        if self.summary["total_skipped"] > self.summary["total_tests"] * 0.1:
            insights.append(f"High number of skipped tests: {self.summary['total_skipped']}")
            
        return insights
        
    def get_failing_tests(self) -> List[Dict]:
        """Get list of failing tests with details."""
        failing_tests = []
        for suite_name, suite_data in self.results.items():
            for test_case in suite_data["test_cases"]:
                if test_case["status"] in ["failed", "error"]:
                    failing_tests.append({
                        "suite": suite_name,
                        "test": test_case["name"],
                        "status": test_case["status"],
                        "message": test_case.get("message", ""),
                        "time": test_case["time"]
                    })
        return failing_tests
        
    def get_test_patterns(self) -> Dict[str, List[str]]:
        """Identify patterns in test failures."""
        patterns = {
            "common_failures": [],
            "flaky_tests": [],
            "slow_tests": [],
            "error_patterns": {}
        }
        
        # Analyze error messages for patterns
        error_counts = {}
        for suite_data in self.results.values():
            for test_case in suite_data["test_cases"]:
                if test_case["status"] in ["failed", "error"]:
                    message = test_case.get("message", "")
                    error_counts[message] = error_counts.get(message, 0) + 1
                    
        # Identify common error patterns
        for message, count in error_counts.items():
            if count > 1:  # Error occurs multiple times
                patterns["error_patterns"][message] = count
                
        return patterns 