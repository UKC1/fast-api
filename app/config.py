import os
from typing import Literal

class Settings:
    # Environment
    ENV: Literal["local", "dev", "prod"] = os.getenv("ENV", "local")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO" if ENV != "prod" else "WARNING")
    LOG_TO_FILE: bool = ENV == "local"  # Only log to file in local environment
    LOG_DIR: str = "logs"
    LOG_ROTATION: str = "H"  # Hourly rotation
    LOG_BACKUP_COUNT: int = 24 * 7  # Keep 7 days of logs
    
    # API
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8080"))
    
    # Performance monitoring
    ENABLE_PERFORMANCE_LOGGING: bool = True
    PERFORMANCE_LOG_THRESHOLD_MS: float = 100  # Log requests slower than this

settings = Settings()