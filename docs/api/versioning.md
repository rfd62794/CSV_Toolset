# API Versioning Guide

Last updated: 2025-01-10

## Overview

CSV Toolset uses semantic versioning for its API to ensure compatibility and smooth transitions between versions. This guide explains how to use different API versions and manage version-specific features.

## Version Support

### Current Versions

| Version | Status | Released | End of Support |
|---------|---------|-----------|----------------|
| 2.0     | Latest  | 2025-01   | Active         |
| 1.1     | Stable  | 2024-12   | 2025-12        |
| 1.0     | Legacy  | 2024-11   | 2025-06        |

### Version Lifecycle

1. **Active**: Latest version, actively developed
2. **Stable**: Maintained with bug fixes
3. **Legacy**: Security fixes only
4. **EOL**: End of life, no support

## Using API Versions

### Setting the API Version

```python
from csv_toolset.api.version import set_api_version

# Use specific version
set_api_version("1.1")

# Use latest version
from csv_toolset.api.version import APIVersion
set_api_version(APIVersion.latest())
```

### Version Context

For temporary version changes:

```python
from csv_toolset.api.version import VersionContext

with VersionContext("1.0"):
    # Code using version 1.0
    process_data()
```

## Version Decorators

### Feature Versioning

```python
from csv_toolset.api.version import VersionedFeature

@VersionedFeature(
    introduced="1.0",
    deprecated="1.1",
    removed="2.0",
    replacement="new_process_data"
)
def process_data():
    # Implementation
```

### Version Compatibility

```python
from csv_toolset.api.version import version_compatible

@version_compatible("1.0", "1.1")
def legacy_function():
    # Implementation
```

### Version Dispatch

```python
from csv_toolset.api.version import version_dispatch

@version_dispatch
def process_csv(data):
    # Default implementation

@process_csv.version("1.0")
def process_csv_v1(data):
    # Version 1.0 implementation

@process_csv.version("2.0")
def process_csv_v2(data):
    # Version 2.0 implementation
```

## Migration Guide

### Upgrading from 1.0 to 1.1

1. Update version requirements
2. Replace deprecated functions
3. Test with both versions
4. Update documentation

### Upgrading from 1.1 to 2.0

1. Review breaking changes
2. Update code for new API
3. Remove deprecated calls
4. Update dependencies

## Best Practices

1. Always specify API version
2. Test with target versions
3. Handle deprecation warnings
4. Follow migration guides
5. Keep dependencies updated

## Version Compatibility

### Feature Matrix

| Feature | 1.0 | 1.1 | 2.0 |
|---------|-----|-----|-----|
| Basic CSV Processing | ✓ | ✓ | ✓ |
| Column Splitting | ✓ | ✓ | ✓ |
| Data Truncation | ✓ | ✓ | ✓ |
| Advanced Filtering | - | ✓ | ✓ |
| Batch Processing | - | - | ✓ |

### Breaking Changes

#### Version 2.0
- Removed legacy processors
- Changed default encodings
- Updated error handling
- Modified return types

#### Version 1.1
- Deprecated old filters
- Added type hints
- Enhanced error messages

## Error Handling

### Version-specific Errors

```python
try:
    process_data()
except NotImplementedError as e:
    # Handle version compatibility error
```

### Deprecation Warnings

```python
import warnings
warnings.filterwarnings('error', category=DeprecationWarning)
```

## Support Policy

- Major versions: 12 months
- Minor versions: 6 months
- Security fixes: 18 months
- Critical bugs: All supported versions

## Additional Resources

- [Changelog](../CHANGELOG.md)
- [Migration Scripts](../tools/migration/)
- [Version Tests](../tests/version/)
- [API Reference](./reference/) 