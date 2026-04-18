import logging
import sys
import os
from typing import Optional
import json
from datetime import datetime
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
from .context import request_context
from ..config import settings

class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_context.get_request_id() or "no-request"
        return True

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", None),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        if hasattr(record, "performance"):
            log_data["performance"] = record.performance
            
        if hasattr(record, "extra_data"):
            log_data.update(record.extra_data)
            
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_data, ensure_ascii=False)

def setup_logger(name: str = "app", level: str = None, log_to_file: bool = None) -> logging.Logger:
    if level is None:
        level = settings.LOG_LEVEL
    if log_to_file is None:
        log_to_file = settings.LOG_TO_FILE
        
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    logger.propagate = False
    
    # Clear existing handlers to avoid duplicates
    logger.handlers = []
    
    if not logger.handlers or True:  # Force setup
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(JSONFormatter())
        console_handler.addFilter(RequestIdFilter())
        logger.addHandler(console_handler)
        
        # File handler with rotation
        if log_to_file:
            log_dir = Path(settings.LOG_DIR)
            log_dir.mkdir(exist_ok=True)
            
            # Create hourly rotating file handler
            log_file = log_dir / f"{name}.log"
            file_handler = TimedRotatingFileHandler(
                filename=log_file,
                when=settings.LOG_ROTATION,
                interval=1,
                backupCount=settings.LOG_BACKUP_COUNT,
                encoding="utf-8",
                utc=True
            )
            file_handler.suffix = "%Y%m%d_%H%M%S.log"
            file_handler.setFormatter(JSONFormatter())
            file_handler.addFilter(RequestIdFilter())
            logger.addHandler(file_handler)
            
            # Performance-specific log file
            if name == "json_comparison":
                perf_log_file = log_dir / "performance.log"
                perf_handler = TimedRotatingFileHandler(
                    filename=perf_log_file,
                    when=settings.LOG_ROTATION,
                    interval=1,
                    backupCount=settings.LOG_BACKUP_COUNT,
                    encoding="utf-8",
                    utc=True
                )
                perf_handler.suffix = "%Y%m%d_%H%M%S.log"
                perf_handler.setFormatter(JSONFormatter())
                perf_handler.addFilter(RequestIdFilter())
                perf_handler.addFilter(lambda record: hasattr(record, "performance"))
                logger.addHandler(perf_handler)
    
    return logger

def get_logger(name: Optional[str] = None) -> logging.Logger:
    if name:
        return logging.getLogger(name)
    return logging.getLogger("app")