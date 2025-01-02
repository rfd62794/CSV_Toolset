import pandas as pd
import numpy as np
from typing import Dict, Any, List
from ..base.base_processor import BaseProcessor
from pathlib import Path
import json

class ValidatorProcessor(BaseProcessor):
    """Processor for data validation"""
    
    def validate_data(self, df: pd.DataFrame, config: dict) -> Dict[str, Any]:
        """Validates dataframe according to configuration"""
        if df is None or df.empty:
            raise ValueError("No data to validate")
            
        try:
            results = {
                'summary': {},
                'details': []
            }
            
            columns = config.get('columns', df.columns)
            row_count = len(df)
            
            for col in columns:
                issues = []
                
                # Check missing values
                if config.get('check_missing', True):
                    missing = df[col].isna().sum()
                    if missing > 0:
                        issues.append(f"Missing values: {missing}")
                        # Add detailed issues
                        missing_rows = df[df[col].isna()].index.tolist()
                        for row in missing_rows[:10]:  # Limit to first 10 for display
                            results['details'].append({
                                'row': row + 1,
                                'column': col,
                                'value': 'NULL',
                                'issue': 'Missing value'
                            })
                
                # Check duplicates
                if config.get('check_duplicates', True):
                    duplicates = df[col].duplicated().sum()
                    if duplicates > 0:
                        issues.append(f"Duplicate values: {duplicates}")
                        # Add detailed issues
                        dup_rows = df[df[col].duplicated()].index.tolist()
                        for row in dup_rows[:10]:
                            results['details'].append({
                                'row': row + 1,
                                'column': col,
                                'value': str(df.at[row, col]),
                                'issue': 'Duplicate value'
                            })
                
                # Check data types
                if config.get('check_datatypes', True):
                    dtype = df[col].dtype
                    if dtype == 'object':
                        # Check if should be numeric
                        numeric_ratio = df[col].str.match(r'^-?\d*\.?\d+$').mean()
                        if numeric_ratio > 0.8:  # If >80% are numeric
                            issues.append(f"Possible numeric column stored as text")
                            # Add examples
                            non_numeric = df[~df[col].str.match(r'^-?\d*\.?\d+$')].index.tolist()
                            for row in non_numeric[:10]:
                                results['details'].append({
                                    'row': row + 1,
                                    'column': col,
                                    'value': str(df.at[row, col]),
                                    'issue': 'Non-numeric value in numeric-like column'
                                })
                
                # Check outliers for numeric columns
                if config.get('check_outliers', True) and pd.api.types.is_numeric_dtype(df[col]):
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower = Q1 - 1.5 * IQR
                    upper = Q3 + 1.5 * IQR
                    outliers = df[(df[col] < lower) | (df[col] > upper)][col]
                    if len(outliers) > 0:
                        issues.append(f"Outliers: {len(outliers)}")
                        # Add detailed issues
                        for row in outliers.index[:10]:
                            results['details'].append({
                                'row': row + 1,
                                'column': col,
                                'value': str(df.at[row, col]),
                                'issue': 'Outlier value'
                            })
                
                results['summary'][col] = issues
            
            return results
            
        except Exception as e:
            raise ValueError(f"Error validating data: {str(e)}")
    
    def export_report(self, df: pd.DataFrame, config: dict) -> Dict[str, Any]:
        """Exports validation results to a report file"""
        try:
            results = self.validate_data(df, config)
            
            # Create report directory if it doesn't exist
            report_dir = Path("reports")
            report_dir.mkdir(exist_ok=True)
            
            # Generate report filename
            timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
            report_file = report_dir / f"validation_report_{timestamp}.json"
            
            # Add metadata to results
            results['metadata'] = {
                'filename': Path(self.input_file).name if self.input_file else "Unknown",
                'timestamp': timestamp,
                'row_count': len(df),
                'column_count': len(df.columns),
                'validated_columns': config.get('columns', []),
                'configuration': config
            }
            
            # Save report
            with open(report_file, 'w') as f:
                json.dump(results, f, indent=4)
            
            return {
                'success': True,
                'output_file': str(report_file),
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'output_file': None,
                'error': str(e)
            }
    
    def _process_data(self, df: pd.DataFrame, config: dict) -> pd.DataFrame:
        """Required implementation of abstract method"""
        return df  # Validator doesn't modify data 