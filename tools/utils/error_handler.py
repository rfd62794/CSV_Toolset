from typing import Callable, Any, Optional, Type, Union
import traceback
import logging
from functools import wraps

class ErrorHandler:
    """Centralized error handling"""
    
    @staticmethod
    def handle_error(error: Exception, log: bool = True) -> str:
        """Formats error message with optional logging"""
        error_msg = str(error)
        if log:
            logging.error(f"Error occurred: {error_msg}")
            logging.debug(traceback.format_exc())
        return error_msg
    
    @staticmethod
    def safe_call(func: Callable, *args, default: Any = None, 
                  error_handler: Optional[Callable[[Exception], Any]] = None,
                  **kwargs) -> Any:
        """Safely calls function with error handling"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if error_handler:
                return error_handler(e)
            return default
            
    @classmethod
    def catch_errors(cls, error_types: Union[Type[Exception], tuple] = Exception,
                    default: Any = None) -> Callable:
        """Decorator for catching and handling errors"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except error_types as e:
                    cls.handle_error(e)
                    return default
            return wrapper
        return decorator 