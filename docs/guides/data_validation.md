# Data Validation Guide

## Overview
This guide provides comprehensive strategies and best practices for validating CSV data in the CSV Toolkit. It covers various aspects of data validation, from basic type checking to complex business rule validation.

## Data Validation Framework

### 1. Basic Validators
```python
class DataValidator:
    def __init__(self):
        self.validators = {
            'string': self.validate_string,
            'integer': self.validate_integer,
            'float': self.validate_float,
            'date': self.validate_date,
            'email': self.validate_email,
            'phone': self.validate_phone
        }
    
    def validate(self, value: Any, type_name: str) -> bool:
        validator = self.validators.get(type_name)
        if not validator:
            raise ValueError(f"Unknown type: {type_name}")
        return validator(value)
```

### 2. Schema Validation
```python
@dataclass
class ColumnSchema:
    name: str
    type: str
    required: bool = True
    unique: bool = False
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    pattern: Optional[str] = None
    choices: Optional[List[Any]] = None

class SchemaValidator:
    def validate_dataframe(
        self,
        df: pd.DataFrame,
        schema: Dict[str, ColumnSchema]
    ) -> ValidationResult:
        results = []
        for col_name, col_schema in schema.items():
            result = self.validate_column(
                df[col_name],
                col_schema
            )
            results.append(result)
        return ValidationResult(results)
```

### 3. Custom Validators
```python
class CustomValidator:
    def __init__(self, validation_func, error_message):
        self.validate = validation_func
        self.error_message = error_message
    
    def __call__(self, value):
        is_valid = self.validate(value)
        if not is_valid:
            raise ValidationError(self.error_message)
        return True

# Example usage
phone_validator = CustomValidator(
    lambda x: re.match(r'^\+?1?\d{9,15}$', str(x)),
    "Invalid phone number format"
)
```

## Validation Rules

### 1. Type Validation
```python
class TypeValidator:
    def validate_type(self, value: Any, expected_type: type) -> bool:
        if expected_type == str:
            return isinstance(value, str)
        elif expected_type == int:
            try:
                int(value)
                return True
            except (ValueError, TypeError):
                return False
        elif expected_type == float:
            try:
                float(value)
                return True
            except (ValueError, TypeError):
                return False
        elif expected_type == datetime:
            try:
                pd.to_datetime(value)
                return True
            except (ValueError, TypeError):
                return False
        return isinstance(value, expected_type)
```

### 2. Format Validation
```python
class FormatValidator:
    def __init__(self):
        self.patterns = {
            'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'phone': r'^\+?1?\d{9,15}$',
            'date': r'^\d{4}-\d{2}-\d{2}$',
            'time': r'^\d{2}:\d{2}:\d{2}$',
            'zipcode': r'^\d{5}(-\d{4})?$'
        }
    
    def validate_format(self, value: str, format_name: str) -> bool:
        pattern = self.patterns.get(format_name)
        if not pattern:
            raise ValueError(f"Unknown format: {format_name}")
        return bool(re.match(pattern, str(value)))
```

### 3. Range Validation
```python
class RangeValidator:
    def validate_range(
        self,
        value: Union[int, float, datetime],
        min_value: Optional[Any] = None,
        max_value: Optional[Any] = None
    ) -> bool:
        if min_value is not None and value < min_value:
            return False
        if max_value is not None and value > max_value:
            return False
        return True
```

## Data Cleaning

### 1. Data Cleaner
```python
class DataCleaner:
    def clean_string(self, value: str) -> str:
        """Clean string values"""
        if pd.isna(value):
            return ""
        return str(value).strip()
    
    def clean_number(self, value: Any) -> Optional[float]:
        """Clean numeric values"""
        if pd.isna(value):
            return None
        try:
            return float(str(value).replace(',', ''))
        except ValueError:
            return None
```

### 2. Missing Value Handler
```python
class MissingValueHandler:
    def handle_missing(
        self,
        df: pd.DataFrame,
        strategy: Dict[str, str]
    ) -> pd.DataFrame:
        """Handle missing values with different strategies"""
        for column, strat in strategy.items():
            if strat == 'mean':
                df[column].fillna(df[column].mean(), inplace=True)
            elif strat == 'median':
                df[column].fillna(df[column].median(), inplace=True)
            elif strat == 'mode':
                df[column].fillna(df[column].mode()[0], inplace=True)
            elif strat == 'zero':
                df[column].fillna(0, inplace=True)
            elif strat == 'empty_string':
                df[column].fillna('', inplace=True)
        return df
```

## Business Rules Validation

### 1. Rule Engine
```python
class BusinessRule:
    def __init__(self, condition, error_message):
        self.condition = condition
        self.error_message = error_message
    
    def validate(self, data: pd.DataFrame) -> List[str]:
        mask = self.condition(data)
        violations = data[~mask]
        return [
            f"{self.error_message} at index {idx}"
            for idx in violations.index
        ]

class BusinessRuleEngine:
    def __init__(self):
        self.rules = []
    
    def add_rule(self, rule: BusinessRule):
        self.rules.append(rule)
    
    def validate_all(self, data: pd.DataFrame) -> List[str]:
        errors = []
        for rule in self.rules:
            errors.extend(rule.validate(data))
        return errors
```

### 2. Complex Validation
```python
class ComplexValidator:
    def validate_dependencies(
        self,
        row: pd.Series,
        dependencies: Dict[str, List[str]]
    ) -> bool:
        """Validate column dependencies"""
        for col, depends_on in dependencies.items():
            if pd.notna(row[col]):
                for dep in depends_on:
                    if pd.isna(row[dep]):
                        return False
        return True
```

## Performance Optimization

### 1. Batch Processing
```python
class BatchValidator:
    def validate_batch(
        self,
        df: pd.DataFrame,
        batch_size: int = 1000
    ) -> List[ValidationResult]:
        results = []
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
            result = self.validate_dataframe(batch)
            results.append(result)
        return results
```

### 2. Parallel Validation
```python
class ParallelValidator:
    def validate_parallel(
        self,
        df: pd.DataFrame,
        num_workers: int = 4
    ) -> List[ValidationResult]:
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            chunks = np.array_split(df, num_workers)
            futures = [
                executor.submit(self.validate_dataframe, chunk)
                for chunk in chunks
            ]
            return [f.result() for f in futures]
```

## Error Reporting

### 1. Validation Report
```python
@dataclass
class ValidationError:
    column: str
    row_index: int
    value: Any
    error_type: str
    message: str

class ValidationReport:
    def __init__(self):
        self.errors: List[ValidationError] = []
    
    def add_error(self, error: ValidationError):
        self.errors.append(error)
    
    def generate_report(self) -> Dict:
        return {
            'total_errors': len(self.errors),
            'errors_by_column': self.group_by_column(),
            'errors_by_type': self.group_by_type(),
            'error_details': [asdict(e) for e in self.errors]
        }
```

### 2. Error Visualization
```python
class ErrorVisualizer:
    def create_error_heatmap(
        self,
        df: pd.DataFrame,
        errors: List[ValidationError]
    ) -> go.Figure:
        """Create heatmap of validation errors"""
        error_matrix = np.zeros((len(df), len(df.columns)))
        for error in errors:
            error_matrix[error.row_index][
                df.columns.get_loc(error.column)
            ] += 1
        
        return go.Figure(
            data=go.Heatmap(z=error_matrix),
            layout=go.Layout(
                title='Validation Error Heatmap'
            )
        )
```

## Best Practices

### 1. Data Validation
- Validate data as early as possible
- Use appropriate data types
- Handle missing values explicitly
- Implement business rules validation
- Document validation rules

### 2. Error Handling
- Provide clear error messages
- Group related validation errors
- Generate comprehensive reports
- Implement error visualization
- Track validation metrics

### 3. Performance
- Use batch processing for large datasets
- Implement parallel validation
- Optimize validation rules
- Cache validation results
- Monitor validation performance 