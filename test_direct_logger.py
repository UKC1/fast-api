import sys
sys.path.insert(0, '.')

from app.observability import setup_logger

# Direct test
logger = setup_logger("direct_test", level="INFO")
logger.info("This is a direct test message")

# Check middleware logger
middleware_logger = setup_logger("middleware")
middleware_logger.info("This is a middleware test message")

# Check json_comparison logger  
json_logger = setup_logger("json_comparison")
json_logger.info("JSON comparison test", extra={
    "performance": {
        "library": "test",
        "encode_ms": 1.23,
        "decode_ms": 4.56
    }
})

print("\nTest completed. Check logs/ directory for:"
      "\n- direct_test.log"
      "\n- middleware.log" 
      "\n- json_comparison.log")