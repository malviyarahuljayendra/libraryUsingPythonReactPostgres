import logging
import json
import sys
from backend.core.context import request_id_ctx_var
from datetime import datetime

class ContextFilter(logging.Filter):
    """
    This filter injects the request_id from the context variable into the log record.
    """
    def filter(self, record):
        record.request_id = request_id_ctx_var.get() or "SYSTEM"
        return True

def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Check if handlers already exist to avoid adding duplicates
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        # Format: [uuid] [backend] [time] [className.methodName] [logLevel] logging statement
        formatter = logging.Formatter(
            '[%(request_id)s] [library_backend] [%(asctime)s] [%(levelname)s] [%(module)s.%(funcName)s] %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    logger.addFilter(ContextFilter())
    return logger

logger = setup_logger("library_backend")
