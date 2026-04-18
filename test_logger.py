from app.observability import setup_logger

# Test logger setup
logger = setup_logger("test", level="INFO")

# Log some test messages
logger.info("Test info message")
logger.warning("Test warning message")
logger.error("Test error message")

# Log with extra data
logger.info("Test with performance data", extra={
    "performance": {
        "duration_ms": 123.456,
        "status": "success"
    }
})

print("Logging test completed. Check logs/ directory for output files.")