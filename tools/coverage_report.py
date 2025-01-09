"""Test coverage reporting and analysis utilities."""
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple
import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger(__name__)

class CoverageAnalyzer:
    """Analyzes and reports test coverage metrics."""
    
    def __init__(self, xml_path: Path):
        self.xml_path = xml_path
        self.metrics = {}
        self.threshold = 80.0  # Minimum acceptable coverage
        
    def analyze_coverage(self) -> Tuple[Dict[str, float], List[str]]:
        """
        Analyze coverage data from XML report.
        Returns (metrics, warnings).
        """
        try:
            tree = ET.parse(self.xml_path)
            root = tree.getroot()
            warnings = []
            
            # Collect metrics
            for package in root.findall(".//package"):
                package_name = package.get("name")
                self.metrics[package_name] = {
                    "line": float(package.get("line-rate", 0)) * 100,
                    "branch": float(package.get("branch-rate", 0)) * 100,
                    "complexity": float(package.get("complexity", 0))
                }
                
                # Check coverage thresholds
                if self.metrics[package_name]["line"] < self.threshold:
                    warnings.append(
                        f"Low line coverage in {package_name}: "
                        f"{self.metrics[package_name]['line']:.1f}%"
                    )
                if self.metrics[package_name]["branch"] < self.threshold:
                    warnings.append(
                        f"Low branch coverage in {package_name}: "
                        f"{self.metrics[package_name]['branch']:.1f}%"
                    )
                    
            return self.metrics, warnings
            
        except Exception as e:
            logger.error(f"Failed to analyze coverage: {str(e)}")
            return {}, [f"Coverage analysis failed: {str(e)}"]
            
    def generate_report(self, output_path: Path) -> bool:
        """Generate a detailed coverage report in JSON format."""
        try:
            metrics, warnings = self.analyze_coverage()
            
            report = {
                "metrics": metrics,
                "warnings": warnings,
                "summary": self._generate_summary(metrics)
            }
            
            with open(output_path, "w") as f:
                json.dump(report, f, indent=2)
                
            return True
            
        except Exception as e:
            logger.error(f"Failed to generate report: {str(e)}")
            return False
            
    def _generate_summary(self, metrics: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """Generate overall coverage summary."""
        if not metrics:
            return {}
            
        total_line = 0
        total_branch = 0
        total_complexity = 0
        count = len(metrics)
        
        for pkg_metrics in metrics.values():
            total_line += pkg_metrics["line"]
            total_branch += pkg_metrics["branch"]
            total_complexity += pkg_metrics["complexity"]
            
        return {
            "average_line_coverage": total_line / count,
            "average_branch_coverage": total_branch / count,
            "total_complexity": total_complexity
        }
        
def main():
    """CLI entry point for coverage analysis."""
    if len(sys.argv) != 3:
        print("Usage: coverage_report.py <coverage.xml> <output.json>")
        sys.exit(1)
        
    xml_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    
    if not xml_path.exists():
        print(f"Coverage XML file not found: {xml_path}")
        sys.exit(1)
        
    analyzer = CoverageAnalyzer(xml_path)
    if analyzer.generate_report(output_path):
        print(f"Coverage report generated: {output_path}")
    else:
        print("Failed to generate coverage report")
        sys.exit(1)
        
if __name__ == "__main__":
    main() 