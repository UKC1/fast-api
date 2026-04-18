import time
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from .context import request_context
from .logger import get_logger

logger = get_logger("middleware")

class RequestTrackerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request_context.set_request_id(request_id)
        
        start_time = time.perf_counter()
        
        logger.info(
            "Request started",
            extra={
                "extra_data": {
                    "method": request.method,
                    "path": request.url.path,
                    "client": request.client.host if request.client else None,
                }
            }
        )
        
        response = await call_next(request)
        
        process_time = (time.perf_counter() - start_time) * 1000
        
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.3f}ms"
        
        logger.info(
            "Request completed",
            extra={
                "performance": {
                    "duration_ms": round(process_time, 3),
                    "status_code": response.status_code,
                },
                "extra_data": {
                    "method": request.method,
                    "path": request.url.path,
                    "status": response.status_code,
                }
            }
        )
        
        return response