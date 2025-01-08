"""API version management and compatibility handling.

This module provides tools and utilities for managing API versions, ensuring
compatibility between different versions, and handling version-specific features.
"""

from enum import Enum
from functools import wraps
from typing import Any, Callable, Dict, Optional, Set, Tuple, TypeVar, Union
import warnings

class APIVersion(Enum):
    """Supported API versions."""
    V1_0 = "1.0"
    V1_1 = "1.1"
    V2_0 = "2.0"

    @classmethod
    def latest(cls) -> 'APIVersion':
        """Get the latest API version."""
        return sorted(cls, key=lambda v: [int(x) for x in v.value.split('.')])[-1]

    @classmethod
    def from_string(cls, version: str) -> 'APIVersion':
        """Convert string version to APIVersion enum."""
        try:
            return cls(version)
        except ValueError:
            raise ValueError(f"Unsupported API version: {version}")

class VersionedFeature:
    """Decorator for version-specific features."""
    
    def __init__(
        self,
        introduced: str,
        deprecated: Optional[str] = None,
        removed: Optional[str] = None,
        replacement: Optional[str] = None
    ):
        """Initialize version information.
        
        Args:
            introduced: Version where feature was introduced
            deprecated: Version where feature was deprecated
            removed: Version where feature will be/was removed
            replacement: Name of replacement feature/method
        """
        self.introduced = APIVersion.from_string(introduced)
        self.deprecated = APIVersion.from_string(deprecated) if deprecated else None
        self.removed = APIVersion.from_string(removed) if removed else None
        self.replacement = replacement

    def __call__(self, func: Callable) -> Callable:
        """Apply version checking to function."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_version = get_active_version()
            
            # Check if feature is available in current version
            if current_version < self.introduced:
                raise NotImplementedError(
                    f"This feature requires API version {self.introduced.value} "
                    f"or later (current version: {current_version.value})"
                )
            
            # Check if feature has been removed
            if self.removed and current_version >= self.removed:
                raise NotImplementedError(
                    f"This feature was removed in version {self.removed.value}. "
                    + (f"Please use {self.replacement} instead." if self.replacement else "")
                )
            
            # Warn if feature is deprecated
            if self.deprecated and current_version >= self.deprecated:
                warnings.warn(
                    f"This feature is deprecated since version {self.deprecated.value} "
                    + (f"Please use {self.replacement} instead." if self.replacement else ""),
                    DeprecationWarning,
                    stacklevel=2
                )
            
            return func(*args, **kwargs)
        return wrapper

# Global version state
_ACTIVE_VERSION: APIVersion = APIVersion.latest()
_VERSION_CONTEXTS: Dict[int, APIVersion] = {}

def set_api_version(version: Union[str, APIVersion]) -> None:
    """Set the active API version globally.
    
    Args:
        version: API version to set
    """
    global _ACTIVE_VERSION
    if isinstance(version, str):
        version = APIVersion.from_string(version)
    _ACTIVE_VERSION = version

def get_active_version() -> APIVersion:
    """Get the currently active API version."""
    return _ACTIVE_VERSION

class VersionContext:
    """Context manager for temporary API version changes."""
    
    def __init__(self, version: Union[str, APIVersion]):
        """Initialize version context.
        
        Args:
            version: API version to use within context
        """
        self.version = (
            APIVersion.from_string(version)
            if isinstance(version, str)
            else version
        )
        self.previous_version: Optional[APIVersion] = None
    
    def __enter__(self) -> 'VersionContext':
        """Enter version context."""
        self.previous_version = get_active_version()
        set_api_version(self.version)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit version context."""
        if self.previous_version:
            set_api_version(self.previous_version)

def version_compatible(*versions: str) -> Callable:
    """Decorator to mark functions as compatible with specific API versions.
    
    Args:
        *versions: Compatible API versions
    """
    compatible_versions = {APIVersion.from_string(v) for v in versions}
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_version = get_active_version()
            if current_version not in compatible_versions:
                raise NotImplementedError(
                    f"This feature is not compatible with API version {current_version.value}. "
                    f"Compatible versions: {', '.join(v.value for v in compatible_versions)}"
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Type variable for generic type hints
T = TypeVar('T')

def version_dispatch(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator for version-specific implementations of functions.
    
    Usage:
        @version_dispatch
        def my_function(arg):
            # Default implementation
            
        @my_function.version('1.0')
        def my_function_v1(arg):
            # Version 1.0 implementation
            
        @my_function.version('2.0')
        def my_function_v2(arg):
            # Version 2.0 implementation
    """
    implementations: Dict[APIVersion, Callable[..., T]] = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs) -> T:
        current_version = get_active_version()
        # Find the newest compatible version
        compatible_versions = [
            v for v in implementations.keys()
            if v <= current_version
        ]
        if not compatible_versions:
            return func(*args, **kwargs)  # Use default implementation
        version = max(compatible_versions)
        return implementations[version](*args, **kwargs)
    
    def register_version(version: str) -> Callable[[Callable[..., T]], Callable[..., T]]:
        def decorator(implementation: Callable[..., T]) -> Callable[..., T]:
            implementations[APIVersion.from_string(version)] = implementation
            return implementation
        return decorator
    
    wrapper.version = register_version
    return wrapper 