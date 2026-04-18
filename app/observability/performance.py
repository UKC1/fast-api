import time
from typing import Optional, Dict, Any
from functools import wraps
from .logger import get_logger
from .context import request_context

class PerformanceTracker:
    def __init__(self):
        self.logger = get_logger("performance")
    
    def track(self, operation: str, metadata: Optional[Dict[str, Any]] = None):
        """Decorator to track performance of functions"""
        def decorator(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                try:
                    result = await func(*args, **kwargs)
                    duration_ms = (time.perf_counter() - start_time) * 1000
                    self._log_performance(operation, duration_ms, "success", metadata)
                    return result
                except Exception as e:
                    duration_ms = (time.perf_counter() - start_time) * 1000
                    self._log_performance(operation, duration_ms, "error", metadata, str(e))
                    raise
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                try:
                    result = func(*args, **kwargs)
                    duration_ms = (time.perf_counter() - start_time) * 1000
                    self._log_performance(operation, duration_ms, "success", metadata)
                    return result
                except Exception as e:
                    duration_ms = (time.perf_counter() - start_time) * 1000
                    self._log_performance(operation, duration_ms, "error", metadata, str(e))
                    raise
            
            if func.__name__.startswith('async_') or func.__code__.co_flags & 0x80:
                return async_wrapper
            return sync_wrapper
        return decorator
    
    def _log_performance(self, operation: str, duration_ms: float, status: str, 
                        metadata: Optional[Dict[str, Any]] = None, error: Optional[str] = None):
        log_data = {
            "performance": {
                "operation": operation,
                "duration_ms": round(duration_ms, 3),
                "status": status,
                "request_id": request_context.get_request_id()
            }
        }
        
        if metadata:
            log_data["performance"]["metadata"] = metadata
        
        if error:
            log_data["performance"]["error"] = error
            self.logger.error(f"Operation failed: {operation}", extra=log_data)
        elif duration_ms > 1000:  # Slow operation warning
            self.logger.warning(f"Slow operation: {operation}", extra=log_data)
        else:
            self.logger.info(f"Operation completed: {operation}", extra=log_data)

performance_tracker = PerformanceTracker()